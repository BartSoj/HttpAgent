import json
import unittest

from reasoners.openApiReasoner.auth_manager import AuthManager
from reasoners.openApiReasoner.open_api_reasoner import OpenApiReasoner
from reasoners.openApiReasoner.openapi_manager import OpenapiManager
from reasoners.openApiReasoner.request_manager import RequestManager


class OpenApiReasonerTest(unittest.TestCase):
    def create_auth_manager(self):
        api_clients_path = "../../../resources/api_clients/api_clients.json"
        api_tokens_path = "../../../resources/api_clients/api_tokens.json"
        return AuthManager(api_clients_path, api_tokens_path)

    def create_request_manager(self):
        with open("../../../resources/functions/send_api_request.json") as file:
            send_api_request_function_schema = json.load(file)
        token_manager = self.create_auth_manager()
        return RequestManager(send_api_request_function_schema, token_manager)

    def create_openapi_manager(self):
        with open("../../../resources/functions/get_operation.json") as file:
            get_operation_function_schema = json.load(file)
        with open("../../../resources/functions/list_operations.json") as file:
            list_operations_function_schema = json.load(file)
        openapi_file_paths = {
            "wolframalpha": "../../../resources/apis/wolfram_openapi.json",
            "discord": "../../../resources/apis/discord_openapi.json",
            "calendar": "../../../resources/apis/calendar_openapi.json",
            "tasks": "../../../resources/apis/tasks_openapi.json",
            "spotify": "../../../resources/apis/spotify_openapi.json"
        }
        return OpenapiManager(list_operations_function_schema, get_operation_function_schema, openapi_file_paths)

    def setUp(self):
        with open("../../../resources/instructions/openapi_reasoner_instructions_v1.txt", "r") as file:
            instructions = file.read()
        self.openapi_reasoner = OpenApiReasoner(
            instructions=instructions,
            openapi_manager=self.create_openapi_manager(),
            request_manager=self.create_request_manager()
        )

    def test_openapi_reasoner(self):
        request = "give distance from Amsterdam to Eindhoven"
        response = self.openapi_reasoner.process_request(request)
        self.assertIn("111", response)
