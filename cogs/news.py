import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
from datetime import date
from pytz import timezone
import requests

load_dotenv()

newskey = os.getenv("news_key")

tz = timezone('EST')
datetime.now(tz)

class News(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def getnews(self, ctx):
        newsTitle = await self.get_BusinessUS_Title()
        source = await self.get_BusinessUS_Source()
        description = await self.get_BusinessUS_Description()

        newsEmbed = discord.Embed(title = newsTitle, color = 0x6B31A5, timestamp = datetime.now())
        newsEmbed.add_field(name = "Source", value = source, inline = False)
        newsEmbed.add_field(name = "Description", value = description, inline = False)
        newsEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = newsEmbed)

    async def get_BusinessUS_Source(self):
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={newskey}")
        data = response.json()
        source = data["articles"][0]["source"]["name"]
        author = data["articles"][0]["author"]
        return f"{source}, by *{author}*"
        
    async def get_BusinessUS_Title(self):
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={newskey}")
        data = response.json()
        title = data["articles"][0]["title"]
        return title
    async def get_BusinessUS_Description(self):
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={newskey}")
        data = response.json()
        description = data["articles"][0]["description"]
        return description

        

async def setup(client):
    await client.add_cog(News(client))
