# Subdomain Monitoring Bot

## Table of Contents

1. About the Project
2. Getting Started
3. Usage
4. Future QOL Improvements
5. License
6. Contact

## About the Project

This is a simple bot that monitors the subdomains of a given domain and reports for any changes in the subdomains. It is built using the Python programming language and the Requests module. The bot is designed to be run on a server that you are hosting. I recommend using a VPS or dedicated server such as DigitalOcean (which is what I used).

The bot will perform the following tasks every week upon running:

1. Monitor the subdomains of a given domain.
2. Report any changes in the subdomains Through a notification through the seleted Discord text channel.
3. Log updated subdomains to a file.

## Getting Started

To get a local copy up and running follow these simple steps. This assumes you have Python 3.8 or higher installed on your machine.

### Installation

- Clone the repository.
- OPTIONAL: Create a virtual environment.

```bash
python3 -m venv venv
source venv/bin/activate
```

- Install the required modules.

```bash
pip install -r requirements.txt
```

- Create a file called `config.json` and add the following template and fill in the required information.

```json
{
    "BOT_TOKEN": "<DISCORD_BOT_TOKEN>", 
    "PREFIX": "!",
    "DOMAIN_LIST": ["google.com","bing.com"],
    "SAVE_LOCATION": "./results",
    "API_KEY": "<WHOISXML_API_KEY>"
}
```

## Usage

- Run the bot.

```bash
python3 bot.py
```

- Run `!start` commmand in preffered Discord text channel to start monitoring.

## Future QOL Improvements

- Utilize embedded messages for better formatting instead of individual messages. - Done
- Logs functionality created. - Done
- Add more functionality to the bot.
- Add more error handling.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Amir Adrian - <amiradrian@protonmail.com>
