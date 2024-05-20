import discord
import requests
import io
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import json
import aiohttp

tz = timezone('EST')
datetime.now(tz)

class Crypto(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def cryptoprice(self, ctx, *, crypto):
        price = await self.get_Crypto_Price(crypto)
        cryptoLogo = await self.get_Crypto_Logo(crypto)

        cryptoEmbed = discord.Embed(title = crypto.upper(), color = 0x6B31A5, timestamp = datetime.now())
        cryptoEmbed.set_thumbnail(url = cryptoLogo)
        cryptoEmbed.add_field(name = f"{crypto.upper()} → USD", value = price, inline = False)
        cryptoEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = cryptoEmbed)

    async def get_Crypto_Price(self,cryptocurrency):
        response = requests.get(f"https://api.blockchain.com/v3/exchange/tickers/{cryptocurrency.upper()}-USD")
        data = response.json()
        price = data["price_24h"]
        lastTradePrice = data["last_trade_price"]
        return f"**Price:** ${price}\n**Last Trade Price:** ${lastTradePrice}"

    async def get_Crypto_Logo(self, cryptocurrency):
        url = 'https://logos.tradeloop.app/api/getLogos'  # Replace with the actual URL
        payload = {
            "symbols": [cryptocurrency.upper()],
            "resolution": "128",
            "mode": "single",
            "parser": {
                "enable": True,
                "options": {
                    "removeNumbers": False
                }
            }
        }

# Set the headers
        headers = {
            'Content-Type': 'application/json'
        }

# Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(payload))

# Parse the response JSON
        response_json = response.json()
        return response_json[0]["png"]
    

async def setup(client):
    await client.add_cog(Crypto(client))
