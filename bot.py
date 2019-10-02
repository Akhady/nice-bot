# bot.py
import os
import json

import discord
from dotenv import load_dotenv
from operator import itemgetter

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()

niceCooldown = False

data = []
with open("nice_data.json", "r+") as data_file:
        data = json.loads(data_file.read())

def get_top_users():
    cnt = 0
    return_value = ""
    tmp = sorted(data, key=lambda x: x['value'], reverse=True)
    for i in tmp:
        if cnt > 5:
            break
        else:
            cnt += 1
            return_value += i['nick'] + ": " + str(i["value"]) + "\n"
    return return_value


def add_to_user(userId, userNick):
    for i in range(len(data)):
        if data[i]['userId'] == userId:
            data[i]['value'] += 1
            data[i]['nick'] = userNick
            return
    data.append({'userId': userId, 'nick': userNick, 'value': 1})

def save_data():
    with open("nice_data.json", "w+") as data_file:
        data_file.write(json.dumps(data))

import atexit
atexit.register(save_data)

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')
    

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() != 'nice':
        # any message that is not nice
        niceCooldown = False

    if message.content == 'Nice' and not niceCooldown:
        add_to_user(message.author.id, message.author.nick)
        niceCooldown = True
        await message.channel.send("Nice")
    elif message.content.lower() == 'nice' and not niceCooldown:
        add_to_user(message.author.id, message.author.nick)
        niceCooldown = True
        await message.channel.send("nice")
    elif message.content.lower() == 'nice top':
        await message.channel.send(get_top_users())


    # must be the last elif
    elif "nice" in message.content.lower():
        add_to_user(message.author.id, message.author.nick)

    

client.run(TOKEN)

