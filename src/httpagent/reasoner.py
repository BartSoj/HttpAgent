import json
from openai_client import OpenAIClient
import logging

from api_manager import APIManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ReasonerBuilder:
    def __init__(self, name):
        self.name = name
        self.model = "gpt-4o-mini"
        self.description = None
        self.instructions = None
        self.temperature = None
        self.api_clients_path = None
        self.api_tokens_path = None
        self.send_api_request_function_path = None
        self.openapi_vector_store_id = None
        self.json_response_format_path = None

    def set_model(self, model):
        self.model = model
        return self

    def set_description(self, description):
        self.description = description
        return self

    def set_instructions(self, instructions):
        self.instructions = instructions
        return self

    def set_temperature(self, temperature):
        self.temperature = temperature
        return self

    def set_api_clients_path(self, api_clients_path):
        self.api_clients_path = api_clients_path
        return self

    def set_api_tokens_path(self, api_tokens_path):
        self.api_tokens_path = api_tokens_path
        return self

    def set_send_api_request_function_path(self, send_api_request_function_path):
        self.send_api_request_function_path = send_api_request_function_path
        return self

    def set_openapi_vector_store_id(self, openapi_vector_store_id):
        self.openapi_vector_store_id = openapi_vector_store_id
        return self

    def set_json_response_format_path(self, json_response_format_path):
        self.json_response_format_path = json_response_format_path
        return self

    def build(self):
        return Reasoner(self.name,
                        self.model,
                        self.description,
                        self.instructions,
                        self.temperature,
                        self.api_clients_path,
                        self.api_tokens_path,
                        self.send_api_request_function_path,
                        self.openapi_vector_store_id,
                        self.json_response_format_path)


class Reasoner:
    def __init__(self, name,
                 model="gpt-4o-mini",
                 description=None,
                 instructions=None,
                 temperature=None,
                 api_clients_path=None,
                 api_tokens_path=None,
                 send_api_request_function_path=None,
                 openapi_vector_store_id=None,
                 json_response_format_path=None):

        self.openai_client = OpenAIClient().get_client()

        self.name = name
        self.api_manager = APIManager(api_clients_path, api_tokens_path)

        tools = []
        tools_resources = {}

        if openapi_vector_store_id:
            file_search = {"type": "file_search"}
            tools.append(file_search)
            tools_resources["file_search"] = {"vector_store_ids": [openapi_vector_store_id]}

        if send_api_request_function_path:
            functions = [json.load(open(send_api_request_function_path))]
            tools.extend(functions)

        json_response_format = None

        if json_response_format_path:
            json_response_format = json.load(open(json_response_format_path))

        self.assistant = self.openai_client.beta.assistants.create(
            name=name,
            model=model,
            description=description,
            instructions=instructions,
            temperature=temperature,
            # response_format=json_response_format,  # TODO: response_format is not supported together with file_search, uncomment when OpenAI API supports it
            tools=tools,
            tool_resources=tools_resources,
        )

        self.thread = self.openai_client.beta.threads.create()

    def _parse_argument_to_dict(self, request_argument):
        if request_argument and isinstance(request_argument, dict):
            return request_argument
        if request_argument and isinstance(request_argument, str) and request_argument.startswith("{"):
            return json.loads(request_argument)
        return None

    def send_request_from_json(self, json_request):
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
        if "localhost:8000" in url:
            return json.dumps({
                "content": "you cannot send the response to the same server that sent the request. Make sure to use the correct api url",
                "status_code": 400})
        response = self.api_manager.send_request(method, url, params, headers, body)
        return json.dumps(response)

    def handle_actions(self, run):
        tool_outputs = []

        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "send_api_request":
                response = self.send_request_from_json(tool.function.arguments)
                tool_outputs.append(
                    {
                        "tool_call_id": tool.id,
                        "output": response
                    }
                )
            else:
                logger.error(f"Unknown tool function: {tool.function.name}")

        if tool_outputs:
            try:
                run = self.openai_client.beta.threads.runs.submit_tool_outputs_and_poll(
                    thread_id=self.thread.id,
                    run_id=run.id,
                    tool_outputs=tool_outputs
                )
            except Exception as e:
                logger.error("Failed to submit tool outputs:", e)
        else:
            logger.error("No tool outputs to submit.")

        return run

    def show_run(self, run):
        run_steps = self.openai_client.beta.threads.runs.steps.list(
            thread_id=self.thread.id,
            run_id=run.id,
            include=["step_details.tool_calls[*].file_search.results[*].content"]
        )
        print(f"Run ID: {run.id}")
        for step in run_steps:
            if step.type == "tool_calls":
                for tool_call in step.step_details.tool_calls:
                    if tool_call.type == "file_search":
                        for result in tool_call.file_search.results:
                            print(f"File ID: {result.file_id}")
                            print(f"Content: {result.content}")
                            print("---")

    def send_message(self, content):
        message = self.openai_client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=content
        )

        run = self.openai_client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id, assistant_id=self.assistant.id, tool_choice={"type": "file_search"}
        )

        return run

    def list_messages(self):
        messages = list(self.openai_client.beta.threads.messages.list(thread_id=self.thread.id))
        return messages

    def get_answer(self):
        answer = list(self.openai_client.beta.threads.messages.list(thread_id=self.thread.id))[0]
        # json_answer = json.loads(answer.content[0].text.value)  # TODO: response_format is not supported together with file_search, uncomment when OpenAI API supports it
        # json_answer["content"] = self._parse_argument_to_dict(json_answer["content"])
        content = answer.content[0].text.value
        json_answer = {"content": content, "status_code": 200}
        return json_answer

    def close(self):
        self.api_manager.close()
