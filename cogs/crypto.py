import discord
import requests
import io
from discord.ext import commands
from datetime import datetime
from pytz import timezone

tz = timezone('EST')
datetime.now(tz)

class Crypto(commands.Cog):
    def __init__(self,client):
        self.client = client

    

async def setup(client):
    await client.add_cog(Crypto(client))
