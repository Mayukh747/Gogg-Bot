from typing import List
from datetime import datetime, timedelta

import discord
from discord import PartialEmoji


class MoitozoPoll(discord.Poll):

    def __init__(self):


        #todo: wait, this is bs, I don't need this if I setup the poll at the same day it closes.
        # Let's just do both setup and teardown on fridays
        def compute_poll_duration(today: datetime) -> timedelta:
            # Calculate the number of days until the next Friday (weekday 4)
            # todo: redundant calculations for 'days_until', is there some kind of calendar
            #  we can use instead to make this cleaner?
            days_until_friday = (4 - today.weekday() + 7) % 7
            if days_until_friday == 0:  # If today is Friday, schedule for next week's Friday
                days_until_friday = 7
            next_friday = today + timedelta(days=days_until_friday)

            # Set the time to 6 PM
            next_friday_6pm = next_friday.replace(hour=18, minute=0, second=0, microsecond=0)
            return next_friday_6pm - today

        poll_duration = compute_poll_duration(datetime.today())
        print(poll_duration)
        super().__init__("Ultimate Frisbee @ Live Oak Park", poll_duration, multiple=True)
        self.generate_poll_answers()

    def generate_poll_answers(self) -> None:

        def get_next_weekend_dates():
            today = datetime.today() + timedelta(days=2)

            # todo: understand the modular arithmetic
            days_until_saturday = (5 - today.weekday()) % 7
            days_until_sunday = (6 - today.weekday()) % 7

            next_saturday = today + timedelta(days=days_until_saturday)
            next_sunday = today + timedelta(days=days_until_sunday)

            return next_saturday.date(), next_sunday.date()

        sat, sun = get_next_weekend_dates()
        sat = str(sat)[5:]
        sun = str(sun)[5:]

        emojis = ["\U0001F353","\U0001FAD0","\U0001F350","\U0001F34C"]
        emojis = [PartialEmoji.from_str(emoji_str) for emoji_str in emojis]
        # emojis = [discord.PartialEmoji()]
        answers = [("SAT " + sat + ": 10 AM", emojis[0]),
                   ("SAT " + sat + ": 11 AM", emojis[0]),
                   ("SAT " + sat + ": 12 PM", emojis[0]),
                   ("SUN " + sun + ": 10 AM", emojis[1]),
                   ("SUN " + sun + ": 11 AM", emojis[1]),
                   ("SUN " + sun + ": 12 PM", emojis[1]),
                   ("I may show up for moral support.", emojis[2]),
                   ("I am UNAVAILABLE this weekend.", emojis[3]),
                   ("Not sure. I will update my availability soon.", emojis[3])]

        for answer in answers:
            self.add_answer(text=answer[0], emoji=answer[1])
