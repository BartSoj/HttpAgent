import json
import http.server
from urllib.parse import urlparse
import socketserver
import webbrowser
import logging
from datetime import timezone, datetime
from attrs import asdict
from binapy import BinaPy
from requests_oauth2client import OAuth2Client, BearerTokenSerializer, OAuth2AccessTokenAuth, BearerToken

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class CallbackHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        if parsed_path.path == '/callback':
            self._handle_callback()
        else:
            self._handle_unknown_path(parsed_path.path)

    def _handle_callback(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Authorization successful! You can close this window.")
        self.server.callback_uri = self.path
        logger.info("Callback received successfully")

    def _handle_unknown_path(self, path):
        self.send_error(404, "Not Found")
        logger.warning(f"Received request for unknown path: {path}")


class AuthManager:
    def __init__(self, api_clients_path, port=8888):
        self.port = port
        self.token_file_path = api_clients_path
        self.token_serializer = self._get_token_serializer()

    def add_client_tokens(self):
        clients = self._load_clients()
        with socketserver.TCPServer(('', self.port), CallbackHandler) as httpd:
            for client in clients:
                if "token" not in client:
                    self._process_client(client, httpd)
        self._save_clients(clients)
        logger.info("All clients have been authorized.")

    def get_auths(self):
        clients = self._load_clients()
        auths = {}
        for client in clients:
            auth_name = client["name"]
            auth_client = self._create_auth_client(client)
            token = self._create_bearer_token(client)
            auths[auth_name] = OAuth2AccessTokenAuth(auth_client, token)
        return auths

    def save_auths(self, auths):
        clients = self._load_clients()
        for client in clients:
            token = auths[client["name"]].token
            client["token"] = self._serialize_token(token)
        self._save_clients(clients)
        logger.info("Authentications have been saved.")

    def _get_token_serializer(self):
        return BearerTokenSerializer(dumper=self._token_dumper, loader=self._token_loader)

    def _token_dumper(self, token):
        d = asdict(token)
        d.update(**d.pop("kwargs", {}))
        token_dict = {key: val for key, val in d.items() if val is not None}
        return BinaPy.serialize_to("json", token_dict).to("deflate").to("b64u").ascii()

    def _token_loader(self, serialized, token_class=BearerToken):
        attrs = BinaPy(serialized).decode_from("b64u").decode_from("deflate").parse_from("json")
        expires_at = attrs.get("expires_at")
        if expires_at:
            attrs["expires_at"] = datetime.fromtimestamp(expires_at, tz=timezone.utc)
        return token_class(**attrs)

    def _load_clients(self):
        with open(self.token_file_path, "r") as tokens_file:
            return json.load(tokens_file)

    def _process_client(self, client, httpd):
        auth_client = self._create_auth_client(client)
        az_request = auth_client.authorization_request(scope=client["scope"], access_type="offline")
        logger.info(f"Please authorize {client['name']} client. A browser window will open automatically.")
        response_uri = self._get_authorization_code(az_request.uri, httpd)
        token = self._get_token(auth_client, az_request, response_uri)
        client["token"] = self._serialize_token(token)
        logger.info(f"Token for {client['name']} client has been saved.")

    def _create_auth_client(self, client_json):
        return OAuth2Client(
            token_endpoint=client_json["token_endpoint"],
            authorization_endpoint=client_json["authorization_endpoint"],
            redirect_uri=f"http://localhost:{self.port}/callback",
            client_id=client_json["client_id"],
            client_secret=client_json["client_secret"]
        )

    def _create_bearer_token(self, client_json):
        return self.token_serializer.loads(client_json["token"])

    def _get_authorization_code(self, auth_url, httpd):
        httpd.callback_uri = None
        webbrowser.open(auth_url)
        logger.info("Waiting for authorization...")
        httpd.handle_request()
        return httpd.callback_uri

    def _get_token(self, auth_client, az_request, response_uri):
        az_response = az_request.validate_callback(response_uri)
        return auth_client.authorization_code(az_response)

    def _serialize_token(self, token):
        return self.token_serializer.dumps(token)

    def _save_clients(self, clients):
        with open(self.token_file_path, "w") as tokens_file:
            json.dump(clients, tokens_file, indent=2)
