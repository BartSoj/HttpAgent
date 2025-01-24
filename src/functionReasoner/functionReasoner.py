import json

from utils.openai_client import OpenAIClient


class FunctionReasoner:
    def __init__(self,
                 model="gpt-4o-mini",
                 system="",
                 temperature: int = None,
                 function_spec_paths: list[str] = None,
                 functions: dict = None):
        self.openai_client = OpenAIClient().get_client()
        self.model = model
        self.system = system
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
        messages = [
            {
                "role": "system",
                "content": self.system
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

                result = self.call_function(name, args)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result
                })

        return response.choices[0].message.content

    def call_function(self, name, args):
        if name in self.functions.keys():
            return str(self.functions[name](**args))
        else:
            return f"Function {name} not found."
