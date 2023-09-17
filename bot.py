import discord
from discord.ext import commands, tasks
import json
import requests
import os

# If results save location doesn't exist, make one.
if os.path.isdir('results'):
    pass
else:
    os.mkdir('results')

# Load settings.
with open("./config.json") as f:
    configData = json.load(f)

# Create variables
token = configData["BOT_TOKEN"]
prefix = configData["PREFIX"]
domains = configData["DOMAIN_LIST"]
api_token = configData["API_KEY"]
save_location = configData["SAVE_LOCATION"]
apireq = f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={api_token}&domainName="

# Create bot instance
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Bot is getting ready...")
    await bot.change_presence(activity=discord.Game(name=f"with cum."))
    print(f'{bot.user} is up!')

@bot.command()
async def start(ctx):
    await ctx.send("Scan Started!")
    check_domains.start(ctx)

@bot.command()
async def stop(ctx):
    check_domains.cancel()
    await ctx.send("Scan Stopped!")

@tasks.loop(minutes=60)
async def check_domains(ctx):
    await ctx.send("Scan Ongoing!")
    
    for domain in domains:
        # Get new results
        await ctx.send(f"{domain}: Fetching new results...")
        new_results= requests.get(f"{apireq}{domain}").json()
        await ctx.send(f"{domain}: Received new results.")

        # Check for new entries
        if os.path.exists(f"{save_location}{domain}_old.json"):
            await ctx.send(f"{domain}: Cross-referencing with old results...")
            with open(f'{save_location}{domain}_old.json', 'r') as f:
                old_results = json.load(f)
        
            for entry in new_results["result"]["records"]:
                subdomain = entry["domain"]
                if not any(old_entry['domain'] == subdomain for old_entry in old_results["result"]["records"]):
                    await ctx.send(f"New entry: {subdomain}")
        else:
            await ctx.send(f"{domain}: No old results found. Sending all new results.")
            for entry in new_results["result"]["records"]:
                subdomain = entry["domain"]
                await ctx.send(f"New entry: {subdomain}")
    
        # Save updated results
        await ctx.send(f"Saving new results to {save_location}{domain}_old.json...")
        with open(f'{save_location}{domain}_old.json', 'w') as f:
            json.dump(new_results, f, ensure_ascii=False, indent=4)
        await ctx.send(f"Saved new results to {save_location}{domain}_old.json.")
    
    await ctx.send("Scan Complete!")

bot.run(token)