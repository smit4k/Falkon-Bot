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

    @commands.command()
    async def onlinemembers(self, ctx):
        online_count = sum(1 for member in ctx.guild.members if member.status == discord.Status.online)
        idle_count = sum(1 for member in ctx.guild.members if member.status == discord.Status.idle)
        dnd_count = sum(1 for member in ctx.guild.members if member.status == discord.Status.do_not_disturb)

        onEmbed = discord.Embed(title = "Online Members", color = 0x6B31A5, timestamp = datetime.now())
        onEmbed.add_field(name = "Statuses", value = f"**Online:** {online_count} members\n**Idle:** {idle_count} members \n**Do Not Disturb:** {dnd_count} members", inline = False)
        onEmbed.add_field(name = "Total Users Online", value = online_count + idle_count + dnd_count, inline = False)
        onEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = onEmbed)

async def setup(client):
    await client.add_cog(GuildUtils(client))