import discord
from discord import File
import asyncio
import json
import os
import random
import requests
import pytesseract
from bs4 import BeautifulSoup
import imageio

bot = discord.Client(command_prefix="\\", status=discord.Status.online)
f = open('api.json')
api_keys = json.load(f)
f.close()

accepted = ["png", "jpg", "jpeg", "gif", "bmp", "webm", "mp4"]

@bot.event
async def on_message(msg):
    if(msg.author.id != bot.user.id):
        chan = bot.get_channel(msg.channel.id)
        if(msg.embeds):
            for attachment in msg.embeds:
                url = attachment.url
                id = url.rsplit("-",1)[1]
                r = requests.get(url)
                beaut = BeautifulSoup(r.text, "html.parser")
                for img in beaut.find_all("img"):
                    if(id in img.get("src")):
                        with open("temp/" + img.get("src").rsplit("/", 1)[1][:9], "wb+") as f:
                            f.write(requests.get(img.get("src")).content)
                        if(hasText("more", "temp/" + img.get("src").rsplit("/", 1)[1][:9])):
                            async with chan.typing():
                                await chan.send(file=File("memes/" + random.choice(os.listdir("memes"))))
        elif(msg.attachments):
            for attch in msg.attachments:
                url = attch.url
                filetype = url.rsplit(".", 1)[1]
                print(filetype)
                if(filetype in accepted):
                    print("Downloading " + url.rsplit("/", 1)[1])
                    r = requests.get(url)
                    with open("memes/" + url.rsplit("/", 1)[1], "wb+") as f:
                        f.write(r.content)
                        await msg.add_reaction('\U0001f44d')
        else:
            print("Nothing of interest")

@bot.event
async def on_ready():
    if(not os.path.isdir("temp")):
        os.mkdir("temp")
    print("Started")
    await bot.change_presence(activity=discord.CustomActivity(name="I will steal your memes"))

def hasText(term, file):
    img = imageio.get_reader(file)
    count = 3
    for frame in img:
        if(count == 0):
            if(term.upper() in pytesseract.image_to_string(frame).upper()):
                return True
            count = 3
        else:
            count -= 1
    return False

bot.run(api_keys["discord"])


