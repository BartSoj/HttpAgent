import json
import logging

from reasoners.generic_reasoner import GenericReasoner
from utils.openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class FunctionReasoner(GenericReasoner):
    def __init__(self,
                 model: str = "gpt-4o-mini",
                 instructions: str = "",
                 temperature: int = None,
                 function_spec_paths: list[str] = None,
                 functions: dict = None):
        super().__init__()
        self.openai_client = OpenAIClient().get_client()
        self.model = model
        self.instructions = instructions
        self.temperature = temperature
        self.functions = functions

        self.tools = []

        if function_spec_paths:
            function_specs = []
            for path in function_spec_paths:
                with open(path) as file:
                    function_specs.append(json.load(file))
            self.tools = function_specs

    def process_request(self, request):
        logger.info(f"Function reasoner request: {request}")
        """
        Tries to execute the request, if executes responds based on response result, otherwise responds why request not executed.
        1. prompt the model with request
        2. checks if function call required
        3. if api call required, executes the function
        3.1. updates the request with function result
        3.2. goes to step 1.
        4. if api call not required, returns model response

        :param request: text explaining the request to execute
        :return: text response about request execution
        """
        messages = [
            {
                "role": "developer",
                "content": self.instructions
            },
            {
                "role": "user",
                "content": request
            }
        ]
        while True:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=messages,
                parallel_tool_calls=True,
                tools=self.tools
            )

            finish_reason = response.choices[0].finish_reason
            if finish_reason == "stop":
                break
            if finish_reason != "tool_calls":
                raise Exception(f"Unexpected finish reason: {finish_reason}")

            messages.append(response.choices[0].message)  # append model's function call message

            for tool_call in response.choices[0].message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                logger.info(f"Calling function: {name} with args: {args}")
                result = self.call_function(name, args)
                logger.info(f"Function result: {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        logger.info(f"Function reasoner response: {response.choices[0].message.content}")
        return response.choices[0].message.content

    def call_function(self, name, args):
        if name not in self.functions.keys():
            raise Exception(f"Unknown function: {name}")
        return str(self.functions[name](**args))
