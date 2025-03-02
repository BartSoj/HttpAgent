import json
import unittest

from reasoners.openApiReasoner.auth_manager import AuthManager
from reasoners.openApiReasoner.request_manager import RequestManager


class TestRequestManager(unittest.TestCase):
    def create_auth_manager(self):
        api_clients_path = "../../../resources/api_clients/api_clients.json"
        api_tokens_path = "../../../resources/api_clients/api_tokens.json"
        return AuthManager(api_clients_path, api_tokens_path)

    def setUp(self):
        with open("../../../resources/functions/send_api_request.json") as file:
            send_api_request_function_schema = json.load(file)
        token_manager = self.create_auth_manager()
        self.req_manager = RequestManager(send_api_request_function_schema, token_manager)

    def test_get_request(self):
        # Test GET request using httpbin.org.
        url = "https://httpbin.org/get"
        params = {"param1": "value1", "param2": "value2"}
        headers = {"Custom-Header": "HeaderValue"}
        result = self.req_manager.send_request("GET", url, params=params, headers=headers)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status_code"], 200)
        # Verify the response content includes the sent parameters.
        self.assertIn("value1", result["content"])
        self.assertIn("value2", result["content"])

    def test_post_request(self):
        # Test POST request with JSON body.
        url = "https://httpbin.org/post"
        json_body = {"key": "value"}
        headers = {"Content-Type": "application/json"}
        result = self.req_manager.send_request("POST", url, json=json_body, headers=headers)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status_code"], 200)
        # The response should contain the JSON we sent.
        self.assertIn('"key": "value"', result["content"])

    def test_put_request(self):
        # Test PUT request with JSON body.
        url = "https://httpbin.org/put"
        json_body = {"update": "data"}
        result = self.req_manager.send_request("PUT", url, json=json_body)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status_code"], 200)
        self.assertIn('"update": "data"', result["content"])

    def test_delete_request(self):
        # Test DELETE request.
        url = "https://httpbin.org/delete"
        result = self.req_manager.send_request("DELETE", url)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status_code"], 200)
        # Check that the response includes an indicator of the URL.
        self.assertIn("url", result["content"])

    def test_404_response(self):
        # Test a request that returns a 404 status.
        url = "https://httpbin.org/status/404"
        result = self.req_manager.send_request("GET", url)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status_code"], 404)

    def test_request_exception(self):
        # Test that a request exception is handled.
        # Use an invalid URL that will fail DNS resolution.
        url = "http://nonexistent.invalid"
        result = self.req_manager.send_request("GET", url)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status_code"], 500)
        self.assertIsInstance(result["content"], dict)
        self.assertIn("error", result["content"])
        self.assertIsInstance(result["content"]["error"], str)

    def test_spotify_search(self):
        # Test a request to the Spotify API.
        url = "https://api.spotify.com/v1/search"
        params = {"q": "album:Afterlife", "type": "album", "limit": 1}
        result = self.req_manager.send_request("GET", url, params=params)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["status_code"], 200)
        # The response should contain the album url.
        self.assertIn("https://open.spotify.com/album/2xO5zlCGNyap7Jx1ED3HgG", result["content"])

    def tearDown(self):
        self.req_manager.close()
