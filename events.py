import discord
import asyncio
import requests
import random
from discord.ext import commands
import sqlite3

with open('Token.txt') as file:
    TOKEN = file.readlines()[0]
client = commands.Bot(command_prefix="-")

ban_words = []
with open('ban_words.txt',encoding='utf8') as bllist:
    for i in bllist.readlines():
        ban_words.append(i)

letters = {'a': 'а', 'o': 'о', 'y': 'у', 'k': 'к', 'о': 'а', 'x': 'х'}


@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Здарова, {member.name}')


@client.event
async def on_message(message):
    if message.channel.id == 806534202781859892:
        await message.delete()


@client.event
async def on_message2(message):
    if message.guild.id != 806257174673883176 and message.author.id != 426407045898436618:
        for i in message.content.lower().strip().split():
            m = ''
            for index in range(len(i)):
                for x, y in letters.items():
                    if i.replace(i[index], x) in ban_words or i.replace(i[index], y) in ban_words:
                        await message.delete()
                        return
                if i[index].isalpha():
                    m += i[index]
            if m in ban_words:
                await message.delete()
    if 'собака' in message.content.lower().split() or 'пёс' in message.content.lower().split():
        request = requests.get('https://dog.ceo/api/breeds/image/random').json()
        await message.channel.send(request['message'])
    elif 'кот' in message.content.lower().split():
        request = requests.get('https://api.thecatapi.com/v1/images/search').json()
        await message.channel.send(request[0]['url'])


@client.event
async def on_member_remove(member):
    if member.id == 426407045898436618:
        member.dm_channel.send(1)


client.run(TOKEN)
