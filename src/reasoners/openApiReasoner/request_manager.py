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

    def _log_request(self, method, url, params, headers, json_data):
        message = f"API Request: {method} {url}"
        if headers:
            message += f" Headers: {headers}"
        if params:
            message += f" Params: {params}"
        if json_data:
            message += f" Body: {json_data}"
        logger.info(message)

    def _get_auth(self, url):
        auth_name = tldextract.extract(url).domain
        return self.auths.get(auth_name)

    def _parse_response(self, response):
        content_type = response.headers.get("Content-Type", "").lower()

        if "application/json" in content_type:
            try:
                return response.json()
            except ValueError:
                return {"error": "Invalid JSON response."}
        elif "text" in content_type or "xml" in content_type:
            # For text-based content types, use the text if it's nonempty.
            text = response.text.strip()
            return text if text else {"error": "Empty text response."}
        else:
            # For other content types, check if the text appears meaningful.
            text = response.text
            if text:
                printable_ratio = sum(1 for c in text if c.isprintable()) / len(text)
                if printable_ratio > 0.9:
                    return text
            return {"error": "Response content is not interpretable as meaningful text."}

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
        self._log_request(method, url, params, headers, json)
        try:
            auth = self._get_auth(url)
            response = requests.request(
                method=method,
                url=url,
                params=params,
                headers=headers,
                json=json,
                auth=auth
            )
            logger.info(f"API Response: {response.status_code} {response.text}")
            content = self._parse_response(response)
            return {"content": content, "status_code": response.status_code}
        except requests.RequestException as e:
            logger.error(f"Failed to send request to {url}: {e}")
            return {"content": {"error": str(e)}, "status_code": 500}

    def close(self):
        if self.token_manager:
            self.token_manager.save_auths(self.auths)
