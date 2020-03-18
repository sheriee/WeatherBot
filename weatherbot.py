import discord
import requests
from bs4 import BeautifulSoup

TOKEN = "<bot token>"   # Unique bot token abtained from discord

client = discord.Client()

def get_weather(location):
    place = "https://www.met.ie/forecasts/" + location
    page = requests.get(place)
    soup = BeautifulSoup(page.content, "html.parser")
    forecast = soup.find_all(class_="forecast")[0]  # Gets information from first instance of forecast class
    days = forecast.find_all("p")   # gets the information included in the paragraph tag
    return(days[1].get_text())  # returns text inside tags, weather for the day is the second element

def strip_command(text):
    return text.split(" ", 1)[1]

@client.event
async def on_message(message):
    if message.author == client.user: # we do not want the bot to reply to itself
        return
    if message.content.startswith('!weather'):
        location = strip_command(message.content)
        if location == "national":  #special case on met eireann site
            location = "national-forecast"
        try:
            weather = get_weather(location)
            await message.channel.send(weather)
        except:
            await message.channel.send(location + " not found")

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)