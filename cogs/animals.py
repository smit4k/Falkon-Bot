import discord
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import requests


class Animals(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def dog(self, ctx):
        try:
            dog_image = await self.get_Dog_Image()
            await ctx.send(dog_image)
        except Exception as e:
            await ctx.send('Error fetching dog image. Please try again later.')

    @commands.command()
    async def cat(self, ctx):
        try:
            cat_image = await self.get_Cat_Image()
            await ctx.send(cat_image)
        except Exception as e:
            await ctx.send("Error fetching cat image. Please try again later.")

    @commands.command()
    async def fox(self, ctx):
        try:
            fox_image = await self.get_Fox_Image()
            await ctx.send(fox_image)
        except Exception as e:
            await ctx.send("Error fetching fox image. Please try again later.")


    async def get_Dog_Image(self):
        response = requests.get("https://dog.ceo/api/breeds/image/random")
        data = response.json() # Parses the response as json
        return data["message"] # Returns the "message" in the json response
    
    async def get_Cat_Image(self):
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        data = response.json()
        cat_url = data[0]['url'] if data else 'No cat image found.'
        return cat_url

    async def get_Fox_Image(self):
        response = requests.get("https://randomfox.ca/floof/?ref=apilist.fun")
        data = response.json()
        return data["image"]

async def setup(client):
    await client.add_cog(Animals(client))
