import discord
import requests
import io
from discord.ext import commands
from datetime import datetime
from pytz import timezone

tz = timezone('EST')
datetime.now(tz)

class GuildUtils(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def membercount(self, ctx):
        adminCount = sum(1 for member in ctx.guild.members if member.guild_permissions.administrator)
        mcountEmbed = discord.Embed(title = "Member Count", color = 0x6B31A5, timestamp = datetime.now())
        mcountEmbed.add_field(name = "**Members:**", value = ctx.guild.member_count, inline = False)
        mcountEmbed.add_field(name = "**Administrators:**", value = adminCount, inline = False)
        mcountEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = mcountEmbed)

async def setup(client):
    await client.add_cog(GuildUtils(client))