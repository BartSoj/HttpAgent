from reasoner import ReasonerBuilder
from core import Core


def main():
    model = "gpt-4o-mini"

    description = "An AI assistant specialized in controlling various Google services, Spotify, and other APIs through HTTP requests."

    with open("resources/instructions/instructions.txt", "r") as file:
        instructions = file.read()

    temperature = 1e-6  # duo to openai api bug, temperature cannot be set to 0

    api_clients_path = "resources/api_clients/api_clients.json"
    api_tokens_path = "resources/api_clients/api_tokens.json"

    send_api_request_function_path = "resources/functions/send_api_request.json"

    retrieve_api_info_function_path = "resources/functions/retrieve_api_info.json"

    openapi_file_paths = {"wolframalpha": "resources/apis/wolfram_openapi.json",
                          "discord": "resources/apis/discord_openapi.json",
                          "calendar": "resources/apis/calendar_openapi.json",
                          "tasks": "resources/apis/tasks_openapi.json",
                          "spotify": "resources/apis/spotify_openapi.json"}

    # openapi_vector_store_id = "vs_eV2E9MwN7Y7FSf6Z4tYhSoql"  # You can use vector store with openapi files instead of openapi manager

    json_response_format_path = "resources/response_formats/json_response.json"

    reasoner = (ReasonerBuilder("HttpAgent")
                .set_model(model)
                .set_description(description)
                .set_instructions(instructions)
                .set_temperature(temperature)
                .set_api_clients_path(api_clients_path)
                .set_api_tokens_path(api_tokens_path)
                .set_send_api_request_function_path(send_api_request_function_path)
                .set_retrieve_api_info_function_path(retrieve_api_info_function_path)
                .set_openapi_file_paths(openapi_file_paths)
                # .set_openapi_vector_store_id(openapi_vector_store_id)  # For using vector store with openapi files
                .set_json_response_format_path(json_response_format_path)
                .build())

    core = Core(reasoner)
    core.start()


if __name__ == "__main__":
    main()
