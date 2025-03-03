import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import uvicorn
from pydantic import BaseModel

from agents.generic_agent import GenericAgent
from reasoners.generic_reasoner import GenericReasoner
from agents.httpAgent.request_processor import RequestProcessor
from utils.openai_client import OpenAIClient

logger = logging.getLogger(__name__)


class HttpResponseFormat(BaseModel):
    content: str
    status_code: int


class HttpAgent(GenericAgent):

    def __init__(self,
                 model: str = "gpt-4o",
                 instructions: str = "",
                 temperature: int = None,
                 reasoner: GenericReasoner = None,
                 request_action_function_schema: dict = None,
                 request_processor: RequestProcessor = RequestProcessor()):
        super().__init__(reasoner)
        self.openai_client = OpenAIClient().get_client()
        self.model = model
        self.instructions = instructions
        self.temperature = temperature
        self.request_action_function_schema = request_action_function_schema
        self.request_action_function_name = request_action_function_schema["function"]["name"]
        self.request_processor = request_processor
        self.app = FastAPI()
        self.app.api_route("/{path_name:path}", methods=["GET", "OPTIONS", "HEAD", "POST", "PUT", "PATCH", "DELETE"])(
            self.catch_all)
        self.server = None

    async def catch_all(self, request: Request, path_name: str):
        if path_name == "exit":
            logger.info("Shutdown requested via /exit endpoint.")
            if self.server:
                self.server.should_exit = True
            return JSONResponse(content="Server is shutting down", status_code=200)

        json_request = await self.request_to_json(request)
        logger.info(f"Request received: {json_request}")
        preprocessed_request = self.preprocess_request(json_request)
        http_response = self.__get_chat_response(preprocessed_request)
        logger.info(f"Response sent: status {http_response.status_code} {http_response.content}")
        return JSONResponse(
            content=http_response.content,
            status_code=http_response.status_code,
        )

    async def request_to_json(self, request: Request):
        result = {
            "method": request.method,
            "url": request.url.path,
        }

        if request.query_params:
            result["params"] = dict(request.query_params)

        # if request.headers:
        #     result["headers"] = dict(request.headers)

        body = await request.body()
        if body:
            result["body"] = json.loads(body)

        return result

    def preprocess_request(self, request_json: dict):
        request_processed = self.request_processor.process_incoming_request(request_json)
        return json.dumps(request_processed, indent=2)

    def __get_chat_response(self, request_message) -> HttpResponseFormat:
        """
        Gives chat response to the provided messages, using reasoner to execute actions when required.
        1. prompt the model with the messages
        2. checks if reasoner action required
        3. if reasoner action required, executes action using reasoner
        3.1 updates the messages with reasoner action result
        3.2 goes to step 1.
        4. if reasoner action not required, returns model response

        :param request_message: Message with the server request
        :return: Response to the last message from the assistant
        """
        messages = [
            {
                "role": "developer",
                "content": self.instructions
            },
            {
                "role": "user",
                "content": request_message
            }
        ]

        while True:
            response = self.openai_client.beta.chat.completions.parse(
                model=self.model,
                temperature=self.temperature,
                messages=messages,
                parallel_tool_calls=False,
                tools=[self.request_action_function_schema],
                response_format=HttpResponseFormat
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

        return response.choices[0].message.parsed

    def __call_function(self, name, args):
        if name != self.request_action_function_name:
            raise Exception(f"Unknown function: {name}")
        return self.reasoner.process_request(args.get("action_description"))

    def start(self):
        config = uvicorn.Config(self.app, host="0.0.0.0", port=8000, log_level="info")
        self.server = uvicorn.Server(config)
        self.server.run()
