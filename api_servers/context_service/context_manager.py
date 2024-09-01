from datetime import datetime
import threading
import time
import geocoder
import logging

logging.getLogger("geocoder").setLevel(logging.ERROR)


class ContextManager:
    def __init__(self, update_interval=15):
        self.context = {}
        self.update_interval = update_interval
        self.stop_event = threading.Event()
        self.update_thread = threading.Thread(target=self._update_context_loop)
        self.update_thread.start()

    def _update_context_loop(self):
        while not self.stop_event.is_set():
            self._on_context_update()
            time.sleep(self.update_interval)

    def _on_context_update(self):
        self.context["date"] = datetime.now().strftime("%d-%m-%Y")
        self.context["time"] = datetime.now().strftime("%H:%M:%S")
        self.context["city"] = geocoder.ip('me').city

    def get_date(self):
        return self.context["date"]

    def get_time(self):
        return self.context["time"]

    def get_city(self):
        return self.context["city"]

    def close(self):
        self.stop_event.set()
        self.update_thread.join()
