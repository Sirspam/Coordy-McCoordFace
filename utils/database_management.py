import logging

from aiosqlite import connect

from discord.ext import commands, tasks


cached = list()

# This system could be improved to delete a guild 30 minutes after it was created, instead of deleting the oldest one every 30 mintues.
class CleanCacheLoop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.clean_cache.start()
    
    @tasks.loop(minutes=30)
    async def clean_cache(self):
        logging.info(f"Cleaning cache ({cached})")
        if not cached:
            return logging.info("Cache empty")
        del self.bot.config[cached[0]]
        del cached[0]
        logging.info("Successfully cleaned cache")

    @clean_cache.before_loop
    async def before_clean(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(CleanCacheLoop(bot))


async def add_to_cache(bot, guild):
    logging.info(f"Adding {guild.name} to cache")
    if guild.id in bot.config:
        return logging.info("guild already in cache")
    async with connect("database.db") as dab:
        async with dab.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild.id,)) as cursor:
            guilds = await cursor.fetchone()
            if guilds is None:
                logging.info("Guild not in database!")
                await create_config(guild)
                return await add_to_cache(bot, guild)
        async with dab.execute("SELECT role FROM coord_roles WHERE guild_id = ?", (guild.id,)) as cursor:
            coord_roles = list()
            for role in await cursor.fetchall():
                coord_roles.append(role[0])
        async with dab.execute("SELECT role FROM ignored_roles WHERE guild_id = ?", (guild.id,)) as cursor:
            ignored_roles = list()
            for role in await cursor.fetchall():
                ignored_roles.append(role[0])
    bot.config[guild.id]={
        "prefix": guilds[1],
        "lobby_vc_id": guilds[2],
        "beatkhana_id": guilds[3],
        "coord_roles_ids": coord_roles,
        "ignored_roles_ids": ignored_roles
    }
    cached.append(guild.id)

async def create_config(guild):
        logging.info(f"Creating database row for {guild.name}")
        async with connect("database.db") as dab:
            await dab.execute("INSERT INTO guilds (guild_id) VALUES (?)", (guild.id,))
            await dab.commit()
        logging.info(f"{guild.name} added to database")