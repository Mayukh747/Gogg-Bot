import os
from datetime import timedelta

import discord
from dotenv import load_dotenv
import requests
import json
import random

from poll import moitozoPoll


# sad_words = ["sad", "depressed", "unhappy", "angry", "miserable", "depressing"]

# starter_encouragements = ["Cheer up!", "Hang in there.", "You are a great person / bot!"]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


load_dotenv(dotenv_path='/Users/mayukh/PycharmProjects/Gogg-Bot/.env')

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
    # elif any(word in msg for word in sad_words):
    #     await message.channel.send(random.choice(starter_encouragements))
    elif msg.startswith('poll'):
        # r = discord.Poll()
        # p = discord.Poll(question='sup', duration=timedelta(hours=168))
        # p.add_answer(text='sup')
        p = moitozoPoll()
        await message.channel.send('Stay Hard!', poll=p)
        # await message.channel.send('What is your favorite food?')
    # await message.channel.send('Stay Hard.')



client.run(os.getenv('TOKEN'))
