from typing import List
from datetime import datetime, timedelta

class Poll:

    def __init__(self):
        self.options = self.generate_poll_options()

    def generate_poll_options(self) -> List:
        def get_next_weekend_dates():
            today = datetime.today()

            #am dumb: don't understand this section
            days_until_saturday = (5 - today.weekday()) % 7
            days_until_sunday = (6 - today.weekday()) % 7

            next_saturday = today + timedelta(days=days_until_saturday)
            next_sunday = today + timedelta(days=days_until_sunday)

            return next_saturday.date(), next_sunday.date()

        sat, sun = get_next_weekend_dates()
        sat = str(sat)[5:]
        sun = str(sun)[5:]

        options = ["SAT " + sat + ": 10 AM",
                   "SAT " + sat + ": 11 AM",
                   "SAT " + sat + ": 12 PM",
                   "SUN " + sun + ": 10 AM",
                   "SUN " + sun + ": 10 AM",
                   "SUN " + sun + ": 12 PM",
                   "SUN " + sun + ": 9:30 AM Ortega Park",
                   "I am UNAVAILABLE this weekend.",
                   "Not sure. I will update my availability soon."]

        return options

p = Poll()
print(p.options)