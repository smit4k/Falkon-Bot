import discord
import asyncio
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from pytz import timezone
from datetime import datetime
from datetime import date
import random
import os

load_dotenv()

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix="f!", intents=intents, case_insensitive=True)

TOKEN = os.getenv("secret_token")

tz = timezone("EST")
datetime.now(tz)


@client.command()
async def ping(ctx):
    pingEmbed = discord.Embed(color=0x6B31A5, timestamp=datetime.now())
    pingEmbed.add_field(
        name="**Pong!**",
        value=f"Latency: {round(client.latency * 1000)}ms",
        inline=False,
    )
    pingEmbed.set_footer(
        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar
    )
    await ctx.send(embed=pingEmbed)


@client.command()
async def whois(ctx, member: discord.Member):
    userInfoEmbed = discord.Embed(
        title=f"User info for {member.name}",
        description=member.mention,
        color=member.color,
        timestamp=datetime.now(),
    )
    userInfoEmbed.add_field(name="**ID:**", value=member.id, inline=False)
    userInfoEmbed.add_field(
        name="**Created At:**", value=str(member.created_at)[0:9], inline=False
    )

    userInfoEmbed.add_field(
        name="**Roles:**",
        value=" ".join(
            [role.mention for role in member.roles if role.name != "@everyone"]
        ),
        inline=False,
    )

    userInfoEmbed.set_thumbnail(url=member.display_avatar)
    userInfoEmbed.set_footer(
        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar
    )
    await ctx.send(embed=userInfoEmbed)


@client.command()
async def contributors(ctx):
    contribEmbed = discord.Embed(
        title="Contributors", color=0x6B31A5, timestamp=datetime.now()
    )
    contribEmbed.add_field(
        name="Lead Developer",
        value="<:discord:1195074703837102121> sm.it\n<:githubwhite:1195075097678065705> smit4k\n<:twitch:1195073396283801651> smitfps",
        inline=False,
    )
    contribEmbed.add_field(name="Developers", value="Placeholder", inline=False)
    contribEmbed.add_field(name="Testers", value="<@807555025634983967>", inline=False)
    contribEmbed.set_footer(
        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar
    )
    await ctx.send(embed=contribEmbed)


@client.command()
async def source(ctx):
    soEmbed = discord.Embed(title="Falkon Source Code", color=0x6B31A5)
    soEmbed.add_field(
        name="GitHub", value="https://www.github.com/smit4k/Falkon-Bot", inline=False
    )
    soEmbed.set_footer(
        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar
    )
    await ctx.send(embed=soEmbed)


@client.command()
async def suggest(ctx):
    suEmbed = discord.Embed(title="Suggest a feature", color=0x6B31A5)
    suEmbed.add_field(name="Google Forms", value="https://forms.gle/kPo3Ma17BjtC6rW18")
    suEmbed.set_footer(
        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar
    )
    await ctx.send(embed=suEmbed)


@client.command()
async def bugs(ctx):
    bugEmbed = discord.Embed(title="Known bugs", color=0x6B31A5)
    bugEmbed.add_field(name="Command not working", value="stocks/stockprice")
    bugEmbed.set_footer(
        text=f"Requested by {ctx.author.name}", icon_url=ctx.author.display_avatar
    )
    await ctx.send(embed=bugEmbed)


@client.event
async def on_ready():
    await client.change_presence(
        activity=discord.Streaming(
            name="prefix is f!", url="https://www.twitch.tv/smitfps"
        )
    )
    print("BOT IS ONLINE!\nSigned in as " + client.user.name)


async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await client.load_extension(f"cogs.{filename[:-3]}")


async def main():
    await load()
    await client.start(TOKEN)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
