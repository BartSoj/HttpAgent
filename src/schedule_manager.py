from schedule import Schedule
from dateutil import parser


class ScheduleManager:

    def __init__(self):
        self.schedule = Schedule()

    def add_schedule(self, time_string, content):
        time = parser.parse(time_string)
        self.schedule.add(time, content)

    def close(self):
        self.schedule.clear()
