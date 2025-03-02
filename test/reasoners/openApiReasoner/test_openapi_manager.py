import unittest
import os
import tempfile
import json
from typing import Dict
from reasoners.openApiReasoner.openapi_manager import OpenapiManager


class OpenapiManagerTest(unittest.TestCase):
    def setUp(self):
        # Create temporary files for various test cases.
        self.temp_files: Dict[str, str] = {}

        # Valid API content for list and get tests.
        valid_api_content = {
            "paths": {
                "/endpoint1": {
                    "get": {
                        "operationId": "op1",
                        "summary": "Summary 1\n"
                    },
                    "post": {
                        "operationId": "op2",
                        "description": "Description 2"
                    }
                },
                "/endpoint2": {
                    "delete": {
                        "operationId": "op3",
                        "summary": "Summary 3"
                    }
                }
            },
            "servers": [{"url": "http://api.example.com"}]
        }
        self.temp_files["valid_api"] = self._create_temp_file(valid_api_content)

        # API with missing operationId to trigger error in list.
        missing_opid_content = {
            "paths": {
                "/endpoint1": {
                    "get": {
                        "summary": "Summary missing opId"
                    }
                }
            }
        }
        self.temp_files["missing_opid"] = self._create_temp_file(missing_opid_content)

        # API with no servers defined; should default to "http://localhost" for get.
        no_servers_content = {
            "paths": {
                "/endpoint1": {
                    "get": {
                        "operationId": "op1",
                        "parameters": [{"name": "param1"}]
                    }
                }
            },
            "servers": []
        }
        self.temp_files["no_servers"] = self._create_temp_file(no_servers_content)

        # API for get operation test with additional operation details.
        get_api_content = {
            "paths": {
                "/endpoint1": {
                    "get": {
                        "operationId": "op1",
                        "parameters": [{"name": "param1"}],
                        "requestBody": {"content": "example"}
                    }
                },
                "/endpoint2": {
                    "post": {
                        "operationId": "op2",
                        "parameters": [{"name": "param2"}]
                    }
                }
            },
            "servers": [{"url": "http://api.example.com"}]
        }
        self.temp_files["get_api"] = self._create_temp_file(get_api_content)

    def tearDown(self):
        # Clean up temporary files.
        for path in self.temp_files.values():
            try:
                os.remove(path)
            except OSError:
                pass

    def _create_temp_file(self, content: dict) -> str:
        temp = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
        json.dump(content, temp)
        temp.close()
        return temp.name

    # --- Tests for list_operation_ids_and_summaries ---

    def test_list_operation_ids_and_summaries_valid(self):
        openapi_files = {"validapi": self.temp_files["valid_api"]}
        manager = OpenapiManager({"function": {"name": "list_op"}}, {"function": {"name": "get_op"}}, openapi_files)
        result = manager.list_operation_ids_and_summaries("ValidApi")
        # Expected behavior:
        # - The newline in "Summary 1\n" is stripped.
        # - If 'summary' is missing, it uses 'description'.
        expected = [
            {"operationId": "op1", "summary": "Summary 1"},
            {"operationId": "op2", "summary": "Description 2"},
            {"operationId": "op3", "summary": "Summary 3"}
        ]
        # Sorting to avoid order issues.
        result_sorted = sorted(result, key=lambda x: x["operationId"])
        expected_sorted = sorted(expected, key=lambda x: x["operationId"])
        self.assertEqual(result_sorted, expected_sorted)

    def test_list_operation_ids_and_summaries_api_not_found(self):
        openapi_files = {"someapi": self.temp_files["valid_api"]}
        manager = OpenapiManager({"function": {"name": "list_op"}}, {"function": {"name": "get_op"}}, openapi_files)
        with self.assertRaises(ValueError) as context:
            manager.list_operation_ids_and_summaries("NonExistentAPI")
        self.assertIn("API NonExistentAPI not found", str(context.exception))

    def test_list_operation_ids_and_summaries_missing_operationId(self):
        openapi_files = {"missingopid": self.temp_files["missing_opid"]}
        manager = OpenapiManager({"function": {"name": "list_op"}}, {"function": {"name": "get_op"}}, openapi_files)
        with self.assertRaises(ValueError) as context:
            manager.list_operation_ids_and_summaries("MissingOpid")
        self.assertIn("OperationId not found", str(context.exception))

    # --- Tests for get_operation_by_id ---

    def test_get_operation_by_id_valid(self):
        openapi_files = {"getapi": self.temp_files["get_api"]}
        manager = OpenapiManager({"function": {"name": "list_op"}}, {"function": {"name": "get_op"}}, openapi_files)
        result = manager.get_operation_by_id("GetApi", "op2")
        expected = {
            "path": "http://api.example.com/endpoint2",
            "method": "POST",
            "details": {
                "operationId": "op2",
                "parameters": [{"name": "param2"}]
            }
        }
        self.assertEqual(result, expected)

    def test_get_operation_by_id_no_servers(self):
        openapi_files = {"noservers": self.temp_files["no_servers"]}
        manager = OpenapiManager({"function": {"name": "list_op"}}, {"function": {"name": "get_op"}}, openapi_files)
        result = manager.get_operation_by_id("NoServers", "op1")
        expected = {
            "path": "http://localhost/endpoint1",
            "method": "GET",
            "details": {
                "operationId": "op1",
                "parameters": [{"name": "param1"}]
            }
        }
        self.assertEqual(result, expected)

    def test_get_operation_by_id_api_not_found(self):
        openapi_files = {"someapi": self.temp_files["get_api"]}
        manager = OpenapiManager({"function": {"name": "list_op"}}, {"function": {"name": "get_op"}}, openapi_files)
        with self.assertRaises(ValueError) as context:
            manager.get_operation_by_id("NonExistentAPI", "op1")
        self.assertIn("API NonExistentAPI not found", str(context.exception))

    def test_get_operation_by_id_operationId_not_found(self):
        openapi_files = {"getapi": self.temp_files["get_api"]}
        manager = OpenapiManager({"function": {"name": "list_op"}}, {"function": {"name": "get_op"}}, openapi_files)
        with self.assertRaises(ValueError) as context:
            manager.get_operation_by_id("GetApi", "nonexistent")
        self.assertIn("OperationId not found", str(context.exception))

    def test_get_operation_by_id_file_not_found(self):
        openapi_files = {"nonexistent": "/path/to/nonexistent/file.json"}
        manager = OpenapiManager({"function": {"name": "list_op"}}, {"function": {"name": "get_op"}}, openapi_files)
        with self.assertRaises(FileNotFoundError):
            manager.get_operation_by_id("Nonexistent", "op1")
