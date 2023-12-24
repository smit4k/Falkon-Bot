import discord
from discord.ext import commands
from datetime import datetime
from pytz import timezone
from steam import Steam
from decouple import config

KEY = config("STEAM_API_KEY")
steam = Steam(KEY)

tz = timezone("EST")
datetime.now(tz)

class SteamCmds(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command(aliases = ["sui", "steamui"])
    async def steamuserinfo(self, ctx, *, steamid):
        user_data = steam.users.search_user(steamid)

        if user_data:
            user = user_data.get("player", {})
            user_id = user.get("steamid", "N/A")
            username = user.get("personaname", "N/A")
            profile_url = user.get("profileurl", "N/A")
            avatar_url = user.get("avatarfull", "N/A")
            steam_level = user.get("playerlevel", "N/A")

        steamUserInfoEmbed = discord.Embed(title = "Steam User Search:", color = 0x6B31A5, timestamp = datetime.now())
        steamUserInfoEmbed.add_field(name = "Username: ", value = username, inline = False)
        steamUserInfoEmbed.add_field(name = "SteamID: ", value = user_id, inline = False)
        steamUserInfoEmbed.add_field(name = "Level: ", value = steam_level, inline = False)
        steamUserInfoEmbed.add_field(name = "Visit this user on Steam: ", value = profile_url, inline = True)
        steamUserInfoEmbed.set_thumbnail(url = avatar_url)
        steamUserInfoEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed=steamUserInfoEmbed)

async def setup(client):
    await client.add_cog(SteamCmds(client))

