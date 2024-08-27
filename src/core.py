import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import json
import uvicorn

from reasoner import Reasoner
from request_processor import RequestProcessor

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Core:

    def __init__(self, reasoner: Reasoner, request_processor: RequestProcessor):
        self.reasoner = reasoner
        self.request_processor = request_processor
        self.app = FastAPI()
        self.app.api_route("/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE"])(self.catch_all)

    async def catch_all(self, request: Request, path_name: str):
        json_request = await self.request_to_json(request)
        logger.info(f"Request received: {json_request}")
        self.process_request(json_request)
        json_response = self.reasoner.get_answer()
        logger.info(f"Response sent: {json_response}")
        return JSONResponse(
            content=json_response["content"],
            status_code=json_response["status_code"],
        )

    async def request_to_json(self, request: Request):
        return {
            "method": request.method,
            "url": str(request.url),
            "query_params": dict(request.query_params),
            "path_params": dict(request.path_params),
            "body": await request.json(),
            "client": {"host": request.client.host, "port": request.client.port},
            "headers": dict(request.headers),
            "cookies": dict(request.cookies)
        }

    def process_request(self, request_json: dict):
        request_processed = self.request_processor.process_incoming_request(request_json)
        content = json.dumps(request_processed)
        self.process_input(content)

    def process_input(self, content):
        run = self.reasoner.send_message(content)

        while run.required_action:
            run = self.reasoner.handle_actions(run)

        if run.status != 'completed':
            logger.error("actions executed, but run is not completed")

    def start(self):
        try:
            uvicorn.run(self.app, host="0.0.0.0", port=8000)
        finally:
            self.reasoner.close()
