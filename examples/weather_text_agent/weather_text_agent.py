from agents.textAgent.text_agent import TextAgent
from reasoners.functionReasoner.functionReasoner import FunctionReasoner
from functions import functions


def main():
    function_spec_paths = ["examples/weather_text_agent/functions/get_weather.json"]
    function_reasoner = FunctionReasoner(function_spec_paths=function_spec_paths, functions=functions)

    request_action_function_path = "resources/functions/request_action.json"
    text_agent = TextAgent(reasoner=function_reasoner, request_action_function_path=request_action_function_path)

    text_agent.start()


if __name__ == "__main__":
    main()
