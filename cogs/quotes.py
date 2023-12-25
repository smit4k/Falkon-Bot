import discord
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import requests

class Quotes(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def quote(self, ctx):
        try:
            quote = await self.get_Quote()
            await ctx.send(quote)
        except Exception as e:
            await ctx.send("Error fetching quote, please try again later")

    async def get_Quote(self):
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        quote_text = data[0]["q"]
        author = data[0]["a"]
        return f"*{quote_text}* - {author}"
        


async def setup(client):
    await client.add_cog(Quotes(client))