import threading
from .schedule import Schedule
import time
import requests
from dateutil import parser


class ScheduleManager:

    def __init__(self, callback_url, update_interval=15):
        self.schedule = Schedule()
        self.callback_url = callback_url
        self.update_interval = update_interval
        self.stop_event = threading.Event()
        self.update_thread = threading.Thread(target=self._update_schedule)
        self.update_thread.start()

    def add_schedule(self, time_string, content):
        time_parsed = parser.parse(time_string)
        self.schedule.add(time_parsed, content)

    def _update_schedule(self):
        while not self.stop_event.is_set():
            self._on_schedule_update()
            time.sleep(self.update_interval)

    def _on_schedule_update(self):
        while self.schedule.is_next():
            schedule_time, schedule_content = self.schedule.get_next()
            requests.post(self.callback_url, json={"time": schedule_time.isoformat(), "content": schedule_content})

    def close(self):
        self.schedule.clear()
        self.stop_event.set()
        self.update_thread.join()
