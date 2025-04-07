from typing import List
from datetime import datetime, timedelta

import discord
from discord import PartialEmoji


class moitozoPoll(discord.Poll):

    def __init__(self):
        super().__init__("Ultimate Frisbee @ Moitozo Park", timedelta(days=7), multiple=True)
        self.generate_poll_answers()

    def generate_poll_answers(self) -> None:

        def get_next_weekend_dates():
            today = datetime.today()

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
                   ("SUN " + sun + ": 10 AM", emojis[1]),
                   ("SUN " + sun + ": 12 PM", emojis[1]),
                   ("SUN " + sun + ": 9:30 AM Ortega Park", emojis[2]),
                   ("I am UNAVAILABLE this weekend.", emojis[3]),
                   ("Not sure. I will update my availability soon.", emojis[3])]

        for answer in answers:
            self.add_answer(text=answer[0], emoji=answer[1])
