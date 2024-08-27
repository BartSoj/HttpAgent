import heapq
from datetime import datetime
from datetime import timezone
from threading import Lock
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class Schedule:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance.schedule = []
        return cls._instance

    def __len__(self):
        return len(self.schedule)

    def add(self, time, content):
        with self._lock:
            heapq.heappush(self.schedule, (time, content))
            logger.info(f"Added '{content}' to schedule for {time}")

    def get_next(self):
        with self._lock:
            if self.schedule:
                return heapq.heappop(self.schedule)
            return None

    def is_next(self):
        with self._lock:
            if self.schedule:
                current_time = datetime.now(timezone.utc)
                return self.schedule[0][0] < current_time
            return False

    def clear(self):
        with self._lock:
            self.schedule.clear()
