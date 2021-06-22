import logging
from asyncio import get_event_loop
from os import getcwd, getenv
from sqlite3 import connect

from discord import Intents, AllowedMentions
from aiohttp import ClientSession
from dotenv import load_dotenv

from discord.ext.commands import Bot

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s: %(message)s', level=logging.INFO)

load_dotenv(getcwd()+"/.env")

with connect("database.db") as dab:
    dab.execute("CREATE TABLE IF NOT EXISTS guilds (guild_id INTEGER PRIMARY KEY, prefix TEXT DEFAULT 'cc ', lobby_vc INTEGER, beatkhana INTEGER)")
    dab.execute("CREATE TABLE IF NOT EXISTS coord_roles (guild_id INTEGER REFERENCES guilds (guild_id) ON DELETE CASCADE, role INTEGER, PRIMARY KEY (guild_id, role))")
    dab.execute("CREATE TABLE IF NOT EXISTS ignored_roles (guild_id INTEGER REFERENCES guilds (guild_id) ON DELETE CASCADE, role INTEGER, PRIMARY KEY (guild_id, role))")

async def prefix(bot, ctx):
        try:
            return bot.config[str(ctx.guild.id)]["prefix"]
        except KeyError:
            return "cc "

intents = Intents.default()
intents.members = True
bot = Bot(command_prefix=prefix, help_command=None, max_messages=None, intents=intents, case_insensitive=True, allowed_mentions=AllowedMentions(replied_user=False))
bot.config = dict()

initial_cogs = [
    "jishaku",
    "cogs.beatkhana",
    "cogs.beatsaver",
    "cogs.configuration",
    "cogs.coord",
    "cogs.error_handler",
    "cogs.general",
    "cogs.help",
    "cogs.waifu",
    "utils.database_management" # Not really a cog but needed for task loop
]

for cog in initial_cogs:
    try:
        bot.load_extension(cog)
        logging.info(f"Successfully loaded {cog}")
    except Exception as e:
        logging.error(f"Failed to load cog {cog}: {e}")


@bot.event
async def on_ready():
    bot.session = ClientSession(loop=get_event_loop(), headers={"User-Agent": "Coordy McCoordFace (https://github.com/Sirspam/Coordy-McCoordFace)"})
    logging.info(f"Bot has successfully launched as {bot.user}")

@bot.before_invoke
async def before_invoke(ctx):
    logging.info(f"Invoked {ctx.command} in {ctx.guild.name} by {ctx.author.name}\nArgs: {ctx.args}" )

@bot.after_invoke
async def after_invoke(ctx):
    logging.info(f"Concluded {ctx.command}")


bot.run(getenv("TOKEN"))
