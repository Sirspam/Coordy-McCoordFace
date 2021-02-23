# https://discord.com/api/oauth2/authorize?client_id=813699805150838795&permissions=29371392&scope=bot

import discord
import os
import logging
from discord.ext import commands
from dotenv import load_dotenv
from utils import jskp

cwd = os.getcwd()
load_dotenv(f"{cwd}/config.env")
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!b ",intents=intents,case_insensitive=True,allowed_mentions=discord.AllowedMentions(replied_user=False))
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)


initial_cogs = [
    "jishaku",
    "cogs.error_handler",
    "cogs.coord"
]

for cog in initial_cogs:
    try:
        client.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")


async def on_ready():
    logging.info('Bot has successfully launched as {0.user}'.format(client))


client.run(os.getenv("TOKEN"))