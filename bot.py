import discord
import os
import logging
import json
import aiohttp
import asyncio
from discord.ext import commands
from dotenv import load_dotenv


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', level=logging.INFO)

load_dotenv(os.getcwd()+"/.env")

try:
    config = (json.load(open("config.json",)))
except FileNotFoundError:
    logging.warning("config.json not found. Creating config")
    json.dump(dict(),open("config.json","w"))
    config = (json.load(open("config.json",)))

async def prefix(bot, ctx):
        try:
            return bot.config[str(ctx.guild.id)]["prefix"]
        except:
            return "cc "


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, max_messages = None, intents=intents, case_insensitive=True, allowed_mentions=discord.AllowedMentions(replied_user=False))
bot.session = aiohttp.ClientSession(loop=asyncio.get_event_loop(), headers={"User-Agent": "Coordy McCoordFace (https://github.com/Sirspam/Coordy-McCoordFace)"})
bot.config = config


initial_cogs = [
    "jishaku",
    "cogs.beatsaver",
    "cogs.coord",
    "cogs.error_handler",
    "cogs.general",
    "cogs.waifu"
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
