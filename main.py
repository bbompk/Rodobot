import discord
from discord.ext import commands
import os
import random
from datetime import datetime 
import logging

logging.basicConfig(level=logging.INFO)

prefix = '-rodo '
client = commands.Bot(command_prefix=prefix, case_insensitive=True, help_command=None)

@client.event
async def on_ready():
  print(f"I am ready to go - {client.user.name}")
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{client.command_prefix}help"))

@client.command(name="help")
async def _help(ctx) :
  f = open('./texts/help_commands.txt','r',encoding='utf-8')
  commands = ''.join(f.readlines())
  embed = discord.Embed(title="Curent Commands (Prefix: -rodo)",description=commands,color=0xDA4C4C)
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
  f = open('./texts/dev_status.txt','r',encoding='utf-8')
  dev_status = ''.join(f.readlines())
  embed = discord.Embed(title="Dev Status",description=dev_status,color=0xB7829A)
  f.close()
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

# BOT_TOKEN = "TOKEN" insert your bot token here     
client.run(BOT_TOKEN)