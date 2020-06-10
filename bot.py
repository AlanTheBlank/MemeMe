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

#The activity acts more as a disclaimer more than anything else
bot = discord.Client(command_prefix="\\", status=discord.Status.online, activity=discord.CustomActivity(name="I will steal your memes"))

# Ha, no api key leakage today, fuck you temper and illict hacking group or whatever ye were called
f = open('api.json')
api_keys = json.load(f)
f.close()

#tf is any other file format, get outta here
accepted = ["png", "jpg", "jpeg", "gif", "bmp", "webm", "mp4"]

ready = False

@bot.event
async def on_message(msg):
    # Makes sure that we aren't reacting off our own message.  Wish I thought of it the first time
    if(msg.author.id != bot.user.id):
        chan = bot.get_channel(msg.channel.id)
        # Checks if the user has sent a gif, I hope discord doesn't also use GIPHY in their gif search engine
        if("tenor" in msg.content):
            # Since the message autosends we want the first part of the message
            url = msg.content.split(" ")[0]
            # it's a surprise tool that will help up later
            id = url.rsplit("-",1)[1]
            r = requests.get(url)
            beaut = BeautifulSoup(r.text, "html.parser")
            for img in beaut.find_all("img"):
                # it's later
                if(id in img.get("src")):
                    with open("temp/" + img.get("src").rsplit("/", 1)[1][:9], "wb+") as f:
                        f.write(requests.get(img.get("src")).content)
                    # calls a method that returns a boolean if tesseract recognizes defined text, btw install tesseract-ocr
                    if(hasText("temp/" + img.get("src").rsplit("/", 1)[1][:9])):
                        # green tick
                        await msg.add_reaction('\U00002705')
                        # great for people with slow, country internet.  Love you Sky, no complaints!
                        async with chan.typing():
                            await chan.send(file=File("memes/" + random.choice(os.listdir("memes"))))
                    else:
                        await msg.add_reaction('\U0000274C')
        elif(msg.attachments):
            # we wanna yoink people's memes, that is all
            for attch in msg.attachments:
                url = attch.url
                filetype = url.rsplit(".", 1)[1]
                if(filetype in accepted):
                    print("Downloading " + url.rsplit("/", 1)[1])
                    r = requests.get(url)
                    with open("memes/" + url.rsplit("/", 1)[1], "wb+") as f:
                        f.write(r.content)
                        await msg.add_reaction('\U0001f44d')
    for x in os.listdir("temp"):
        # we don't want to keep the temp files made by the hasText() function
        os.remove("temp/" + x)


@bot.event
async def on_ready():
    if(not ready):
        if(not os.path.isdir("temp")):
            os.mkdir("temp")
        print("Started")
    else:
        # This is in place solely for that missing bug, if found call 01189998819991197253
        print("Why am I running again?!")
    # I did intend for memes to be downloaded from instagram but that would then rely on people not being pricks
    # This is why instaloader was downloaded in pip, you could set this up yourself but this code has not been tested with instaloader
    # Also a bug in the previous version has since disappeared, if you find it please let me know. I'm scared

def hasText(file):
    terms = ['MO', 'RE', 'MOR', 'ORE', 'MORE']
    img = imageio.get_reader(file)
    count = 0
    for frame in img:
        # greyscale gave better results in testing
        cv2.imwrite("temp/temp.jpg", frame)
        im = cv2.imread("temp/temp.jpg")
        grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        out = pytesseract.image_to_string(grey, config='--psm 6')
        for term in terms:
           if(term in out.upper()):
                return True
    return False

bot.run(api_keys["discord"])


