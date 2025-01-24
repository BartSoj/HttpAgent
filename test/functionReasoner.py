import unittest
from src.functionReasoner.functionReasoner import FunctionReasoner


class FunctionReasonerTest(unittest.TestCase):

    def test_weather_function(self):
        function_spec_paths = ["functions/get_weather.json"]
        get_weather_function = lambda latitude, longitude: 1
        functions = {
            "get_weather": get_weather_function
        }
        function_reasoner = FunctionReasoner(function_spec_paths=function_spec_paths, functions=functions)

        request = "What is the weather in London?"
        response = function_reasoner.process_request(request)
        self.assertIn("1", response)
