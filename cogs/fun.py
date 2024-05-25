import discord
import os
import requests
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import random
from PIL import Image
import io

coinFlip = ["Heads", "Tails"]

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
        diceRollEmbed.add_field(name = "**You rolled a die and got:**", value = random.randint(1,6), inline = False)
        diceRollEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = diceRollEmbed)

    @commands.command(aliases = ["8ball"])
    async def eightball(self, ctx, *, question):
        response = await self.getResponse()
        _8ballEmbed = discord.Embed(title = "8Ball", color = 0x6B31A5, timestamp = datetime.now())
        _8ballEmbed.add_field(name = "**Question:**", value = question, inline = False)
        _8ballEmbed.add_field(name = "**Answer:**", value = response, inline = False)
        _8ballEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = _8ballEmbed)

    @commands.command(aliases=["randcolors"])
    async def randomcolor(self, ctx):
        red = random.randint(0,255)
        green = random.randint(0,255)
        blue = random.randint(0,255)

        hexcolor = f"#{red:02x}{green:02x}{blue:02x}"

        width = 256
        height = 256

        image = Image.new("RGB", (width, height), (red, green, blue))
        image_file = io.BytesIO()
        image.save(image_file, "JPEG")
        image_file.seek(0)

        file = discord.File(image_file, filename = "randomcolor.png")

        randColorEmbed = discord.Embed(title = "Random Color", color = discord.Color.from_rgb(red,green,blue), timestamp = datetime.now())
        randColorEmbed.add_field(name = "RGB", value = f"{red}, {green}, {blue}", inline = False)
        randColorEmbed.add_field(name = "Hexadecimal", value = hexcolor, inline = False)
        randColorEmbed.set_image(url = "attachment://randomcolor.png")
        randColorEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(file=file, embed=randColorEmbed)


    @commands.command()
    async def joke(self, ctx):
        try:
            joke = await self.get_Joke()
            await ctx.send(joke)
        except Exception as e:
            await ctx.send("Error fetching joke, please try again later")

    @commands.command(aliases=["fortunecookie"])
    async def fortune(self, ctx):
        file_path = "assets/fortunes.txt"  # Replace with the actual path to your file
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
        meme = await self.get_Meme()
        memeTitle = await self.get_Meme_Title()

        meEmbed = discord.Embed(title = memeTitle, color = 0x6B31A5, timestamp = datetime.now())
        meEmbed.set_image(url = meme)
        meEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = meEmbed)

    @commands.command()
    async def bored(self, ctx):
        bored = await self.get_Bored()

        boEmbed = discord.Embed(title = "Do This if You're Bored!", color = 0x6B31A5, timestamp = datetime.now())
        boEmbed.add_field(name = "", value = bored, inline = False)
        boEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = boEmbed)

    async def getResponse(self):
        file_path = "assets/responses.txt"
        response = "";
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.read().splitlines()
                if lines:
                    response = random.choice(lines)
                else:
                    response = "Error: File not found."
        except Exception as e:
            response = "An error occurred: {e}"
        return response

    async def get_Joke(self):
        response = requests.get("https://v2.jokeapi.dev/joke/Any?blacklistFlags=nsfw&type=single")
        data = response.json()
        return data["joke"]

    async def get_Meme(self):
        response = requests.get("https://meme-api.com/gimme")
        data = response.json()

        return data["preview"][4]

    async def get_Meme_Title(self):
        response = requests.get("https://meme-api.com/gimme")

        data = response.json()
        return data["title"]

    async def get_Bored(self):
        response = requests.get("https://www.boredapi.com/api/activity")

        data = response.json()
        activity = data["activity"]
        type = data["type"]
        participants = data["participants"]
        return f"**Activity:** {activity}\n**Type:** {type.capitalize()}\n**Participants:** {participants}"


async def setup(client):
    await client.add_cog(Fun(client))
