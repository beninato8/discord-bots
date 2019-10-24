import discord
from discord.ext import tasks
from discord.ext.commands import Bot
import re
import json
import asyncio
from os import listdir
from os.path import isfile, join
from insta import *
from operator import itemgetter
from pprint import pprint

browser, s = login()

with open('swearsies.json', 'r') as f:
    swearsies = json.load(f)

emojis = {'spacer':'⬛',
          'likes':'❤',
          'comments':'🗨'}

for i in range(0, 10):
    emojis[str(i)] = f"{str(i)}\N{COMBINING ENCLOSING KEYCAP}"

TOKEN = ""
client = discord.Client()
mypath = './instagram/'
GUILD = client.get_guild(617845288568094869)
all_feeds = {617909777451712537:'csl_uwmadison', 618242027557224449:'uw_studentlife', 618253261635452938:'uwmadison', 618334262755590144:'UWMadison'}
twitters = [618334262755590144, 618510937032359937]
all_roles = {617909777451712537:'csl-instagram', 618242027557224449:'student-life-instagram', 618253261635452938:'uw-instagram', 618334262755590144:'uw-twitter'}


def get_instagram_files(account):
    get_photos(f'https://www.instagram.com/{account}/', browser, s)
    onlyfiles = [f for f in listdir(f'{mypath}/{account}') if isfile(join(f'{mypath}/{account}', f)) and '.json' in f]
    l = []
    for x in onlyfiles:
        with open(f'{mypath}{account}/{x}', 'r') as f:
            l.append(json.load(f))
    l = sorted(l, key=itemgetter('timestamp')) 
    return l

PAUSE_FEED = False
PAUSE_FEED = True
CLEAR_MESSAGES = False
# CLEAR_MESSAGES = True
blacklist = [617909777451712537, 
             618242027557224449, 
             618253261635452938]
blacklist = []

async def clear(channel):
    PAUSE_FEED = True
    async for x in channel.history(limit=None):
        await x.delete()
        await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even
    PAUSE_FEED = False


@tasks.loop(seconds=30)
async def cleaner():
    for feed in all_feeds.keys():
        if feed not in blacklist:
            channel = client.get_channel(feed)
            async for x in channel.history(limit=None):
                if not x.embeds:
                    await x.delete()
                if CLEAR_MESSAGES and feed not in twitters:
                    await x.delete()
                    # await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even

def get_post_id(message):
    if message.embeds:
        return message.embeds[0].url.replace('https://instagram.com/p/', '')
    return None

@tasks.loop(minutes=60)
async def loop_it():
    if not CLEAR_MESSAGES and not PAUSE_FEED:
        for feed, account in all_feeds.items():
            if feed not in twitters:
                channel = client.get_channel(feed)

                files = get_instagram_files(account)

                msgs = channel.history(limit=None)

                history = []
                async for x in msgs:
                    history.append(x)
                if len(history) < len(files):
                    history_ids = [get_post_id(x) for x in history]
                    file_ids = [x['page_id'] for x in files]
                    missing = [x for x in file_ids if x not in history_ids]
                    for x in missing:
                        await send_post(channel, x)
    # print(len(history), len(files))

    # await csl_insta.send('test')

@client.event
async def on_ready():
    print("The bot is ready!")
    await client.change_presence(activity=discord.Game(name="Robo Overlord"))
    loop_it.start()
    cleaner.start()

def num_format(num, s):
    if num == 1:
        return f'{num} {s}'
    return f'{num} {s}s'

async def send_post(channel, filename):
    # filename = 'B1cqx0WnRg-'
    base = mypath + all_feeds[channel.id] + '/'
    with open(f'{base}{filename}.json', 'r') as f:
        d = json.load(f)

    file = discord.File(f"{base}{filename}.jpg", filename=f"{filename}.jpg")
    embed = discord.Embed(description=f"{d['caption']}", color=0xFF00FF, title=f'', url=f'https://instagram.com/p/{d["page_id"]}')
    embed.set_image(url=f"attachment://{filename}.jpg")
    embed.set_thumbnail(url=f"{d['profile_img']}")
    embed.set_author(name=f"{d['account']}", url=f"https://instagram.com/{d['account']}")
    
    likes = num_format(d['likes'], 'like')
    comments = num_format(d['comments'], 'comment')
    embed.set_footer(text=f"{d['time']} -------- {likes}, {comments}")
    # embed.add_field(name='a', value='aaaaaaaa', inline=False)
    # embed.add_field(name='b', value='bbbbbbbb', inline=True)
    # embed.add_field(name='c', value='cccccccc', inline=True)
    # embed.add_field(name='d', value='dddddddd', inline=True)
    await channel.send(file=file, embed=embed)
    for x in channel.guild.roles:
        if all_roles[channel.id] == x.name:
            await channel.send(f'{x.mention} There is a new post from {all_feeds[channel.id]} instagram')
            await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even
            return

async def role_error(message, available_roles):
    print(available_roles, message.author.roles)
    await message.delete()
    nl = '\n'
    msg = f'{message.author.mention} I didn\'t recognize that command. Please make sure it matches the format `+new-role` or `-old-role`'
    current_roles = list([x.name for x in message.author.roles if x.name in available_roles])
    available_roles = list([x for x in available_roles if x not in current_roles])
    if not current_roles:
        current_roles = ['None']
    msg = msg + '\n' + f'Your available roles are ```{nl}{nl.join(available_roles)}{nl}```'
    msg = msg + '\n' + f'Your current roles are ```{nl}{nl.join(current_roles)}{nl}```'
    await message.channel.send(msg)
    return

@client.event
async def on_message(message):
    #only run where it should

    if message.guild == None:
        return
    if message.author == client.user:
        # reactions
        return
        if message.embeds:
            post_id = message.embeds[0].url.replace('https://instagram.com/p/', '')
            account = message.embeds[0].author.name
            with open(f'{mypath}{account}/{post_id}.json') as f:
                d = json.load(f)
            comments = d['comments']
            likes = d['likes']
            l = []
            for x in str(likes):
                l.append(emojis[x])
            l.append(emojis['likes'])
            l.append(emojis['spacer'])
            for x in str(comments):
                l.append(emojis[x])
            l.append(emojis['comments'])
            for x in l:
                print(post_id, x, end=' ')
                await message.add_reaction(x)
                time.sleep(1)
                await asyncio.sleep(1.2) #1.2 second timer so the deleting process can be even

        return

    # ignore webhooks
    if message.channel.id in twitters:
        return

    # admin commands
    if 'admin' in [x.name for x in message.author.roles]:
        if message.content == '!clear':
            await clear(message.channel)
            return

    # letting users in
    if message.channel.name == 'get-access':
        if re.match(r'^.+@wisc\.edu$', message.content):
            print(message.content, message.author)
            await message.delete()
            await message.channel.send(f'{message.author.mention} Welcome to the server!')
            await message.author.add_roles(discord.utils.get(message.author.guild.roles, name='verified'))
            user = client.get_user(91620951703183360)
            await user.send(f"New member: {message.author} ({message.author.display_name}) submitted email {message.content}")
            return
        else:
            await message.delete()
            await message.channel.send(f'{message.author.mention} I didn\'t recognize that email. Please make sure it matches the format `netID@wisc.edu`')
            return

    # setting up subscriptions
    if message.channel.name == 'subscribe-here':
        
        content = message.content.lower().replace(' ', '')
        
        if message.content.startswith('+'):
            new_role = message.content[1:]
            if new_role in [x.name for x in message.author.roles]:
                await message.channel.send(f'{message.author.mention} You are already subscribed to {new_role}')
                return
            if any(new_role == x for x in all_roles.values()):
                await message.author.add_roles(discord.utils.get(message.author.guild.roles, name=new_role))
                await message.channel.send(f'{message.author.mention} You have successfully subscribed to {new_role}')
                return

        
        elif message.content.startswith('-'):
            old_role = message.content[1:]
            if old_role in [x.name for x in message.author.roles]:
                await message.channel.send(f'{message.author.mention} You are not currently subscribed to {old_role}')
                return
            if any(old_role == x for x in all_roles.values()):
                await message.author.remove_roles(discord.utils.get(message.author.guild.roles, name=old_role))
                await message.channel.send(f'{message.author.mention} You have successfully unsubscribed from {old_role}')
                return
        #else
        await role_error(message, all_roles.values())
    
    # twitter
    if message.channel.id in twitters:
        for x in message.channel.guild.roles:
            if all_roles[message.channel.id] == x.name:
                await message.channel.send(f'{x.mention} There is a new post from {all_feeds[message.channel.id]} twitter')

    # filtering words
    l = []
    checkit = message.content.lower()
    for x in swearsies:
        if any(x == y for y in re.split('[ ]',checkit)):
            await message.delete()
            await message.channel.send(f'{message.author.mention} Let\'s keep this chat clean, OK?')
            return

client.run(TOKEN)