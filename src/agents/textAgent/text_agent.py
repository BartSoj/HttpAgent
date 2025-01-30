import logging
import json

from agents.generic_agent import GenericAgent
from reasoners.generic_reasoner import GenericReasoner
from utils.openai_client import OpenAIClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TextAgent(GenericAgent):
    def __init__(self,
                 model: str = "gpt-4o-mini",
                 system: str = "",
                 temperature: int = None,
                 reasoner: GenericReasoner = None,
                 request_action_function_path: str = None):
        super().__init__(reasoner)
        self.openai_client = OpenAIClient().get_client()
        self.model = model
        self.system = system
        self.temperature = temperature
        request_action_function = self.__parse_function_path(request_action_function_path)
        self.tools = [request_action_function]
        self.request_action_function_name = request_action_function["function"]["name"]

    def __parse_function_path(self, function_path) -> dict:
        with open(function_path) as file:
            function = json.load(file)
        if not function or function["type"] != "function":
            raise Exception("Function not found")
        return function

    def start(self):
        messages = []
        while True:
            user_reqeust = input("You: ")
            messages.append({
                "role": "user",
                "content": user_reqeust
            })
            chat_response = self.__get_chat_response(messages)
            messages.append({
                "role": "assistant",
                "content": chat_response
            })
            print(f"Bot: {chat_response}")

    def __get_chat_response(self, messages):
        while True:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=messages,
                parallel_tool_calls=False,
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

                result = self.__call_function(name, args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return response.choices[0].message.content

    def __call_function(self, name, args):
        if name != self.request_action_function_name:
            raise Exception(f"Unknown function: {name}")
        return self.reasoner.process_request(args.get("action_description"))
