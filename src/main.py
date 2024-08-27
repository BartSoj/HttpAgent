import requests

from reasoner import ReasonerBuilder
from request_processor import RequestProcessor
from core import Core


def process_incoming_request(request):
    context = requests.get("http://0.0.0.0:8001/context")
    memory = requests.get("http://0.0.0.0:8001/memory")
    if not request["body"]:
        request["body"] = {}
    request["body"]["context"] = context.json()
    request["body"]["memory"] = memory.json()
    return request


def main():
    description = "An AI assistant specialized in controlling various Google services, Spotify, and other APIs through HTTP requests."

    instructions = (
        "You are an AI assistant designed to interact with multiple APIs, including Google services and Spotify. "
        "The messages you receive will be in a form of HTTP requests in a JSON format, and they are coming from different web services. (these will be webhooks or direct http requests)"
        "You need to understand the request, determine if any action is required, and respond accordingly by interacting with the appropriate APIs. "
        "Run the `send_api_request` function to interact with the appropriate APIs and return a HTTP response in a JSON format.\n\n"
        "Your primary functions include managing and controlling various aspects of web services through API requests. "
        "The APIs you can interact with are:\n\n"
        "1. Google Calendar\n"
        "2. Google Chat\n"
        "3. Google Docs\n"
        "4. Google Drive\n"
        "5. Gmail\n"
        "6. Google People\n"
        "7. Google Apps Script\n"
        "8. Google Sheets\n"
        "9. Google Slides\n"
        "10. Spotify\n"
        "11. Google Tasks\n\n"
        "When a received http request indicates a need for an action related to any of these services, follow these steps:\n\n"
        "1. Identify the appropriate API based on the user's request.\n"
        "2. Consult the relevant OpenAPI specification file (e.g., calendar_openapi.json, spotify_openapi.json, etc.) "
        "to determine the correct API method, URL, and parameters.\n"
        "3. Construct the API request using the `send_api_request` function, ensuring all necessary parameters are included.\n"
        "4. Do not include authentication tokens in the request header, as they will be added automatically after the request is sent.\n"
        "5. Execute the action by calling the `send_api_request` function with the constructed request.\n"
        "6. Interpret the API response and follow up with the next `send_api_request` function if required or return a http response.\n\n"
        "Always strive to understand the intent of the request and provide helpful, accurate responses in a form of api calls.\n\n"
        "Key points:\n"
        "- Always double-check that you're using the correct headers, params, data, and body for each request.\n"
        "- Determine what api request need to be sent and respond by sending the http response in a json format.\n"
        "- In case no action is required, return a http response indicating that the request was successfully processed immediatelly.\n"
        "- Present results efficiently, focusing on the most relevant information that answers the question.\n"
        "- Avoid unnecessary explanations or verbose responses.\n"
        "- If a request is unclear or outside your capabilities, ask for clarification or politely explain your limitations.\n\n"
        "Remember, your goal is to provide accurate and concise responses that efficiently address the needs of the request. "
        "For detailed information about each API's capabilities, refer to the corresponding OpenAPI specification file."
    )

    temperature = 0.2

    api_clients_path = "resources/api_clients/api_clients.json"
    api_tokens_path = "resources/api_clients/api_tokens.json"

    send_api_request_function_path = "resources/functions/send_api_request.json"
    openapi_vector_store_id = "vs_eV2E9MwN7Y7FSf6Z4tYhSoql"
    json_response_format_path = "resources/response_formats/json_response.json"

    reasoner = (ReasonerBuilder("API Control Assistant")
                .set_description(description)
                .set_instructions(instructions)
                .set_temperature(temperature)
                .set_api_clients_path(api_clients_path)
                .set_api_tokens_path(api_tokens_path)
                .set_send_api_request_function_path(send_api_request_function_path)
                .set_openapi_vector_store_id(openapi_vector_store_id)
                .set_json_response_format_path(json_response_format_path)
                .build())

    request_processor = RequestProcessor(incoming_request_processor=process_incoming_request)

    core = Core(reasoner, request_processor)
    core.start()


if __name__ == "__main__":
    main()
