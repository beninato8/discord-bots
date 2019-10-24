import discord
from discord.ext import tasks
from discord.ext.commands import Bot
import re
import json
import asyncio
from pprint import pprint

with open('tokens.json', 'r') as f:
    d = json.load(f)
TOKEN = d['birch']
client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name="In̸̛̕ ͘͘a͠n̸̕ò̴̀th͠e̢̢̢ŗ͠ ̷d͏̀i̡̛m̶e̕͠n̸s̷̵̵į̴on"))
import random

def ht():
    return f'{0.51 - (random.random()/10) + .05:.2f}'

def wt():
    return f'{5 - (random.random()) + .5:.2f}'

base = 'https://raw.githubusercontent.com/ZeChrales/PogoAssets/master/pokemon_icons/pokemon_icon_201_'
end = '_shiny.png'
d = {"A":11,
"B":12,
"C":13,
"D":14,
"E":15,
"G":17,
"H":18,
"I":19,
"J":20,
"K":21,
"L":22,
"M":23,
"N":24,
"O":25,
"P":26,
"Q":27,
"R":28,
"S":29,
"T":30,
"U":31,
"V":32,
"W":33,
"X":34,
"Y":35,
"Z":36,
"!":37,
"?":38}
def unown(s):
    return f'{base}{d[s.upper()]}{end}'

letters = list('goodbye')
import time

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.guild == None:
        time.sleep(5)
        for x in letters:
            # file = discord.File(f"/Users/Nicholas/Desktop/dim.png", filename=f"dim.png")
            embed = discord.Embed(description=f"", color=0xF85888, title=f'**Unown {x.upper()}** 15/15/15 (100%)', url=f'')
            nl = '\n'
            embed.add_field(name='Level 40 | CP 1185', value=f'Ht: {ht()}m | Wt: {wt()}kg | normal{nl}Hidden Power / Struggle <:type_normal:636990893110591516>', inline=False)
            embed.add_field(name='<:check:636991535048556544> | ??:?? (00m ∞s)', value='<:type_psychic:636990893290815513> Psychic', inline=False)
            embed.add_field(name='null_location | Directions:', value='[Google Map](https://google.com) | [Apple Map](https://google.com) | [MadPoGoMap](https://google.com)', inline=False)
            embed.set_thumbnail(url=f"{unown(x)}")
            embed.set_image(url=f"https://i.imgur.com/eApFfxr.png")
            # await message.channel.send(file=file, embed=embed)
            time.sleep(2)
            await message.channel.send(embed=embed)

client.run(TOKEN)