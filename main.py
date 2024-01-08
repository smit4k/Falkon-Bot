import discord
import asyncio
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from pytz import timezone
from datetime import datetime
import random
import os

load_dotenv()

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix = "f!", intents = intents, case_insensitive = True)

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
async def whois(ctx, member : discord.Member):
  userInfoEmbed = discord.Embed(title = f'User info for {member.name}', description = member.mention, color = member.color, timestamp = datetime.now())
  userInfoEmbed.add_field(name = "**ID:**", value = member.id, inline = False)
  userInfoEmbed.add_field(name = "**Created At:**", value = member.created_at, inline = False)
  userInfoEmbed.add_field(name = "**Roles:**", value = f"{' '.join([role.mention for role in member.roles if role.name != '@everyone'])}", inline = False)
  userInfoEmbed.set_thumbnail(url = member.display_avatar)
  userInfoEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
  await ctx.send(embed = userInfoEmbed)


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

# Ensure the event loop is running
loop = asyncio.get_event_loop()
loop.run_until_complete(main())