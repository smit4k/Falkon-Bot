import discord
from dotenv import load_dotenv
import asyncio
from discord import app_commands
from discord.ext import commands
from pytz import timezone
from datetime import datetime
import random
import os

load_dotenv

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = "m!", intents = intents, case_insensitive = True)
client.remove_command("help")

TOKEN = os.getenv("secret_token")

tz = timezone('EST')
datetime.now(tz)

@client.command()
async def ping(ctx):
  pingEmbed = discord.Embed(color = 0x6B31A5, timestamp = datetime.now())
  pingEmbed.add_field(name = "**Ping:**", value = f'Latency: {round(client.latency * 1000)}ms', inline = False)
  pingEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
  await ctx.send(embed = pingEmbed)

@client.command()
async def userinfo(ctx, member : discord.Member):
  userInfoEmbed = discord.Embed(title = f'User info for {member.name}', description = member.mention, color = member.color, timestamp = datetime.now())
  userInfoEmbed.add_field(name = "**ID:**", value = member.id, inline = False)
  userInfoEmbed.add_field(name = "**Created At:**", value = member.created_at, inline = False)
  userInfoEmbed.add_field(name = "**Top Role:**", value = member.top_role.mention, inline = False)
  userInfoEmbed.set_thumbnail(url = member.display_avatar)
  userInfoEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
  await ctx.send(embed = userInfoEmbed)

@client.command()
async def help(ctx):
  helpEmbed = discord.Embed(title = "Meteor Commands", color = 0x6B31A5, timestamp = datetime.now())
  helpEmbed.add_field(name = "**Fun Commands:**", value = "```8Ball``` Gives you a random outcome when you give it a question\n  ```flip``` Flips a coin and gives you either heads, or tails.\n  ```roll``` Rolls a die and gives you an random outcome of 1 - 6", inline = True)
  helpEmbed.add_field(name = "**Utility Commands:**", value = "```userinfo``` Gives you information about the user mentioned.\n  ```ping``` Gives you the current latency of the bot", inline = True)
  helpEmbed.add_field(name = "**Prefix:**", value = "The prefix for meteor bot is m!", inline = False)
  helpEmbed.add_field(name = "**Credits:**", value = "All coding, artwork and work was done by @sm.it (smit#2047)", inline = False)
  helpEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
  await ctx.send(embed = helpEmbed)

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Streaming(name = "prefix is m!", url = "https://www.twitch.tv/smitfps"))
    print("BOT IS ONLINE!")
  
async def load():
  for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
      await client.load_extension(f'cogs.{filename[:-3]}')

async def main():
  await load()
  await client.start(TOKEN)

asyncio.run(main())