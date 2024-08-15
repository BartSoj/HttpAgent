import json
from openai_client import OpenAIClient
import logging

from api_manager import APIManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class AssistantBuilder:
    def __init__(self, name):
        self.name = name
        self.model = "gpt-4o-mini"
        self.description = None
        self.instructions = None
        self.temperature = None
        self.api_clients_path = None
        self.function_paths = None
        self.file_search_vector_store_ids = None

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

    def set_function_paths(self, function_paths):
        self.function_paths = function_paths
        return self

    def set_file_search_vector_store_ids(self, file_search_vector_store_ids):
        self.file_search_vector_store_ids = file_search_vector_store_ids
        return self

    def build(self):
        return Assistant(self.name,
                         self.model,
                         self.description,
                         self.instructions,
                         self.temperature,
                         self.api_clients_path,
                         self.function_paths,
                         self.file_search_vector_store_ids)


class Assistant:
    def __init__(self, name,
                 model="gpt-4o-mini",
                 description=None,
                 instructions=None,
                 temperature=None,
                 api_clients_path=None,
                 function_paths=None,
                 file_search_vector_store_ids=None):

        self.openai_client = OpenAIClient().get_client()

        self.name = name
        self.api_manager = APIManager(api_clients_path)

        tools = []
        tools_resources = {}

        if file_search_vector_store_ids:
            file_search = {"type": "file_search"}
            tools.append(file_search)
            tools_resources["file_search"] = {"vector_store_ids": file_search_vector_store_ids}

        if function_paths:
            functions = [json.load(open(function_path)) for function_path in function_paths]
            tools.extend(functions)

        self.assistant = self.openai_client.beta.assistants.create(
            name=name,
            model=model,
            description=description,
            instructions=instructions,
            temperature=temperature,
            tools=tools,
            tool_resources=tools_resources,
        )

        self.thread = self.openai_client.beta.threads.create()

    def _parse_request_argument(self, request_argument):
        if request_argument and isinstance(request_argument, dict):
            return request_argument
        if request_argument and isinstance(request_argument, str) and request_argument.startswith("{"):
            return json.loads(request_argument)
        return None

    def send_request_from_json(self, json_request):
        function_arguments = json.loads(json_request)
        method = function_arguments["method"]
        url = function_arguments["url"]
        headers = self._parse_request_argument(function_arguments.get("headers"))
        params = self._parse_request_argument(function_arguments.get("params"))
        data = self._parse_request_argument(function_arguments.get("data"))
        body = self._parse_request_argument(function_arguments.get("body"))
        return self.api_manager.send_request(method, url, headers, params, data, body)

    def print_messages(self):
        messages = list(self.openai_client.beta.threads.messages.list(thread_id=self.thread.id))
        for message in reversed(messages):
            role = message.role.capitalize()
            content = message.content[0].text.value
            print(f"\n## {role}")
            print("-" * (len(role) + 3))
            print(content)
            print()

    def handle_actions(self, run):
        tool_outputs = []

        for tool in run.required_action.submit_tool_outputs.tool_calls:
            if tool.function.name == "send_api_request":
                status, text = self.send_request_from_json(tool.function.arguments)
                tool_outputs.append(
                    {
                        "tool_call_id": tool.id,
                        "output": f"Status code: {status}, Response text: {text}"
                    }
                )

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

    def send_message(self, content):
        message = self.openai_client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=content
        )

        run = self.openai_client.beta.threads.runs.create_and_poll(
            thread_id=self.thread.id, assistant_id=self.assistant.id
        )

        return run

    def close(self):
        self.openai_client.beta.assistants.delete(assistant_id=self.assistant.id)
        self.openai_client.beta.threads.delete(thread_id=self.thread.id)
        self.api_manager.cleanup()

    def run(self):
        try:
            while True:
                user_input = input("You: ")
                if user_input == "exit":
                    break

                run = self.send_message(user_input)

                while run.required_action:
                    run = self.handle_actions(run)

                if run.status == 'completed':
                    self.print_messages()
                else:
                    logger.error("actions executed, but run is not completed")
                    self.print_messages()
        finally:
            self.close()
