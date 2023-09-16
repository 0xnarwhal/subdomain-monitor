import discord
from discord.ext import commands, tasks
import json
import os

# Load current settings.
with open("./config.json") as f:
    configData = json.load(f)

token = configData["Token"]
prefix = configData["Prefix"]
domains = configData["Domains"].split(",")
chat_id = int(configData["ChatID"])
api_token = configData["APIToken"]

# Create Bot and Client Instance
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Bot is ready.")
    await bot.change_presence(activity=discord.Game(name=f"with cum."))

bot.run(token)