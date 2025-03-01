import json
import unittest

from agents.httpAgent.http_agent import HttpAgent
from reasoners.generic_reasoner import GenericReasoner


class MockReasoner(GenericReasoner):
    def process_request(self, request):
        print("reasoner request:", request)
        return input("reasoner response: ")


class HttpAgentTest(unittest.TestCase):

    def test_http_agent(self):
        with open("../../../resources/instructions/http_agent_instructions_v1.txt", "r") as file:
            agent_instructions = file.read()
        with open("../../../resources/functions/request_action.json") as file:
            request_action_function_schema = json.load(file)
        reasoner = MockReasoner()
        text_agent = HttpAgent(
            instructions=agent_instructions,
            reasoner=reasoner,
            request_action_function_schema=request_action_function_schema
        )
        text_agent.start()
        self.assertEqual(input("Pass test? (y/n)"), "y")
