TOKEN = ''

import discord
import json
from subprocess import Popen as cmd, PIPE
from pprint import pprint

client = discord.Client()
@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name="with some code"))

with open('./profane-words/words.json', 'r') as f:
    swearsies = json.load(f)
swearsies = []
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    l = []
    checkit = message.content.lower()
    for x in swearsies:
        if x in checkit:
            l.append(x)
    if len(l) == 1:
        if message.guild != None:
            await message.delete()
        await message.channel.send(f'{message.author.mention} `{l[0]}` is a bad word. No swearsies')
    if len(l) > 1:
        if message.guild != None:
            await message.delete()
        await message.channel.send(f'{message.author.mention} `{", ".join(l)}` are bad words. No swearsies')
    
    # print(message)
    if "Hello" in message.content:
        await message.channel.send("Heyyo")
        return
    if message.content == '.fortune':
        if message.guild != None:
            await message.channel.send(f'{message.author.mention}')
            await message.delete()
        txt = cmd(f'fortune -ae 100% /usr/local/Cellar/fortune/9708/share/games/fortunes/', shell=True, executable='/usr/local/bin/zsh',stdout=PIPE).stdout.read().decode('utf8')
        await message.channel.send(txt)
        return
    if message.content == '.chuck':
        if message.guild != None:
            await message.channel.send(f'{message.author.mention}')
            await message.delete()
        txt = cmd(f'fortune -ae 100% /Users/Nicholas/.oh-my-zsh/plugins/chucknorris/fortunes/chucknorris', shell=True, executable='/usr/local/bin/zsh',stdout=PIPE).stdout.read().decode('utf8')
        await message.channel.send(txt)
        return
    if message.content == '.off':
        if message.guild != None:
            await message.channel.send(f'{message.author.mention}')
            await message.delete()
        txt = cmd(f'fortune -ae 100% /usr/local/Cellar/fortune/9708/share/games/fortunes/off', shell=True, executable='/usr/local/bin/zsh',stdout=PIPE).stdout.read().decode('utf8')
        await message.channel.send(txt)
        return


client.run(TOKEN)