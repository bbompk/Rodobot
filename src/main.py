import discord
from discord.ext import commands, tasks
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option
import os
import random
from dotenv import load_dotenv
import json
import time
import pytz
from datetime import datetime 
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)

prefix = "-rodo0 "
client = commands.Bot(command_prefix=prefix, case_insensitive=True, help_command=None)
slash = SlashCommand(client, sync_commands=True) # Declares slash commands through the client.

BOT_TOKEN = os.getenv('BOT_TOKEN')
guild_ids = json.load(open('guild_ids.json'))['guild_ids']

@client.event
async def on_ready():
  print(f"I am ready to go - {client.user.name}")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{client.command_prefix}help"))

@client.command(name="help")
async def _help(ctx) :
  f = open('./texts/help_commands.txt','r',encoding='utf-8')
  commands = ''.join(f.readlines())
  embed = discord.Embed(title="Curent Commands (Prefix: -rodo0)",description=commands,color=0xDA4C4C)
  f.close()
  await ctx.send(embed=embed)

@client.command(name="ping")
async def _ping(ctx):
  await ctx.send(f"Ping: {client.latency}")

@client.command(name="hello")
async def _hello(ctx):
  await ctx.send("Hello, I'm Rodo! <:prasrodo:796030411570282496>")

@client.command(name="coinflip")
async def _coinflip(ctx):
  c = "Head" if random.randint(0,1) else "Tail"
  await ctx.send(f"Coinflip: {c}")

@client.command(name="dev")
async def _dev(ctx):
  version = os.getenv('VERSION')
  embed = discord.Embed(title="Rodobot Github Repo",description="Version: "+version,url="https://github.com/bbompk/Rodobot.git",color=0xB7829A)
  embed.add_field(name="Github Repo",value="https://github.com/bbompk/Rodobot.git",inline=False)
  embed.add_field(name="Contributors",value="bbomya, Prasrodo")
  await ctx.send(embed=embed)

@client.command(name="pick")
async def _choose(ctx, n=1):
  n=int(n)
  await ctx.send("Give me the items you want to pick from:")
  msg = await client.wait_for("message", check=lambda msg :msg.author == ctx.author and msg.channel == ctx.channel)
  items = msg.content.split()
  if items[0] == 'range' :
    if(int(items[1])<=int(items[2])):
      items = [e for e in range(int(items[1]),int(items[2])+1)]
    else: await ctx.send("invalid range!")
  if int(n) <= len(items) :
    pool = list()
    for i in range(n) :
      poll = random.randint(0,len(items)-1)
      pool.append(str(items.pop(poll)))
    await ctx.send(f"Winner: {','.join(pool)}")
  else: await ctx.send("Too few items to pick from!")

@client.command(name="partymaker")
async def _divide_to_groups(ctx, n: int) :
  await ctx.send("Give me the items you want to divide into groups:")
  msg = await client.wait_for("message", check=lambda msg :msg.author == ctx.author and msg.channel == ctx.channel)
  items = msg.content.split()
  random.shuffle(items)
  if n<= len(items) :
    embed = discord.Embed(color=0xB7829A)
    x = len(items)
    result = []
    for i in range(n) :
      result.append([])
    for i in range(n) :
      for j in range(x//n) :
        result[i].append(items.pop())
    for i in range(len(items)) :
        result[i].append(items.pop())
    for i in range(n):
      result[i] = "Group {} - {}".format(i+1,' '.join(result[i]))
    embed.add_field(name="Partymaker Result",value='\n'.join(result),inline=False)
    await ctx.send(embed=embed)
  else :
    await ctx.send("Too few items!")

@client.command(name="snakeladder")
async def _matchmake(ctx) :
  await ctx.send("Give me participants/fisrt group:")
  msg = await client.wait_for("message", check=lambda msg :msg.author == ctx.author and msg.channel == ctx.channel)
  g1 = msg.content.split()
  await ctx.send("Now give me the results/second group:")
  msg = await client.wait_for("message", check=lambda msg :msg.author == ctx.author and msg.channel == ctx.channel)
  g2 = msg.content.split()
  if len(g1) == len(g2) :
    embed = discord.Embed(color=0xB7829A)
    random.shuffle(g1)
    random.shuffle(g2)
    result = []
    for i in range(len(g1)) :
      result.append("{} - {}".format(g1[i],g2[i]))
    embed.add_field(name="Snakeladder Result",value='\n'.join(result),inline=False)
    await ctx.send(embed=embed)
  else: await ctx.send("Participants and Results must have the same amount!")

@client.command(name="rolldice")
async def _rolldice(ctx, roll=1, faces=6):
  roll=int(roll);faces=int(faces)
  result = []
  for i in range(roll):
    result.append(str(random.randint(1,faces)))
  await ctx.send('Roll Dice: '+' '.join(result))

@slash.slash(name="coinflip", guild_ids=guild_ids, description="flip a coin")
async def _ping(ctx): 
    c = "Head" if random.randint(0,1) else "Tail"
    await ctx.send(f"Coinflip: {c}")

@slash.slash(name="rodopoll",
             description="This is just a test command, nothing more.",
             guild_ids=guild_ids,
             options=[
               create_option(
                 name="question_or_title",
                 description="Title or Question for the poll",
                 option_type=3,
                 required = True
               ),create_option(name="choice_1",description="create a choice",option_type=3,required=False),
               create_option(name="choice_2",description="create a choice",option_type=3,required=False),
               create_option(name="choice_3",description="create a choice",option_type=3,required=False),
               create_option(name="choice_4",description="create a choice",option_type=3,required=False),
               create_option(name="choice_5",description="create a choice",option_type=3,required=False),
               create_option(name="choice_6",description="create a choice",option_type=3,required=False),
               create_option(name="choice_7",description="create a choice",option_type=3,required=False),
               create_option(name="choice_8",description="create a choice",option_type=3,required=False),
               create_option(name="choice_9",description="create a choice",option_type=3,required=False),
               create_option(name="choice_10",description="create a choice",option_type=3,required=False),
             ])
async def test(ctx, question_or_title: str,choice_1="",choice_2="",choice_3="",choice_4="",choice_5="",choice_6="",choice_7="",choice_8="",choice_9="",choice_10=""):
  in_choices = (choice_1,choice_2,choice_3,choice_4,choice_5,choice_6,choice_7,choice_8,choice_9,choice_10)
  choices = []
  emotes = ('🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯')
  for c in in_choices:
      if c != "" :
        choices.append(c)
  result = []
  for i in range(len(choices)) :
    result.append(emotes[i]+' : '+choices[i]+'\n')
  embed = discord.Embed(color=0xB7829A)
  if len(choices) > 0 : embed.add_field(name=question_or_title,value=''.join(result)) 
  else : embed.add_field(name=question_or_title+'\n',value='-forgot to add choices dumbass-')
  embed.timestamp = datetime.now(pytz.utc)
  message = await ctx.send(embed=embed)
  for i in range(len(choices)) :
    await message.add_reaction(emotes[i])

  
client.run(BOT_TOKEN)