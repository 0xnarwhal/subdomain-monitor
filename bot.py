import discord # Discord Library
from discord.ext import commands, tasks # Discord Extensions
import json # JSON Library. Used to read and write config.json file.
import requests # Used to send HTTP requests to the API.
import os # Used to verify files and directories.
import datetime # Used for logging.

# Check logs.txt existence
if not os.path.isfile("./logs.txt"):
    with open("./logs.txt", "w") as logs:
        logs.write(f"[{datetime.datetime.now()}] Logs file not found. Creating one...\n")
        logs.write(f"[{datetime.datetime.now()}] Logs file created. Bot starting...\n")
else: # If logs.txt exist, do nothing.
    with open("./logs.txt", "a") as logs:
        logs.write(f"[{datetime.datetime.now()}] Logs file created. Bot starting...\n")

# Check config.json existence
with open("./logs.txt", "a") as logs:
    logs.write(f"[{datetime.datetime.now()}] Checking config.json...\n")
    if os.path.isfile("./config.json"): # If config.json exist, load configuration.
        logs.write(f"[{datetime.datetime.now()}] config.json found. Loading configuration...\n")
        with open("./config.json") as config:
            configData = json.load(config)
            # Assign variables from config.json
            bot_token = configData["BOT_TOKEN"]
            prefix = configData["PREFIX"]
            domain_list = configData["DOMAIN_LIST"]
            api_key = configData["API_KEY"]
            save_location = configData["SAVE_LOCATION"]
            req_url = f"https://subdomains.whoisxmlapi.com/api/v1?apiKey={api_key}&domainName="
        logs.write(f"[{datetime.datetime.now()}] Configuration loaded.\n")
    else: # If config.json does not exist, create a template config.json and exit.
        logs.write(f"[{datetime.datetime.datetime.now()}] config.json not found. Creating sample...\n")
        config_template =   {
                                "BOT_TOKEN": "<DISCORD_BOT_TOKEN>", 
                                "PREFIX": "!",
                                "DOMAIN_LIST": ["google.com","bing.com"],
                                "SAVE_LOCATION": "./results",
                                "API_KEY": "<WHOISXML_API_KEY>"
                            }
        with open("./config.json", "w") as config:
            json.dump(config_template, config, indent=4)
        logs.write(f"[{datetime.datetime.now()}] Sample config.json created. Exiting...\n")
        exit()

# If results save location doesn't exist, make one.
with open("./logs.txt", "a") as logs:
    logs.write(f"[{datetime.datetime.now()}] Checking save location...\n")
    if os.path.isdir(save_location):
        logs.write(f"[{datetime.datetime.now()}] Save location found. Continuing...\n")
    else:
        logs.write(f"[{datetime.datetime.now()}] Save location not found. Creating one...\n")
        os.mkdir(save_location)
        logs.write(f"[{datetime.datetime.now()}] Save location created.\n")

# Create bot instance
bot = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())

@bot.event
async def on_ready():
    with open("./logs.txt", "a") as logs:
        logs.write(f"[{datetime.datetime.now()}] Bot starting...\n")
        await bot.change_presence(activity=discord.Game(name=f"with cum.")) # Just for fun. Might want to remove this :)
        logs.write(f"[{datetime.datetime.now()}] Bot has successfully started!\n")

# Commands to start and stop the scan task.
@bot.command()
async def start(ctx):
    with open("./logs.txt", "a") as logs:
        logs.write(f"[{datetime.datetime.now()}] {ctx.author} has started the scan task.\n")
        check_domains.start(ctx)


@bot.command()
async def stop(ctx):
    with open("./logs.txt", "a") as f:
        check_domains.cancel()
        logs.write(f"[{datetime.datetime.now()}] {ctx.author} has stopped the scan task.\n")

# Scan task that runs every 168 hours or 1 week.
@tasks.loop(hours=168)
async def check_domains(ctx):
    with open("./logs.txt", "a") as logs:
        logs.write(f"[{datetime.datetime.now()}] Scan task has started.\n")
        
        # Go through each domain in the list.
        for domain in domain_list:
            # Fetch new results
            logs.write(f"[{datetime.datetime.now()}] Fetching new results for {domain}...\n")
            new_results = requests.get(f"{req_url}{domain}").json()
            logs.write(f"[{datetime.datetime.now()}] Received new results for {domain}.\n")

            # Check if old results exist. If not, print out the new results and save them to a file as old results.
            # If old results exist, cross-reference them with new results and print out the new results that are not in the old results.
            if os.path.exists(f"{save_location}/{domain}_old.json"):
                logs.write(f"[{datetime.datetime.now()}] Old results found for {domain}. Cross-referencing with new results...\n")
                with open(f'{save_location}{domain}_old.json', 'r') as oldData:
                    old_results = json.load(oldData)
                for entry in new_results["result"]["records"]:
                    subdomain = entry["domain"]
                    if not any(old_entry['domain'] == subdomain for old_entry in old_results["result"]["records"]):
                        logs.write(f"[{datetime.datetime.now()}] New entry found: {subdomain}. Sending a notification to Discord...\n")
                        embed=discord.Embed(title=f"http://{subdomain}", url=f"http://{subdomain}", description=f"A new subdomain has been found. Performing a small test should do it >:)", color=0xFF5733)
                        await ctx.send(embed=embed)
            else:
                logs.write(f"[{datetime.datetime.now()}] No old results found for {domain}. Printing new results to Discord...\n")
                for entry in new_results["result"]["records"]:
                    subdomain = entry["domain"]
                    embed=discord.Embed(title=f"http://{subdomain}", url=f"http://{subdomain}", description=f"A new subdomain has been found. Performing a small test should do it >:)", color=0xFF5733)
                    await ctx.send(embed=embed)
        
            # Save updated results to a file.
            logs.write(f"[{datetime.datetime.now()}] Saving new results to {save_location}/{domain}_old.json...\n")
            with open(f'{save_location}/{domain}_old.json', 'w') as oldData:
                json.dump(new_results, oldData, ensure_ascii=False, indent=4)
            logs.write(f"[{datetime.datetime.now()}] Saved new results to {save_location}/{domain}_old.json.\n")
        
        logs.write(f"[{datetime.datetime.now()}] Scan task has ended.\n")

bot.run(bot_token)