import logging
import aiosqlite
import cogs.configuration
from discord.ext import tasks

cached = list()

# This system could be improved to delete a guild 30 minutes after it was created, instead of deleting the oldest one every 30 mintues.
@tasks.loop(minutes=30)
async def clean_cache():
    logging.info(f"Cleaning cache ({cached})")
    if not cached:
        return logging.info("Cache empty")
    del cached[0]
    logging.info("Successfully cleaned cache")
clean_cache.start()

async def add_to_cache(bot, guild):
    logging.info(f"Adding {guild.name} to cache")
    if guild.id in bot.config:
        return logging.info("guild already in cache")
    async with aiosqlite.connect("database.db") as dab:
        async with dab.execute("SELECT * FROM guilds WHERE guild_id = ?", (guild.id,)) as cursor:
            guilds = await cursor.fetchone()
            if guilds is None:
                await cogs.configuration.create_config(guild)
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
    if guild.id in cached:
        cached.remove(guild.id)
    cached.append(guild.id)