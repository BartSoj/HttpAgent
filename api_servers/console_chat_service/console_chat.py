import threading

import requests


class ConsoleChat:

    def __init__(self, user_name, agent_name, agent_url):
        self.user_name = user_name
        self.agent_name = agent_name
        self.agent_url = agent_url
        self.stop_event = threading.Event()
        self.user_input_thread = threading.Thread(target=self._run)
        self.user_input_thread.start()

    def print_answer(self, content):
        print(f"\n## {self.agent_name}")
        print("-" * (len(self.agent_name) + 3))
        print(content)
        print()

    def _get_user_input(self):
        print(f"\n## {self.user_name}")
        print("-" * (len(self.user_name) + 3))
        user_input = input()
        print()
        return user_input

    def _run(self):
        self.stop_event.wait(1)
        while not self.stop_event.is_set():
            user_input = self._get_user_input()
            if user_input == "exit":
                break
            response = requests.post(self.agent_url, json={"user_request": user_input})

    def set_user_name(self, user_name):
        self.user_name = user_name

    def set_agent_name(self, agent_name):
        self.agent_name = agent_name

    def close(self):
        self.stop_event.set()
        self.user_input_thread.join(1)
