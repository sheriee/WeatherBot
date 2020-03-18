import discord
import requests
from bs4 import BeautifulSoup

TOKEN = "<bot token>"

client = discord.Client()

def get_weather(location):
    place = "https://www.met.ie/forecasts/" + location
    page = requests.get(place)
    soup = BeautifulSoup(page.content, "html.parser")
    forecast = soup.find_all(class_="forecast")[0]
    days = forecast.find_all("p")
    return(days[1].get_text())

def strip_command(text):
    return text.split(" ", 1)[1]

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!weather'):
        location = strip_command(message.content)
        if location == "national":
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