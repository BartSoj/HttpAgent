import json

from agents.textAgent.text_agent import TextAgent
from reasoners.functionReasoner.function_reasoner import FunctionReasoner
from functions import functions


def main():
    function_spec_paths = ["functions/get_weather.json"]
    function_reasoner = FunctionReasoner(function_spec_paths=function_spec_paths, functions=functions)
    with open("../../resources/instructions/text_agent_instructions_v1.txt") as file:
        instructions = file.read()
    with open("../../resources/functions/request_action.json") as f:
        request_action_function_schema = json.load(f)

    text_agent = TextAgent(instructions=instructions,
                           reasoner=function_reasoner,
                           request_action_function_schema=request_action_function_schema)

    text_agent.start()


if __name__ == "__main__":
    main()
