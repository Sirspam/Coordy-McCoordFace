import discord
import os
import logging
import json
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv(os.getcwd()+"/.env")


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=json.load(open("config.json",))["prefix"], max_messages = None, intents=intents, case_insensitive=True)
logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', level=logging.INFO)


initial_cogs = [
    "jishaku",
    "cogs.error_handler",
    "cogs.coord",
    "cogs.neko",
    "cogs.text"
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")


@bot.event
async def on_ready():
    logging.info('Bot has successfully launched as {0.user}'.format(bot))


bot.run(os.getenv("TOKEN"))