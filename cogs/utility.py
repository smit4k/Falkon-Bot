import discord
import pyshorteners
import requests
from translate import Translator
import qrcode
import io
from discord.ext import commands
from datetime import datetime
from pytz import timezone

tz = timezone('EST')
datetime.now(tz)

urlShortener = pyshorteners.Shortener()

class Utility(commands.Cog):
    def __init__(self,client):
        self.client = client
        
    @commands.command(aliases=["qr", "makeqr"])
    async def qrcode(self, ctx, *, link):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(link)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image to a BytesIO buffer
        with io.BytesIO() as image_binary:
            img.save(image_binary, format="PNG")
            image_binary.seek(0)

            # Send the image
            await ctx.send(file=discord.File(fp=image_binary, filename="qrcode.png"))

    @commands.command(aliases = ["linkshorten", "shortenlink", "shortlink"])
    async def sl(self, ctx, *, link):
        slEmbed = discord.Embed(color = 0x6B31A5, timestamp = datetime.now())
        slEmbed.add_field(name = "**Your shortened link is:**", value = urlShortener.dagd.short(link), inline = False)
        slEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = slEmbed)

    @commands.command(aliases=["expand"])
    async def unshorten(self, ctx, *, link):
        usEmbed = discord.Embed(color = 0x6B31A5, timestamp = datetime.now())
        usEmbed.add_field(name = "**Your expanded link is:**", value = urlShortener.dagd.expand(link), inline = False)
        usEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = usEmbed)

    @commands.command()
    async def translate(self, ctx, to_language:str, *, text):
        translator = Translator(to_lang=to_language)
        translation=translator.translate(text)
        trEmbed = discord.Embed(color = 0x6B31A5, timestamp = datetime.now())
        trEmbed.add_field(name = f"Translated to {to_language.upper()}", value = translation,inline = False)
        trEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = trEmbed)

    @commands.command()
    async def iplookup(self, ctx, *, ip):
        lookup = await self.get_Ip(ip)

        ipEmbed = discord.Embed(title = f"IP Lookup for {ip}", color = 0x6B31A5, timestamp = datetime.now())
        ipEmbed.add_field(name = "", value = lookup, inline = False)
        ipEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = ipEmbed)

    async def get_Ip(self,ip):
        response = requests.get(f"http://ip-api.com/json/{ip}")
        data = response.json()
        country = data["country"]
        region = data["region"]
        city = data["city"]
        lat = data["lat"]
        lon = data["lon"]
        return f"**Country:** {country}\n**Region:** {region}\n**City:** {city}\n**Latitude:** {lat}\n**Longitude:** {lon}"


async def setup(client):
    await client.add_cog(Utility(client))