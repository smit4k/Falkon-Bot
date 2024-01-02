import discord
import os
from dotenv import load_dotenv
from discord.ext import commands
from datetime import datetime
from pytz import timezone
import requests

load_dotenv()

KEY = os.getenv("weather_key")

tz = timezone('EST')
datetime.now(tz)


class Weather(commands.Cog):
    def __init__(self,client):
        self.client = client

    @commands.command()
    async def mycogtest(self, ctx):
        await ctx.send("Weather cog loaded, it works")

    @commands.command()
    async def weather(self, ctx, *, query):
        weather = await self.get_Current_Weather(query)
        wind = await self.get_Current_Wind(query)
        icon = await self.get_Condition_Icon(query)

        weEmbed = discord.Embed(title = f"Current Forecast for {query.capitalize()}", color = 0x6B31A5, timestamp = datetime.now())
        weEmbed.add_field(name = "Temperature", value = weather, inline = False)
        weEmbed.add_field(name = "Wind", value = wind, inline = False)
        weEmbed.set_thumbnail(url = icon)
        weEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = weEmbed)

    @commands.command()
    async def aqi(self, ctx, *, query):
        currentAQI = await self.get_Current_AQI(query)
        aqiEmbed = discord.Embed(title = f"Current Air Quality for {query.capitalize()}", color = 0x6B31A5, timestamp = datetime.now())
        aqiEmbed.add_field(name = "", value = currentAQI, inline = False)
        aqiEmbed.set_footer(text = f'Requested by {ctx.author.name}', icon_url = ctx.author.display_avatar)
        await ctx.send(embed = aqiEmbed)


    async def get_Current_Weather(self, q):
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?q={q}&key={KEY}")

        data = response.json()
        condition = data["current"]["condition"]["text"]
        temp = data["current"]["temp_f"]
        feelsLike = data["current"]["feelslike_f"]
        return f"**Temperature:** {temp} °F\n**Feels Like:** {feelsLike} °F\n**Condition:** {condition}"
    
    async def get_Current_Wind(self, q):
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?q={q}&key={KEY}")
        
        data = response.json()
        windSpeed = data["current"]["wind_mph"]
        windDir = data["current"]["wind_dir"]
        return f"**Wind Speed:** {windSpeed} mph\n**Wind Direction:** {windDir}"
    
    async def get_Condition_Icon(self, q):
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?q={q}&key={KEY}")
        
        data = response.json()
        relativeIcon = data["current"]["condition"]["icon"]
        icon = f"https:{relativeIcon}"
        return icon

    async def get_Current_AQI(self, q):
        response = requests.get(f"https://api.weatherapi.com/v1/current.json?q={q}&aqi=yes&key={KEY}")

        data = response.json()
        aqi = data["current"]["air_quality"]["pm2_5"]
        epaIndex = data["current"]["air_quality"]["us-epa-index"]

        if epaIndex == 1:
            epaDescription = "Good"
        elif epaIndex == 2:
            epaDescription =  "Moderate"
        elif epaIndex == 3:
            epaDescription = "Unhealthy for Sensitive Groups"
        elif epaIndex == 4:
            epaDescription = "Unhealthy"
        elif epaIndex == 5:
            epaDescription = "Very Unhealthy"
        elif epaIndex == 6:
            epaDescription ="Hazardous"
        else:
            epaDescription = "Unknown"
        
        return f"**AQI:** {aqi}\n**EPA Index:** {epaIndex} *({epaDescription})*"


async def setup(client):
    await client.add_cog(Weather(client))
