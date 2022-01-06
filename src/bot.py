import discord
import os
import json
from dotenv import load_dotenv, find_dotenv
from test_selenium import get_data

PREFIX = "%"




def gen_data(kwd):

    try:
        with open("data.json") as file:
            data = json.load(file)
            return dict(data[kwd.strip()])
    except:
        return {"dataloss" : "NO data found. Accountant Vader betrayed you."}


def get_list():
    comps = []
    try:
        with open("data.json") as file:
            data = json.load(file)
            for x in data.items():
                comps.append(x[0])
        return comps

    except:
        return ['No Stocks active rightnow']
                


client = discord.Client()

@client.event
async def on_ready():
    print("Accountant vader has logged in!")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(PREFIX):
        
        if message.content.__contains__("list"):
            # LISTING ALL STOCKS
            await message.reply(os.environ.get("ENTRY_LIST"))
            get_data()
            lit = get_list()
            i = 1
            for x in lit:
                await message.channel.send(f"{i} : {x}")
                i+=1
            await message.channel.send(os.environ.get("EXIT_TXT"))


        elif message.content.__contains__("geninfo"):
            # LISTING INFO OF A GIVEN STOCK
            await message.reply(os.environ.get("ENTRY_GET"))
            get_data()
            print("OK")
            kwd = message.content.replace(PREFIX + "geninfo","").strip()
            y = gen_data(kwd=kwd)
            if not "dataloss" in y:
                await message.channel.send(f"Data for {kwd}: ")
                for x in y.items():
                    await message.channel.send(f"                       {x[0]}  :  {x[1]}")
            else:
                await message.channel.send("No Stock with this keyword exists")
            await message.reply(os.environ.get('EXIT_TXT'))
            


load_dotenv(find_dotenv())
client.run(os.environ.get("TOKEN"))