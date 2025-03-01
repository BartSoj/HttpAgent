import unittest

from reasoners.functionReasoner.function_reasoner import FunctionReasoner


class FunctionReasonerTest(unittest.TestCase):

    def setUp(self):
        function_spec_paths = ["functions/get_weather.json"]
        get_weather_function = lambda latitude, longitude: "The temperature is 1 degree"
        functions = {
            "get_weather": get_weather_function
        }
        self.function_reasoner = FunctionReasoner(function_spec_paths=function_spec_paths, functions=functions)

    def test_weather_function(self):
        request = "What is the weather in London?"
        response = self.function_reasoner.process_request(request)
        self.assertIn("1", response)
