import os
import discord
from dotenv import load_dotenv


load_dotenv(dotenv_path='/Users/mayukh/PycharmProjects/Gogg-Bot/.env')

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    #print(message.content)
    if message.author == client.user:
        return

    if message.content:
        await message.channel.send('Stay Hard.')


client.run(os.getenv('TOKEN'))
