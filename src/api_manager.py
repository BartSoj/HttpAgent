import requests
import logging
import tldextract
from auth_manager import AuthManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class APIManager:
    def __init__(self, api_clients_path, api_tokens_path):
        self.auths = {}
        self.token_manager = None
        if api_clients_path and api_tokens_path:
            self.token_manager = AuthManager(api_clients_path, api_tokens_path)
            self._load_auths()

    def _load_auths(self):
        self.auths = self.token_manager.get_auths()
        logger.info(f"Loaded {len(self.auths)} authentications")

    def send_request(self, method, url, params=None, headers=None, json=None):
        """
        Send an HTTP request with the given parameters.

        :param method: HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE')
        :param url: The URL to send the request to
        :param params: (optional) A dictionary of query parameters
        :param headers: (optional) A dictionary of HTTP headers
        :param json: (optional) A JSON serializable object to send in the body
        :return: A tuple containing (status_code, response_text)
        """
        try:
            auth_name = tldextract.extract(url).domain
            auth = self.auths.get(auth_name)
            response = requests.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=json,
                auth=auth
            )

            log_message = (f"{method} {url}" +
                           (f" Headers: {headers}" if headers else "") +
                           (f" Params: {params}" if params else "") +
                           (f" Body: {json}" if json else "") +
                           f" Response: {response.status_code} {response.text}")
            logger.info(log_message)
            return {"content": response.text, "status_code": response.status_code}
        except requests.RequestException as e:
            logger.error(f"Failed to send request to {url}: {e}")
            return None, str(e)

    def close(self):
        if self.token_manager:
            self.token_manager.save_auths(self.auths)
