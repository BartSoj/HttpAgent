import json

from agents.textAgent.text_agent import TextAgent
from reasoners.openApiReasoner.auth_manager import AuthManager
from reasoners.openApiReasoner.open_api_reasoner import OpenApiReasoner
from reasoners.openApiReasoner.openapi_manager import OpenapiManager
from reasoners.openApiReasoner.request_manager import RequestManager


def create_auth_manager():
    api_clients_path = "../../resources/api_clients/api_clients.json"
    api_tokens_path = "../../resources/api_clients/api_tokens.json"
    return AuthManager(api_clients_path, api_tokens_path)


def create_request_manager():
    with open("../../resources/functions/send_api_request.json") as file:
        send_api_request_function_schema = json.load(file)
    token_manager = create_auth_manager()
    return RequestManager(send_api_request_function_schema, token_manager)


def create_openapi_manager():
    with open("../../resources/functions/get_operation.json") as file:
        get_operation_function_schema = json.load(file)
    with open("../../resources/functions/list_operations.json") as file:
        list_operations_function_schema = json.load(file)
    openapi_file_paths = {
        "wolframalpha": "../../resources/apis/wolfram_openapi.json",
        "discord": "../../resources/apis/discord_openapi.json",
        "calendar": "../../resources/apis/calendar_openapi.json",
        "tasks": "../../resources/apis/tasks_openapi.json",
        "spotify": "../../resources/apis/spotify_openapi.json"
    }
    return OpenapiManager(list_operations_function_schema, get_operation_function_schema, openapi_file_paths)


def main():
    with open("../../resources/instructions/openapi_reasoner_instructions_v1.txt", "r") as file:
        reasoner_instructions = file.read()
    openapi_manager = create_openapi_manager()
    request_manager = create_request_manager()
    openapi_reasoner = OpenApiReasoner(
        instructions=reasoner_instructions,
        openapi_manager=openapi_manager,
        request_manager=request_manager
    )

    with open("../../resources/instructions/text_agent_instructions_v1.txt", "r") as file:
        agent_instructions = file.read()
    with open("../../resources/functions/request_action.json") as file:
        request_action_function_schema = json.load(file)

    text_agent = TextAgent(
        instructions=agent_instructions,
        reasoner=openapi_reasoner,
        request_action_function_schema=request_action_function_schema
    )
    text_agent.start()

    request_manager.close()


if __name__ == "__main__":
    main()
