from src.functionReasoner.functionReasoner import FunctionReasoner
from functions import functions


def main():
    function_spec_paths = ["functions/get_weather.json"]
    function_reasoner = FunctionReasoner(function_spec_paths=function_spec_paths, functions=functions)

    while True:
        request = input("Ask me about weather forecast: ")
        response = function_reasoner.process_request(request)
        print(response)


if __name__ == '__main__':
    main()
