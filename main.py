import os
from datetime import timedelta
from datetime import datetime as datetimeObj
from pathlib import Path

import discord
from dotenv import load_dotenv
import requests
import json
import random

from BonchonPoll import BonchonPoll


sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

starter_encouragements = ["Sucks to be you.", "Stop being a bitch.", "Stay Hard.", "Do something about it."]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


dotenv_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path)

token = os.getenv("TOKEN")
if not token:
    raise RuntimeError(f"TOKEN not found. Please set TOKEN in {dotenv_path} or your environment.")

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    msg = message.content

    if message.author == client.user:
        return

    new_poll = discord.Poll

    if msg.startswith('wisdom'):
        quote = get_quote()
        await message.channel.send(quote)
    elif any(word in msg for word in sad_words):
         await message.channel.send(random.choice(starter_encouragements))
    elif msg.startswith('poll'):
        # r = discord.Poll()
        # p = discord.Poll(question='sup', duration=timedelta(hours=168))
        # p.add_answer(text='sup')
        p = BonchonPoll()
        await message.channel.send('Stay Hard!', poll=p)
        # await message.channel.send("poll duration " + str(p.duration))
        # await message.channel.send("poll end time " + str(p.duration + datetimeObj.now()))
        # await messagpe.channel.send('What is your favorite food?')
    # await message.channel.send('Stay Hard.')
    elif msg.startswith('pull poll dates'):
        planning_channel = discord.utils.get(message.guild.channels, name='session-planning')
        if planning_channel is None:
            await message.channel.send('Could not find a channel named session-planning.')
            return

        poll_dates = []
        async for m in planning_channel.history(limit=None):
            if m.poll is not None:
                poll_dates.append(m.created_at.strftime('%Y-%m-%d %H:%M UTC'))

        if not poll_dates:
            await message.channel.send('No poll messages found in session-planning.')
        else:
            header = 'Poll message dates in #session-planning:\n'
            chunk = header
            for d in poll_dates:
                line = f'- {d}\n'
                if len(chunk) + len(line) > 2000:
                    await message.channel.send(chunk)
                    chunk = ''
                chunk += line
            if chunk:
                await message.channel.send(chunk)



client.run(token)
