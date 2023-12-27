import discord
import os
import requests
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import random

coinFlip = ["Heads", "Tails"]
diceRollList = ["1", "2", "3", "4", "5", "6"]
responses = ["It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Yes - definitely.",
"You may rely on it.",
"As I see it, yes.",
"Most likely.",
"Outlook good.",
"Yes.",
"Signs point to yes.",
"Reply hazy, try again.",
"Ask again later.",
"Better not tell you now.",
"Cannot predict now.",
"Concentrate and ask again.",
"Don't count on it.",
"My reply is no.",
"My sources say no.",
"Outlook not so good.",
"Very doubtful."]

tz = timezone('EST')
datetime.now(tz)

class Fun(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases = ["coinflip"])
    async def flip(self, ctx):
        flipEmbed = discord.Embed(color = 0x6B31A5, timestamp = datetime.now())
        flipEmbed.add_field(name = "**You flipped a coin and got:**", value = random.choice(coinFlip), inline = False)
        flipEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = flipEmbed)

    @commands.command(aliases = ["rolldice", "roll"])
    async def diceroll(self,ctx):
        diceRollEmbed = discord.Embed(color = 0x6B31A5, timestamp = datetime.now())
        diceRollEmbed.add_field(name = "**You rolled a die and got:**", value = random.choice(diceRollList), inline = False)
        diceRollEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = diceRollEmbed)

    @commands.command(aliases = ["8ball"])
    async def eightball(self, ctx, *, question):
        _8ballEmbed = discord.Embed(title = "8Ball", color = 0x6B31A5, timestamp = datetime.now())
        _8ballEmbed.add_field(name = "**Question:**", value = question, inline = False)
        _8ballEmbed.add_field(name = "**Answer:**", value = random.choice(responses), inline = False)
        _8ballEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = _8ballEmbed)

    @commands.command()
    async def joke(self, ctx):
        try:
            joke = await self.get_Joke()
            await ctx.send(joke)
        except Exception as e:
            await ctx.send("Error fetching joke, please try again later")

    @commands.command(aliases=["fortunecookie"])
    async def fortune(self, ctx):
        file_path = "fortunes.txt"  # Replace with the actual path to your file
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.read().splitlines()
                if lines:
                    random_line = random.choice(lines)
                    await ctx.send(random_line)
                else:
                    await ctx.send("The file is empty.")
        except FileNotFoundError:
            await ctx.send("File not found.")
        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def meme(self, ctx):
        try:
            meme = await self.get_Meme()
            await ctx.send(meme)
        except Exception as e:
            await ctx.send("Error fetching meme, please try again later.")

    
    async def get_Joke(self):
        response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw&type=single")
        data = response.json()
        return data["joke"]
    
    async def get_Meme(self):
        response = requests.get("https://meme-api.com/gimme")
        data = response.json()
        return data["preview"][3]


async def setup(client):
    await client.add_cog(Fun(client))