import discord
import asyncio
import requests
import random
from discord.ext import commands
import sqlite3
from time import sleep
import codecs

with open('Token.txt') as file:
    TOKEN = file.readline()
client = commands.Bot(command_prefix=".")

gods = []
with open('god.txt') as bllist:
    for i in bllist.readlines():
        gods.append(int(i.strip().split('-')[0]))

bl = []
with open('black_list.txt',encoding='utf8') as bll:
    for i in bll.readlines():
        bl.append(int(i.strip().split('-')[0]))


@client.command(name='server_name')
async def name(ctx, *new_name):
    nm = ''
    for i in new_name:
        nm += f'{str(i)} '
    await ctx.guild.edit(name=nm)
    await ctx.channel.purge(limit=1)


@client.command(name='randint')
async def my_randint(ctx, min_int, max_int):
    num = random.randint(int(min_int), int(max_int))
    await ctx.send(num)


@client.command()
async def server(ctx):
    serv_name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    region = str(ctx.guild.region)
    member_count = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=serv_name + " server info",
        description=description,
        color=discord.Color.red()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name='boss', value=owner, inline=True)
    embed.add_field(name='Родина', value=region, inline=True)
    embed.add_field(name='Количество', value=member_count, inline=True)

    await ctx.send(embed=embed)


@client.command(name='dmspam')
async def dmspam(ctx, user: discord.Member, count, *message):
    await ctx.channel.purge(limit=1)
    stroka = ''
    for i in message:
        stroka += f'{i} '
    for i in range(int(count)):
        await user.send(stroka)


@client.command(name='spam')
async def spam(ctx, count, *message):
    if int(count) < 31 or ctx.message.author.id == 426407045898436618:
        await ctx.channel.purge(limit=1)
        stroka = ''
        for i in message:
            stroka += f'{i} '
        for index in range(int(count)):
            await ctx.send(stroka)
    else:
        await ctx.send('Не так много')


@client.command(name='kick')
async def kick(ctx, member: discord.Member, delay: int = 0):
    if member.id == 426407045898436618:
        await ctx.send('Ты не знаешь с кем связался.')
    else:
        if ctx.message.author.id not in gods:
            await ctx.send('Заказ принят')
            sleep(delay)
            await ctx.channel.purge(limit=1)
            await ctx.send(f'Время истекло, {member}')
            await member.kick()
        else:
            await ctx.send('Ты нуб')


@client.command(name='sex')
async def sex(ctx):
    await ctx.send(
        'Добавить меня на свой сервер можно по ссылке: \n\
https://discord.com/api/oauth2/authorize?client_id=817809263212363786&permissions=8&scope=bot')


@client.command(name='anekdot')
async def anekdot(ctx):
    con = sqlite3.connect("anekdot.db")
    cur = con.cursor()
    text = str(cur.execute('''
    SELECT text FROM anek
        WHERE id = ?
    ''', (random.randint(0, 130000),)).fetchall()[0][0])
    my_string = codecs.escape_decode(text)[0].decode('unicode-escape')
    my_string = my_string.encode('latin1').decode('unicode-escape').encode('latin1').decode('utf8')

    await ctx.send(my_string)


@client.command(name='role')
async def addrole(ctx, role: discord.Role, member: discord.Member):
    if ctx.author.id in gods:
        await member.add_roles(role, reason='проплаченный')
        await ctx.channel.purge(limit=1)
    else:
        await ctx.send('Ты нуб')


@client.command(name='ban')
async def ban(ctx):
    guilt = client.get_guild(ctx.guild.id)
    for i in guilt.members:
        print(i.id)
        if i.id in bl:
            i.kick()


@client.command(name='remove_role')
async def remove_role(ctx, role: discord.Role, member: discord.Member):
    if member.id in gods:
        await member.remove_roles(role, reason='ГГ')
        await ctx.channel.purge(limit=1)
    else:
        await ctx.send('Ты нуб')


@client.command(name='all_roles')
async def prikol(ctx):
    await ctx.send(list(ctx.guild.roles))


@client.command(name='cl')
async def clear(ctx, number: int):
    if ctx.message.author.id not in bl:
        await ctx.channel.purge(limit=number)


@client.command(name='team')
async def team(ctx):
    teams = ['террористы', 'контртеррористы']
    await ctx.send(teams[random.randint(0, 1)])


client.run(TOKEN)
