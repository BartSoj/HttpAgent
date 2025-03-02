import unittest
import tempfile
import os
import json
import logging
from datetime import datetime, timezone
from unittest.mock import patch

from reasoners.openApiReasoner.auth_manager import (
    AuthManager,
    CustomPrefixBearerToken
)
from requests_oauth2client import OAuth2AccessTokenAuth

# Disable excessive logging during tests.
logging.disable(logging.CRITICAL)


class TestAuthManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for our test client and token files.
        self.temp_dir = tempfile.TemporaryDirectory()
        self.clients_path = os.path.join(self.temp_dir.name, "clients.json")
        self.tokens_path = os.path.join(self.temp_dir.name, "tokens.json")

        # Write a sample clients file.
        sample_clients = [
            {
                "name": "client1",
                "client_id": "id1",
                "client_secret": "secret1",
                "token_endpoint": "https://example.com/token",
                "authorization_endpoint": "https://example.com/auth",
                "scope": "read"
            }
        ]
        with open(self.clients_path, "w") as f:
            json.dump(sample_clients, f)

        # Write an empty tokens file.
        with open(self.tokens_path, "w") as f:
            json.dump({}, f)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_add_client_token_manually_valid(self):
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        manager.add_client_token_manually("client1", "abc123", expires_at=datetime(2025, 3, 3, tzinfo=timezone.utc))
        with open(self.tokens_path, "r") as f:
            tokens = json.load(f)
        self.assertIn("client1", tokens)
        token = manager.token_serializer.loads(tokens["client1"])
        self.assertEqual(token.access_token, "abc123")

    def test_get_auths(self):
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        # Create a token and write it into tokens file.
        token = CustomPrefixBearerToken("abc123", expires_at=datetime(2025, 3, 3, tzinfo=timezone.utc))
        serialized = manager._serialize_token(token)
        tokens = {"client1": serialized}
        with open(self.tokens_path, "w") as f:
            json.dump(tokens, f)
        auths = manager.get_auths()
        self.assertIn("client1", auths)
        self.assertEqual(auths["client1"].token.access_token, "abc123")

    def test_save_auths(self):
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        token = CustomPrefixBearerToken("abc123", expires_at=datetime(2025, 3, 3, tzinfo=timezone.utc))
        auth_client = manager._create_auth_client(json.load(open(self.clients_path))[0])
        auth = OAuth2AccessTokenAuth(auth_client, token)
        auths = {"client1": auth}
        manager.save_auths(auths)
        with open(self.tokens_path, "r") as f:
            tokens = json.load(f)
        self.assertIn("client1", tokens)
        loaded_token = manager.token_serializer.loads(tokens["client1"])
        self.assertEqual(loaded_token.access_token, "abc123")

    def test_token_serialization(self):
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        original_token = CustomPrefixBearerToken("abc123", expires_at=datetime(2025, 3, 3, tzinfo=timezone.utc),
                                                 scope="read")
        serialized = manager._token_dumper(original_token)
        loaded_token = manager._token_loader(serialized)
        self.assertEqual(loaded_token.access_token, original_token.access_token)
        self.assertEqual(loaded_token.scope, original_token.scope)
        self.assertEqual(loaded_token.prefix, original_token.prefix)
        self.assertEqual(loaded_token.authorization_header(), f"{original_token.prefix} {original_token.access_token}")

    def test_create_auth_client(self):
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        with open(self.clients_path, "r") as f:
            clients = json.load(f)
        client = clients[0]
        auth_client = manager._create_auth_client(client)
        self.assertEqual(auth_client.client_id, client["client_id"])
        self.assertEqual(auth_client.client_secret, client["client_secret"])
        self.assertEqual(auth_client.token_endpoint, client["token_endpoint"])
        self.assertEqual(auth_client.authorization_endpoint, client["authorization_endpoint"])
        self.assertEqual(auth_client.redirect_uri, f"http://localhost:{manager.port}/callback")

    def test_create_authorization_request(self):
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        dummy_client = {
            "name": "dummy",
            "client_id": "dummy_id",
            "client_secret": "dummy_secret",
            "token_endpoint": "http://dummy/token",
            "authorization_endpoint": "http://dummy/auth",
            "scope": "dummy_scope",
            "request_params": {"param1": "value1"}
        }

        class DummyAuthClient:
            def authorization_request(self, **params):
                return params

        dummy_auth_client = DummyAuthClient()
        auth_request = manager._create_authorization_request(dummy_client, dummy_auth_client)
        expected_params = {"scope": "dummy_scope", "access_type": "offline", "param1": "value1"}
        self.assertEqual(auth_request, expected_params)

    def test_get_authorization_code(self):
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)

        class DummyHTTPD:
            def __init__(self):
                self.callback_uri = None
                self.calls = 0

            def handle_request(self):
                self.calls += 1
                if self.calls == 1:
                    self.callback_uri = "dummy_callback"

        dummy_httpd = DummyHTTPD()
        with patch("webbrowser.open") as mock_browser:
            result = manager._get_authorization_code("http://dummy_auth", dummy_httpd)
            mock_browser.assert_called_once_with("http://dummy_auth")
            self.assertEqual(result, "dummy_callback")

    def test_retrieve_token(self):
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        dummy_client = {
            "name": "client1",
            "client_id": "id1",
            "client_secret": "secret1",
            "token_endpoint": "http://example.com/token",
            "authorization_endpoint": "http://example.com/auth",
            "scope": "read"
        }

        class DummyHTTPD:
            callback_uri = "dummy_callback"

            def handle_request(self):
                pass

        dummy_httpd = DummyHTTPD()

        with patch.object(manager, "_get_authorization_code", return_value="dummy_callback"):
            class DummyAuthClient:
                def authorization_request(self, **params):
                    # Return a dummy request object.
                    return type("DummyAuthRequest", (), {
                        "uri": "http://dummy_auth",
                        "validate_callback": lambda self, uri: {"code": "dummy_code"}
                    })()

                def authorization_code(self, az_response):
                    # Return a dummy token.
                    return CustomPrefixBearerToken("dummy_access_token",
                                                   expires_at=datetime(2025, 3, 3, tzinfo=timezone.utc))

            with patch.object(manager, "_create_auth_client", return_value=DummyAuthClient()):
                serialized_token = manager._retrieve_token(dummy_client, dummy_httpd)
                token = manager.token_serializer.loads(serialized_token)
                self.assertEqual(token.access_token, "dummy_access_token")

    def test_load_clients_missing_name(self):
        # Prepare a clients file missing the 'name' key.
        invalid_clients = [{"client_id": "id1", "client_secret": "secret1"}]
        with open(self.clients_path, "w") as f:
            json.dump(invalid_clients, f)
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        with self.assertRaises(ValueError):
            manager._load_clients()

    def test_load_clients_missing_client_id(self):
        invalid_clients = [{"name": "client1", "client_secret": "secret1"}]
        with open(self.clients_path, "w") as f:
            json.dump(invalid_clients, f)
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        with self.assertRaises(ValueError):
            manager._load_clients()

    def test_load_tokens_file_not_found(self):
        os.remove(self.tokens_path)
        manager = AuthManager(self.clients_path, self.tokens_path, port=8888)
        tokens = manager._load_tokens()
        self.assertEqual(tokens, {})
