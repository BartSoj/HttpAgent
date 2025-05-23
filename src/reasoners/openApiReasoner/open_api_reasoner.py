import json
import logging

from reasoners.generic_reasoner import GenericReasoner
from utils.openai_client import OpenAIClient
from reasoners.openApiReasoner.openapi_manager import OpenapiManager
from reasoners.openApiReasoner.request_manager import RequestManager

logger = logging.getLogger(__name__)


class OpenApiReasoner(GenericReasoner):
    # TODO: there are multiple prompts so single model, instructions might not suffice
    def __init__(self,
                 model: str = "o3-mini",
                 instructions: str = "",
                 openapi_manager: OpenapiManager = None,
                 request_manager: RequestManager = None):
        super().__init__()
        self.openai_client = OpenAIClient().get_client()
        self.model = model
        self.instructions = instructions
        self.openapi_manager = openapi_manager
        self.request_manager = request_manager

        # context variables
        self.messages = []
        self.api_name_choice = None

    def _reset_context(self):
        self.messages = [
            {
                "role": "developer",
                "content": self.instructions
            }
        ]
        self.api_name_choice = None

    def _parse_argument_to_dict(self, arg):
        if isinstance(arg, dict) and arg:
            return arg

        if isinstance(arg, str):
            try:
                parsed = json.loads(arg)
                if isinstance(parsed, dict) and parsed:
                    return parsed
            except json.JSONDecodeError:
                pass

        try:
            parsed = dict(arg)
            if parsed:
                return parsed
        except Exception:
            pass

        return None

    def _send_request_from_json(self, json_request):
        logger.info(
            "Sending request to API: %s",
            json_request)
        try:
            function_arguments = json.loads(json_request)
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON API request. Request: %s", json_request)
            return json.dumps({
                "content": "Failed to parse JSON request.",
                "status_code": 400})
        method = function_arguments["method"]
        url = function_arguments["url"]
        params = self._parse_argument_to_dict(function_arguments.get("params"))
        headers = self._parse_argument_to_dict(function_arguments.get("headers"))
        body = self._parse_argument_to_dict(function_arguments.get("body"))

        response = self.request_manager.send_request(method, url, params, headers, body)
        return json.dumps(response)

    def _list_operations_from_json(self, json_spec):
        logger.info("Retrieving operations list from API: %s", json_spec)
        try:
            function_arguments = json.loads(json_spec)
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON specification: %s", json_spec)
            return "Failed to parse JSON specification."
        self.api_name_choice = function_arguments["api_name"]
        return json.dumps(self.openapi_manager.list_operation_ids_and_summaries(self.api_name_choice),
                          default=dict)  # default=dict is necessary as some objects are JsonRef which needs to be converted to dict otherwise they are not serializable

    def _get_operation_from_json(self, json_spec):
        logger.info("Retrieving operation details from API: %s", json_spec)
        try:
            function_arguments = json.loads(json_spec)
        except json.JSONDecodeError:
            logger.error("Failed to parse JSON specification: %s", json_spec)
            return "Failed to parse JSON specification."
        operation_id = function_arguments.get("operation_id")
        if not self.api_name_choice or not operation_id:
            raise Exception("API name or operation id not set.")
        return json.dumps(self.openapi_manager.get_operation_by_id(self.api_name_choice, operation_id), default=dict)

    def process_request(self,
                        request):  # TODO: allow for changing mind and calling the function again, asking for more data, or calling another reasoner for a subtask
        logger.info("OpenApi Reasoner request: %s", request)
        """
        Tries to execute the request, if executes responds based on response result, otherwise responds why request not executed.
        1. prompt the model with request
        2. checks if api call required
        3. if api call required, retrieves possible api requests
        3.1. prompt the model to send api request
        3.2. checks if send api request required
        3.3. if api request sent, update the request with the response go back to step 1.
        3.4. if api request not sent, return model response  #TODO: the request might not be sent because it needs more data (then should return a response requesting data) or another action is required (call new reasoner and proceed after the response)
        4. if api call not required, returns model response

        :param request: text explaining the request to execute
        :return: text response about request execution
        """

        self._reset_context()  # For now, we are resetting the context for each request, but in future we might want to keep the context

        self.messages.append({
            "role": "user",
            "content": request
        })
        while True:
            # list possible api requests
            response = self.openai_client.chat.completions.create(
                model=self.model,
                reasoning_effort="medium",
                messages=self.messages,
                tools=[self.openapi_manager.list_operations_function_schema]
            )

            finish_reason = response.choices[0].finish_reason
            if finish_reason == "stop":
                break
            if finish_reason != "tool_calls":
                raise Exception(f"Unexpected finish reason: {finish_reason}")

            self.messages.append(response.choices[0].message)  # append model's function call message

            if len(response.choices[0].message.tool_calls) > 1:
                raise Exception(f"Too many tool calls: {response.choices[0].message.tool_calls}")

            tool_call = response.choices[0].message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments

            if name != self.openapi_manager.list_operations_function_name:
                raise Exception(f"Unexpected tool call: {name}")

            result = self._list_operations_from_json(args)

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

            # get the details about chosen api request
            response = self.openai_client.chat.completions.create(
                model=self.model,
                reasoning_effort="medium",
                messages=self.messages,
                tools=[self.openapi_manager.get_operation_function_schema]
            )

            finish_reason = response.choices[0].finish_reason
            if finish_reason == "stop":
                break
            if finish_reason != "tool_calls":
                raise Exception(f"Unexpected finish reason: {finish_reason}")

            self.messages.append(response.choices[0].message)  # append model's function call message

            if len(response.choices[0].message.tool_calls) > 1:
                raise Exception(f"Too many tool calls: {response.choices[0].message.tool_calls}")

            tool_call = response.choices[0].message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments

            if name != self.openapi_manager.get_operation_function_name:
                raise Exception(f"Unexpected tool call: {name}")

            result = self._get_operation_from_json(args)

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

            # get the http request details and send the request
            response = self.openai_client.chat.completions.create(
                model=self.model,
                reasoning_effort="medium",
                messages=self.messages,
                tools=[self.request_manager.function_schema]
            )

            finish_reason = response.choices[0].finish_reason
            if finish_reason == "stop":
                break
            if finish_reason != "tool_calls":
                raise Exception(f"Unexpected finish reason: {finish_reason}")

            self.messages.append(response.choices[0].message)  # append model's function call message

            if len(response.choices[0].message.tool_calls) > 1:
                raise Exception(f"Too many tool calls: {response.choices[0].message.tool_calls}")

            tool_call = response.choices[0].message.tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments

            if name != self.request_manager.function_name:
                raise Exception(f"Unexpected tool call: {name}")

            result = self._send_request_from_json(args)

            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

        logger.info("OpenApi Reasoner response: %s", response.choices[0].message.content)
        return response.choices[0].message.content
