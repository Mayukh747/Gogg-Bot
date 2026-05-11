import io
import os
from collections import defaultdict
from datetime import timedelta
from datetime import datetime as datetimeObj
from pathlib import Path

import discord
from dotenv import load_dotenv
import requests
import json
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

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
    elif msg.startswith('pull poll results'):
        planning_channel = discord.utils.get(message.guild.channels, name='session-planning')
        if planning_channel is None:
            await message.channel.send('Could not find a channel named session-planning.')
            return

        poll_messages = []
        async for m in planning_channel.history(limit=None):
            if m.poll is not None:
                poll_messages.append(m)

        if not poll_messages:
            await message.channel.send('No poll messages found in session-planning.')
        else:
            header = 'Poll results in #session-planning:\n'
            chunk = header
            for m in poll_messages:
                date = m.created_at.strftime('%Y-%m-%d %H:%M UTC')
                question = m.poll.question
                top_answer = max(m.poll.answers, key=lambda a: a.vote_count, default=None)
                top_text = f'{top_answer.text} ({top_answer.vote_count} votes)' if top_answer else 'N/A'
                line = f'- {date} | {question} | Top: {top_text}\n'
                if len(chunk) + len(line) > 2000:
                    await message.channel.send(chunk)
                    chunk = ''
                chunk += line
            if chunk:
                await message.channel.send(chunk)
    elif msg.startswith('dist'):
        channel_name = msg[len('dist'):].strip()
        target_channel = discord.utils.get(message.guild.channels, name=channel_name)
        if target_channel is None:
            await message.channel.send(f'Could not find a channel named {channel_name}.')
            return

        # Collect (week_start, author) pairs
        week_author_counts = defaultdict(lambda: defaultdict(int))
        async for m in target_channel.history(limit=None):
            created = m.created_at.replace(tzinfo=None)
            week_start = created - timedelta(days=created.weekday())
            week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
            week_author_counts[week_start][m.author.display_name] += 1

        if not week_author_counts:
            await message.channel.send(f'No messages found in #{channel_name}.')
            return

        # Build sorted week list and top authors (by total message count)
        weeks = sorted(week_author_counts.keys())
        total_per_author = defaultdict(int)
        for week_data in week_author_counts.values():
            for author, count in week_data.items():
                total_per_author[author] += count

        # Show top 10 authors to keep the chart readable
        top_authors = sorted(total_per_author, key=total_per_author.get, reverse=True)[:10]

        # Build time-series arrays per author
        series = {author: [week_author_counts[w].get(author, 0) for w in weeks] for author in top_authors}

        # Plot
        fig, ax = plt.subplots(figsize=(12, 6))
        colors = plt.cm.tab10.colors

        for i, author in enumerate(top_authors):
            color = colors[i % len(colors)]
            y = series[author]
            x_numeric = np.arange(len(weeks))

            ax.plot(weeks, y, marker='o', markersize=3, linewidth=1.5,
                    color=color, label=author, alpha=0.85)

            # Trendline (linear regression over numeric x)
            if len(weeks) > 1:
                coeffs = np.polyfit(x_numeric, y, 1)
                trend = np.poly1d(coeffs)(x_numeric)
                ax.plot(weeks, trend, linestyle='--', linewidth=1,
                        color=color, alpha=0.5)

        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d\n%Y'))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator())
        fig.autofmt_xdate(rotation=30)

        ax.set_title(f'Message activity over time in #{channel_name}', fontsize=14, pad=12)
        ax.set_xlabel('Week starting', fontsize=11)
        ax.set_ylabel('Messages sent', fontsize=11)
        ax.legend(loc='upper left', fontsize=8, framealpha=0.7)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.set_ylim(bottom=0)
        fig.tight_layout()

        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=150)
        plt.close(fig)
        buf.seek(0)

        total_messages = sum(total_per_author.values())
        summary_lines = [f'**Message distribution in #{channel_name}** ({total_messages:,} total messages, {len(weeks)} week(s) of data)']
        for author in top_authors:
            pct = total_per_author[author] / total_messages * 100
            summary_lines.append(f'• **{author}**: {total_per_author[author]:,} msgs ({pct:.1f}%)')
        summary = '\n'.join(summary_lines)

        await message.channel.send(summary, file=discord.File(buf, filename='dist.png'))


client.run(token)
