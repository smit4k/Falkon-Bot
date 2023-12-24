import discord
import pyshorteners
from discord.ext import commands
from datetime import datetime
from pytz import timezone

tz = timezone('EST')
datetime.now(tz)

urlShortener = pyshorteners.Shortener()

class Utility(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases = ["linkshorten", "shortenlink"])
    async def sl(self, ctx, *, link):
        slEmbed = discord.Embed(color = 0x6B31A5, timestamp = datetime.now())
        slEmbed.add_field(name = "**Your shortened link is:**", value = urlShortener.tinyurl.short(link), inline = False)
        slEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = slEmbed)

    @commands.command()
    async def ver(self, ctx):
        verEmbed = discord.Embed(title = "BETA 0.02", color = 0x6B31A5, timestamp = datetime.now())
        verEmbed.add_field(name = "**Upcoming Features:**", value = "* Steam Commands")
        verEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = verEmbed)

async def setup(client):
    await client.add_cog(Utility(client))