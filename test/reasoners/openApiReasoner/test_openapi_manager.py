import unittest

from reasoners.openApiReasoner.openapi_manager import OpenapiManager


class OpenapiManagerTest(unittest.TestCase):
    openapi_file_paths = {"wolframalpha": "../../../resources/apis/wolfram_openapi.json",
                          "discord": "../../../resources/apis/discord_openapi.json",
                          "calendar": "../../../resources/apis/calendar_openapi.json",
                          "tasks": "../../../resources/apis/tasks_openapi.json",
                          "spotify": "../../../resources/apis/spotify_openapi.json"}
    mock_function = {"function": {"name": "mock_function"}}
    openapi_manager = OpenapiManager(mock_function, mock_function, openapi_file_paths)

    def test_get_operation_ids_and_summaries(self):
        operation_ids_and_summaries = self.openapi_manager.list_operation_ids_and_summaries("Wolfram Alpha")
        print(operation_ids_and_summaries)

    def test_get_operation_by_id(self):
        operation_by_id = self.openapi_manager.get_operation_by_id("Wolfram Alpha", "get-result")
        print(operation_by_id)


if __name__ == '__main__':
    unittest.main()
