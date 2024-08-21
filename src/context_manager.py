from datetime import datetime
import json
import geocoder
import threading
import time


class ContextManager:

    def __init__(self, update_interval=60):
        self.context = ""
        self.context_dict = {}
        self.update_interval = update_interval
        self.stop_event = threading.Event()
        self.update_thread = threading.Thread(target=self._update_context_loop)
        self.update_thread.start()

    def _update_context_loop(self):
        while not self.stop_event.is_set():
            self.on_context_update()
            time.sleep(self.update_interval)

    def on_context_update(self):
        self.context_dict["date"] = datetime.now().strftime("%d-%m-%Y")
        self.context_dict["time"] = datetime.now().strftime("%H:%M:%S")
        self.context_dict["city"] = geocoder.ip('me').city
        self.context = json.dumps(self.context_dict)

    def get_context(self):
        return self.context

    def close(self):
        self.stop_event.set()
        self.update_thread.join()
