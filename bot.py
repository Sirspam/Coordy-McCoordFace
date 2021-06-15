import discord
import os
import logging
import aiohttp
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from sqlite3 import connect


logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', level=logging.INFO)

load_dotenv(os.getcwd()+"/.env")

with connect("database.db") as dab:
    dab.execute("CREATE TABLE IF NOT EXISTS guilds (guild_id BIGINT PRIMARY KEY, prefix TEXT, lobby_vc BIGINT, beatkhana BIGINT)")
    dab.execute("CREATE TABLE IF NOT EXISTS coord_roles (guild_id BIGINT REFERENCES guilds (guild_id) ON DELETE CASCADE, role BIGINT, PRIMARY KEY (guild_id, role))")
    dab.execute("CREATE TABLE IF NOT EXISTS ignored_roles (guild_id BIGINT REFERENCES guilds (guild_id) ON DELETE CASCADE, role BIGINT, PRIMARY KEY (guild_id, role))")

async def prefix(bot, ctx):
        try:
            return bot.config[str(ctx.guild.id)]["prefix"]
        except KeyError:
            return "cc "


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=prefix, max_messages = None, intents=intents, case_insensitive=True, allowed_mentions=discord.AllowedMentions(replied_user=False))
bot.session = aiohttp.ClientSession(loop=asyncio.get_event_loop(), headers={"User-Agent": "Coordy McCoordFace (https://github.com/Sirspam/Coordy-McCoordFace)"})
bot.config = dict()


initial_cogs = [
    "jishaku",
    "cogs.beatkhana",
    "cogs.beatsaver",
    "cogs.configuration",
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
    logging.info(f"Bot has successfully launched as {bot.user}")


bot.run(os.getenv("TOKEN"))
