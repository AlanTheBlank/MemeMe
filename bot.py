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
import cv2
import instaloader

IL = None

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
            print("Embed")
            for attachment in msg.embeds:
                url = attachment.url
                id = url.rsplit("-",1)[1]
                r = requests.get(url)
                beaut = BeautifulSoup(r.text, "html.parser")
                for img in beaut.find_all("img"):
                    if(id in img.get("src")):
                        print(img.get("src"))
                        with open("temp/" + img.get("src").rsplit("/", 1)[1][:9], "wb+") as f:
                            f.write(requests.get(img.get("src")).content)
                        if(hasText("temp/" + img.get("src").rsplit("/", 1)[1][:9])):
                            await msg.add_reaction('\U00002705')
                            async with chan.typing():
                                await chan.send(file=File("memes/" + random.choice(os.listdir("memes"))))
                        else:
                            await msg.add_reaction('\U0000274C')
        elif(msg.attachments):
            print("Attachment")
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
            print(msg)
            print("Nothing of interest")
    for x in os.listdir("temp"):
        os.remove("temp/" + x)


@bot.event
async def on_ready():
    global IL
    if(not os.path.isdir("temp")):
        os.mkdir("temp")
    print("Started")
    IL = instaloader.Instaloader(dirname_pattern="memes", download_video_thumbnails=False, download_comments=False, download_geotags=False)
    for p in instaloader.Hashtag.from_name(IL.context, "yeetmemes").get_posts():
        IL.download_post(p, target="#yeetmemes")
    await bot.change_presence(activity=discord.CustomActivity(name="I will steal your memes"))

def hasText(file):
    terms = ['MO', 'OR', 'RE', 'MOR', 'ORE', 'MORE']
    img = imageio.get_reader(file)
    count = 0
    for frame in img:
        cv2.imwrite("temp/temp.jpg", frame)
        im = cv2.imread("temp/temp.jpg")
        grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        out = pytesseract.image_to_string(grey, config='--psm 6')
        for term in terms:
           if(term in out.upper()):
                print("has text")
                return True
    print("No text")
    return False

bot.run(api_keys["discord"])


