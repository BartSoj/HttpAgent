import logging
import threading
from schedule import Schedule

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Core:

    def __init__(self, reasoner):
        self.reasoner = reasoner
        self.schedule = Schedule()
        self.running = True
        self.lock = threading.Lock()

    def print_messages(self):
        messages = self.reasoner.list_messages()
        for message in reversed(messages):
            role = message.role.capitalize()
            content = message.content[0].text.value
            print(f"\n## {role}")
            print("-" * (len(role) + 3))
            print(content)
            print()

    def process_input(self, message_type, user_input):
        with self.lock:
            run = self.reasoner.send_message(message_type, user_input)

            while run.required_action:
                run = self.reasoner.handle_actions(run)

            if run.status == 'completed':
                self.print_messages()
            else:
                logger.error("actions executed, but run is not completed")
                self.print_messages()

    def user_input_thread(self):
        while self.running:
            user_input = input("You: ")
            if user_input == "exit":
                self.running = False
                break
            self.process_input("user message", user_input)

    def schedule_event_thread(self):
        while self.running:
            while self.schedule.is_next():
                content = self.schedule.get_next()[1]
                self.process_input("schedule event", content)

    def start(self):
        try:
            input_thread = threading.Thread(target=self.user_input_thread)
            event_thread = threading.Thread(target=self.schedule_event_thread)
            input_thread.start()
            event_thread.start()
            input_thread.join()
            event_thread.join()
        finally:
            self.reasoner.close()
