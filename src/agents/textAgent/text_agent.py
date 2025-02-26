import logging
import json

from agents.generic_agent import GenericAgent
from reasoners.generic_reasoner import GenericReasoner
from utils.openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class TextAgent(GenericAgent):
    def __init__(self,
                 model: str = "gpt-4o-mini",
                 instructions: str = "",
                 temperature: int = None,
                 reasoner: GenericReasoner = None,
                 request_action_function_schema: dict = None):
        super().__init__(reasoner)
        self.openai_client = OpenAIClient().get_client()
        self.model = model
        self.instructions = instructions
        self.temperature = temperature
        self.request_action_function_schema = request_action_function_schema
        self.request_action_function_name = request_action_function_schema["function"]["name"]

    def start(self):
        messages = [{
            "role": "developer",
            "content": self.instructions
        }]
        while True:
            user_reqeust = input("You: ")
            messages.append({
                "role": "user",
                "content": user_reqeust
            })
            chat_response = self._get_chat_response(messages)
            messages.append({
                "role": "assistant",
                "content": chat_response
            })
            print(f"Bot: {chat_response}")

    def _get_chat_response(self, messages):
        """
        Gives chat response to the provided messages, using reasoner to execute actions when required.
        1. prompt the model with the messages
        2. checks if reasoner action required
        3. if reasoner action required, executes action using reasoner
        3.1 updates the messages with reasoner action result
        3.2 goes to step 1.
        4. if reasoner action not required, returns model response

        :param messages: List of messages between user and assistant
        :return: Response to the last message from the assistant
        """
        while True:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                temperature=self.temperature,
                messages=messages,
                parallel_tool_calls=False,
                tools=[self.request_action_function_schema]
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

                result = self._call_function(name, args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return response.choices[0].message.content

    def _call_function(self, name, args):
        if name != self.request_action_function_name:
            raise Exception(f"Unknown function: {name}")
        return self.reasoner.process_request(args.get("action_description"))
