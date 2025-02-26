import requests
import logging
import tldextract

from reasoners.openApiReasoner.auth_manager import AuthManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class RequestManager:
    def __init__(self, function_schema: dict, token_manager: AuthManager):
        self.function_schema = function_schema
        self.function_name = function_schema["function"]["name"]
        self.auths = {}
        self.token_manager = token_manager
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
        log_message = (f"API Request: {method} {url}" +
                       (f" Headers: {headers}" if headers else "") +
                       (f" Params: {params}" if params else "") +
                       (f" Body: {json}" if json else ""))
        logger.info(log_message)

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

            log_message = f"API Response: {response.status_code} {response.text}"
            logger.info(log_message)
            return {"content": response.text, "status_code": response.status_code}
        except requests.RequestException as e:
            logger.error(f"Failed to send request to {url}: {e}")
            return None, str(e)

    def close(self):
        if self.token_manager:
            self.token_manager.save_auths(self.auths)
