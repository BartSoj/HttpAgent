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
    def __init__(self, api_clients_path, api_tokens_path, port=8888):
        self.port = port
        self.api_clients_path = api_clients_path
        self.api_tokens_path = api_tokens_path
        self.token_serializer = self._get_token_serializer()

    def add_client_tokens(self):
        clients = self._load_clients()
        tokens = self._load_tokens()
        with socketserver.TCPServer(('', self.port), CallbackHandler) as httpd:
            for client in clients:
                if not tokens.get(client["name"]):
                    tokens[client["name"]] = self._retrieve_token(client, httpd)
        self._save_tokens(tokens)
        logger.info("All clients have been authorized.")

    def add_client_token_manually(self, name, access_token, refresh_token=None, expires_at=None):
        clients = self._load_clients()
        tokens = self._load_tokens()
        for client in clients:
            if client["name"] == name:
                token = BearerToken(access_token, refresh_token=refresh_token, expires_at=expires_at)
                tokens[client["name"]] = self._serialize_token(token)
                logger.info(f"Client {name} has been authorized.")
                break
        else:
            logger.error(f"Client {name} not found.")
        self._save_tokens(tokens)

    def get_auths(self):
        clients = self._load_clients()
        tokens = self._load_tokens()
        auths = {}
        for client in clients:
            auth_name = client["name"]
            auth_client = self._create_auth_client(client)
            token = self._create_bearer_token(tokens[auth_name])
            auths[auth_name] = OAuth2AccessTokenAuth(auth_client, token)
        return auths

    def save_auths(self, auths):
        clients = self._load_clients()
        tokens = self._load_tokens()
        for client in clients:
            token = auths[client["name"]].token
            tokens[client["name"]] = self._serialize_token(token)
        self._save_tokens(tokens)
        logger.info("Authentications have been saved.")

    def _retrieve_token(self, client, httpd):
        auth_client = self._create_auth_client(client)
        az_request = auth_client.authorization_request(scope=client["scope"], access_type="offline")
        logger.info(f"Please authorize {client['name']} client. A browser window will open automatically.")
        response_uri = self._get_authorization_code(az_request.uri, httpd)
        az_response = az_request.validate_callback(response_uri)
        token = auth_client.authorization_code(az_response)
        logger.info(f"Token for {client['name']} has been retrieved.")
        return self._serialize_token(token)

    def _get_authorization_code(self, auth_url, httpd):
        httpd.callback_uri = None
        webbrowser.open(auth_url)
        logger.info("Waiting for authorization...")
        while httpd.callback_uri is None:
            httpd.handle_request()
        return httpd.callback_uri

    def _serialize_token(self, token):
        return self.token_serializer.dumps(token)

    def _create_auth_client(self, client_json):
        return OAuth2Client(
            token_endpoint=client_json["token_endpoint"],
            authorization_endpoint=client_json["authorization_endpoint"],
            redirect_uri=f"http://localhost:{self.port}/callback",
            client_id=client_json["client_id"],
            client_secret=client_json["client_secret"]
        )

    def _create_bearer_token(self, token_json):
        return self.token_serializer.loads(token_json)

    def _load_clients(self):
        with open(self.api_clients_path, "r") as api_clients:
            return json.load(api_clients)

    def _load_tokens(self):
        try:
            with open(self.api_tokens_path, "r") as api_tokens:
                return json.load(api_tokens)
        except FileNotFoundError:
            return {}

    def _save_clients(self, clients):
        with open(self.api_clients_path, "w") as api_clients:
            json.dump(clients, api_clients, indent=2)

    def _save_tokens(self, tokens):
        with open(self.api_tokens_path, "w") as api_tokens:
            json.dump(tokens, api_tokens, indent=2)

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
