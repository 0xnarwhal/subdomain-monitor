import discord
from discord.ext import commands, tasks
import json
import requests
import os

# Check if config.json exist. If not, will create a template config.json and exit.
if os.path.isfile("./config.json"):
    with open("./config.json") as f:
        configData = json.load(f)
else:
    config_template =   {
                            "BOT_TOKEN": "<DISCORD_BOT_TOKEN>", 
                            "PREFIX": "!",
                            "DOMAIN_LIST": ["google.com","bing.com"],
                            "SAVE_LOCATION": "./results",
                            "API_KEY": "<WHOISXML_API_KEY>"
                        }
    with open("./config.json", "w") as f:
        json.dump(config_template, f, indent=4)
    print("'config.json' file not found. Read the README.md file for instructions. 'config.json' file template has been created. Edit as you see fit. Exiting...")
    exit()

# Load config data from config.json file and assign them to variables.
bot_token = configData["BOT_TOKEN"]
prefix = configData["PREFIX"]
domain_list = configData["DOMAIN_LIST"]
api_key = configData["API_KEY"]
save_location = configData["SAVE_LOCATION"]
req_url = f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={api_key}&domainName="

# If results save location doesn't exist, make one.
if os.path.isdir(save_location):
    print(f"Results will be saved to {save_location}")
else:
    print(f"{save_location} doesn't exist. Creating one...")
    os.mkdir(save_location)
    print(f"Results will be saved to {save_location}")

# Create bot instance
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

# Logging message when bot is online.
@bot.event
async def on_ready():
    print("Bot is getting ready...")
    await bot.change_presence(activity=discord.Game(name=f"with cum.")) # Just for fun. Might want to remove this :)
    print(f'{bot.user} is up and running!')

# Commands to start and stop the scan task.
@bot.command()
async def start(ctx):
    check_domains.start(ctx)
    await ctx.send("Scan Started!")

@bot.command()
async def stop(ctx):
    check_domains.cancel()
    await ctx.send("Scan Stopped!")

# Scan task that runs every 168 hours or 1 week.
@tasks.loop(hours=168)
async def check_domains(ctx):
    await ctx.send("Scan is running...")
    
    # Go through each domain in the list.
    for domain in domain_list:
        
        # Fetch new results
        await ctx.send(f"{domain}: Fetching new results...")
        new_results = requests.get(f"{req_url}{domain}").json()
        await ctx.send(f"{domain}: Received new results.")

        # Check if old results exist. If not, print out the new results and save them to a file as old results.
        # If old results exist, cross-reference them with new results and print out the new results that are not in the old results.
        if os.path.exists(f"{save_location}/{domain}_old.json"):
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
        await ctx.send(f"Saving new results to {save_location}/{domain}_old.json...")
        with open(f'{save_location}/{domain}_old.json', 'w') as f:
            json.dump(new_results, f, ensure_ascii=False, indent=4)
        await ctx.send(f"Saved new results to {save_location}/{domain}_old.json.")
    
    await ctx.send("Scan Complete!")

bot.run(bot_token)