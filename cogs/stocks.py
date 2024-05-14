import discord
import requests
import os
from dotenv import load_dotenv
import io
from discord.ext import commands
from datetime import datetime
from datetime import date
from pytz import timezone

today = date.today()

load_dotenv()

KEY = os.getenv("polygon_key")

tz = timezone('EST')
datetime.now(tz)

class Stocks(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def stockprice(self,ctx,*,ticker):
        closed_price = await self.get_Day_Close_Price(ticker)
        stockPriceEmbed = discord.Embed(title = f"TODAY: {ticker.upper()}", color = 0x6B31A5, timestamp = datetime.now())
        stockPriceEmbed.add_field(name = "Price", value = closed_price, inline = False)
        stockPriceEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = stockPriceEmbed)

    async def get_Day_Close_Price(self,ticker):
        response = requests.get(f"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{today}/{today}?apiKey={KEY}")
        data = response.json()
        closed_price = data["results"]["0"]["c"]
        print(closed_price)
        return closed_price




async def setup(client):
    await client.add_cog(Stocks(client))