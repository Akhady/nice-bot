# bot.py
import os

import discord
from dotenv import load_dotenv
from operator import itemgetter

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

data = {}

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    with open("nice_data.json", "w+") as data_file:
        data = json.loads(data_file.read())

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == 'nice':
        add_to_user(message.author)
        await message.channel.send("nice")
    elif message.content == 'Nice':
        add_to_user(message.author)
        await message.channel.send("Nice")
    elif message.content.lower() == 'nice top':
        await message.channel.send(get_top_users())

client.run(TOKEN)


def add_to_user(username):
    if username in data:
        data[username].value += 1
    else:
        data[username] = 1

def save_data():
    with open("nice_data.json", "w+") as data_file:
        data_file.write(json.dumps(data_file))

def get_top_users():
    cnt = 0
    return_value = ""
    tmp = sorted(data, key=lambda x: x[1], reverse=True)
    for key in tmp:
        if cnt > 5:
            break
        else:
            cnt += 1
            return_value += key + ": " + tmp[key] + "\n"
    return return_value

import atexit
atexit.register(save_data())
