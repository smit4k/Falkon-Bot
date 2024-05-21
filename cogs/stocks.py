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

KEY = os.getenv("alphavantage_key")

tz = timezone('EST')
datetime.now(tz)

class Stocks(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def stockprice(self,ctx,*,ticker):
        ticker = ticker.upper()
        openPrice = await self.getCurrentOpenStockPrice(ticker)
        interval = await self.getInterval(ticker)
        timeZone = await self.getTimeZone(ticker)
        stockEmbed = discord.Embed(title = ticker, color = 0x6B31A5, timestamp = datetime.now())
        stockEmbed.add_field(name = "Interval", value = interval, inline = False)
        stockEmbed.add_field(name = "Time Zone", value = timeZone, inline = False)
        stockEmbed.add_field(name = "Open Price", value = openPrice, inline = False)
        stockEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar) 
        await ctx.send(embed = stockEmbed)



    async def getCurrentOpenStockPrice(self, ticker):
        response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={KEY}")
        data = response.json()
        time_series = data["Time Series (5min)"]
        latest_timestamp = sorted(time_series.keys(), reverse=True)[0]
        open_price = time_series[latest_timestamp]["1. open"]
        return open_price

    async def getInterval(self,ticker):
        response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={KEY}")
        data = response.json()
        interval = data["Meta Data"]["4. Interval"]
        return interval
        
    async def getTimeZone(self, ticker):
        response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={KEY}")
        data = response.json()
        timeZone = data["Meta Data"]["6. Time Zone"]
        return timeZone
        


async def setup(client):
    await client.add_cog(Stocks(client))
