import logging
import aiosqlite
import discord
import json
import utils.database_cache
from discord.ext import commands


async def call_add_to_cache(self, ctx): # Decorator wouldn't take add_to_cache, so here we are making a function to call another function
    await utils.database_cache.add_to_cache(self.bot, ctx.guild)

class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logging.info(f"Joined {guild.name}")
        await create_config(self, guild)
        await self.bot.get_user(guild.owner_id).send("Thanks for inviting Coordy!\nRight now Coordy will be as useful as a vegetable, refer to the readme on how to set-up, configurate and use Coordy!\nFeel free to DM Sirspam#7765 if you have any issues with Coordy!\nhttps://github.com/Sirspam/Coordy-McCoordFace/blob/main/README.md")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logging.info(f"Left {guild.name}")
        del self.bot.config[str(guild.id)]
        async with aiosqlite.connect("database.db") as dab:
            await dab.execute("DELETE FROM guilds WHERE guild_id=?", (guild.id,))
        logging.info(f"{guild.name} removed from database")

    @commands.group(invoke_without_command=True, help="Posts the current configuration")
    @commands.has_permissions(administrator = True)
    @commands.before_invoke(call_add_to_cache)
    async def config(self, ctx):
        logging.info(f"Config invoked in {ctx.guild.name}")
        embed = discord.Embed(title=f"{ctx.guild.name} Config",)
        embed.add_field(
            name="Prefix",
            value=f"``{self.bot.config[ctx.guild.id]['prefix']}``",
            inline=True
        )
        embed.add_field(
            name="Lobby VC",
            value=ctx.guild.get_channel(self.bot.config[ctx.guild.id]["lobby_vc_id"]),
            inline=True
        )
        message=None
        if self.bot.config[ctx.guild.id]["beatkhana_id"] is not None:
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                json_data = json.loads(await resp.text())
                message = f"[{json_data[0]['name']}](https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']})"
        embed.add_field(
            name="BeatKhana Page",
            value=message,
            inline=False
        )
        message = str()
        for role in self.bot.config[ctx.guild.id]["coord_roles_ids"]:
            message = f"{message}{(ctx.guild.get_role(role)).mention} "
        if not message:
            message = "None"
        embed.add_field(
            name="Coordinator Roles",
            value=message,
            inline=True
        )
        message = str()
        for role in self.bot.config[ctx.guild.id]["ignored_roles_ids"]:
            message = f"{message}{(ctx.guild.get_role(role)).mention} "
        if not message:
            message = "None"
        embed.add_field(
            name="Ignored Roles",
            value=message,
            inline=False
        )
        await ctx.send(embed=embed)
        logging.info("config concluded")

    @config.command(help="Posts the current configuration in a raw format")
    @commands.before_invoke(call_add_to_cache)
    async def raw(self, ctx):
        logging.info(f"config raw invoked in {ctx.guild.name}")
        await ctx.send(self.bot.config[ctx.guild.id])
        logging.info("config raw concluded")

    @config.command(help="Creates a config for this guild")
    async def create(self, ctx):
        await create_config(ctx.guild)
        await ctx.message.add_reaction("✅")

    @config.command(help="Removes this guild from the config")
    async def remove(self, ctx):
        logging.info(f"Removing {ctx.guild.name} from config")
        del self.bot.config[ctx.guild.id]
        async with aiosqlite.connect("database.db") as dab:
            await dab.execute("DELETE FROM guilds WHERE guild_id=?", (ctx.guild.id,))
            await dab.commit()
        await ctx.message.add_reaction("✅")

    @config.command(help="Sets the bot's prefix for this guild")
    @commands.before_invoke(call_add_to_cache)
    async def set_prefix(self, ctx, *, prefix):
        logging.info(f"Recieved set_prefix {prefix} in {ctx.guild.name}")
        if prefix[:1]!='"' or prefix[-1:]!='"':
            raise commands.BadArgument
        self.bot.config[ctx.guild.id]["prefix"] = prefix.strip('"')
        async with aiosqlite.connect("database.db") as dab:
            await dab.execute("UPDATE guilds SET prefix=? WHERE guild_id=?", (prefix, ctx.guild.id))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("Prefix set")

    @config.command(help="Sets the lobby vc id for this guild")
    @commands.before_invoke(call_add_to_cache)
    async def set_lobby(self, ctx, lobby_id: int):
        logging.info(f"Recieved set_lobby {lobby_id} in {ctx.guild.name}")
        channel_object = ctx.guild.get_channel(lobby_id)
        if channel_object is None or isinstance(channel_object, discord.TextChannel):
            raise commands.BadArgument
        self.bot.config[ctx.guild.id]["lobby_vc_id"] = lobby_id
        async with aiosqlite.connect("database.db") as dab:
            await dab.execute("UPDATE guilds SET lobby_vc=? WHERE guild_id=?", (lobby_id, ctx.guild.id))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("lobby vc id set")

    @config.command(help="Sets the coordinator roles for this guild")
    @commands.before_invoke(call_add_to_cache)
    async def set_coords(self, ctx, *roles: int):
        logging.info(f"Recieved set_coords {roles} in {ctx.guild.name}")
        for role in roles:
            if ctx.guild.get_role(role) is None:
                raise commands.BadArgument
        self.bot.config[ctx.guild.id]["coord_roles_ids"] = list()
        async with aiosqlite.connect("database.db") as dab:
            for role in roles:
                self.bot.config[ctx.guild.id]["coord_roles_ids"].append(role)
                await dab.execute("INSERT INTO coord_roles (guild_id, role) VALUES (?,?)", (ctx.guild.id, role))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("coord roles set")

    @config.command(help="Sets the ignored roles for this guild")
    @commands.before_invoke(call_add_to_cache)
    async def set_ignored(self, ctx, *roles: int):
        logging.info(f"Recieved set_ignored {roles} in {ctx.guild.name}")
        for role in roles:
            if ctx.guild.get_role(role) is None:
                raise commands.BadArgument
        self.bot.config[ctx.guild.id]["ignored_roles_ids"] = list()
        async with aiosqlite.connect("database.db") as dab:
            await dab.execute("DELETE FROM ignored_roles WHERE guild_id=?", (ctx.guild.id,))
            for role in roles:
                self.bot.config[ctx.guild.id]["ignored_roles_ids"].append(role)
                await dab.execute("INSERT INTO ignored_roles (guild_id, role) VALUES (?,?)", (ctx.guild.id, role))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("ignored roles set")

    @config.command(help="Sets the ignored roles for this guild")
    @commands.before_invoke(call_add_to_cache)
    async def set_beatkhana(self, ctx, beatkhana_id: int):
        logging.info(f"Recieved set_beatkhana {beatkhana_id} in {ctx.guild.name}")
        async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{beatkhana_id}") as resp:
            if "Tournament Not Found" in await resp.text():
                raise commands.BadArgument
        self.bot.config[ctx.guild.id]["beatkhana_id"] = beatkhana_id
        async with aiosqlite.connect("database.db") as dab:
            await dab.execute("UPDATE guilds SET beatkhana=? WHERE guild_id=?", (beatkhana_id, ctx.guild.id))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("beatkhana id set")

def setup(bot):
    bot.add_cog(Configuration(bot))

async def create_config(guild):
        logging.info(f"Creating database row for {guild.name}")
        async with aiosqlite.connect("database.db") as dab:
            await dab.execute("INSERT INTO guilds (guild_id, prefix) VALUES (?,?)", (guild.id,"cc "))
            await dab.commit()
        logging.info(f"{guild.name} added to database")
