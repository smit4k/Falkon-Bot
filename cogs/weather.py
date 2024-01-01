import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import requests

load_dotenv()

KEY = os.getenv("weather_key")

tz = timezone('EST')
datetime.now(tz)


class Weather(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def mycogtest(self, ctx):
        await ctx.send("Weather cog loaded, it works")

    @commands.command()
    async def weather(self, ctx, *, query):
        weather = await self.get_Current_Weather(query)

        weEmbed = discord.Embed(title = f"Current Weather for {query.capitalize()}", color = 0x6B31A5, timestamp = datetime.now())
        weEmbed.add_field(name = "", value = weather, inline = False)
        weEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = weEmbed)


    async def get_Current_Weather(self, q):
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?q={q}&key={KEY}")

        data = response.json()
        condition = data["current"]["condition"]["text"]
        temp = data["current"]["temp_f"]
        feelsLike = data["current"]["feelslike_f"]
        return f"**Temperature:** {temp} °F\n**Feels Like:** {feelsLike} °F\n**Condition:** {condition}"


async def setup(client):
    await client.add_cog(Weather(client))
