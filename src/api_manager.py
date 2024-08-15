import requests
from urllib.parse import urlparse
import logging
from auth_manager import AuthManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class APIManager:
    def __init__(self, api_clients_path):
        self.auths = {}
        self.token_manager = None
        if api_clients_path:
            self.token_manager = AuthManager(api_clients_path)
            self._load_auths()

    def _load_auths(self):
        self.auths = self.token_manager.get_auths()
        logger.info(f"Loaded {len(self.auths)} authentications")

    def cleanup(self):
        if self.token_manager:
            self.token_manager.save_auths(self.auths)

    def send_request(self, method, url, headers=None, params=None, data=None, json=None):
        """
        Send an HTTP request with the given parameters.

        :param method: HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE')
        :param url: The URL to send the request to
        :param headers: (optional) A dictionary of HTTP headers
        :param params: (optional) A dictionary of query parameters
        :param data: (optional) A dictionary, list of tuples, bytes, or file-like object to send in the body
        :param json: (optional) A JSON serializable object to send in the body
        :return: A tuple containing (status_code, response_text)
        """
        try:
            auth_name = urlparse(url).netloc
            auth = self.auths.get(auth_name)
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                auth=auth
            )

            log_message = (f"{method} {url}" +
                           (f" Headers: {headers}" if headers else "") +
                           (f" Params: {params}" if params else "") +
                           (f" Data: {data}" if data else "") +
                           (f" body: {json}" if json else "") +
                           f" Response: {response.status_code} {response.text}")
            logger.info(log_message)
            return response.status_code, response.text
        except requests.RequestException as e:
            return None, str(e)
