import logging
from json import loads

from aiosqlite import connect
from discord import Embed, TextChannel, VoiceChannel, Colour

from discord.ext import commands
from utils.database_management import add_to_cache, create_config
from utils.role_checks import admin_or_bot_owner_check


class Configuration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def cog_check(self, ctx):
        await add_to_cache(self.bot, ctx.guild)
        return True


    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logging.info(f"Joined {guild.name}")
        await create_config(self, guild)
        await self.bot.get_user(guild.owner_id).send("Thanks for inviting Coordy!\nRight now Coordy will be as useful as a vegetable, refer to the readme on how to set-up, configurate and use Coordy!\nFeel free to DM Sirspam#7765 if you have any issues with Coordy!\nhttps://github.com/Sirspam/Coordy-McCoordFace/blob/main/README.md")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logging.info(f"Left {guild.name}")
        del self.bot.config[guild.id]
        async with connect("database.db") as dab:
            await dab.execute("DELETE FROM guilds WHERE guild_id=?", (guild.id,))
        logging.info(f"{guild.name} removed from database")

    @commands.group(invoke_without_command=True, help="Posts the current configuration")
    @admin_or_bot_owner_check()
    async def config(self, ctx):
        logging.info(f"Config invoked in {ctx.guild.name}")
        embed = Embed(
            title=f"{ctx.guild.name} Config",
            colour=Colour.light_grey()
        )
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
                json_data = loads(await resp.text())
                embed.add_field(
                    name="BeatKhana Page",
                    value=f"[{json_data[0]['name']}](https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']})",
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
    async def raw(self, ctx):
        logging.info(f"config raw invoked in {ctx.guild.name}")
        await ctx.send(self.bot.config[ctx.guild.id])
        logging.info("config raw concluded")

    @config.command(help="Removes this guild from the config")
    async def remove(self, ctx):
        logging.info(f"Removing {ctx.guild.name} from config")
        del self.bot.config[ctx.guild.id]
        async with connect("database.db") as dab:
            await dab.execute("PRAGMA foreign_keys = TRUE")
            await dab.execute("DELETE FROM guilds WHERE guild_id=?", (ctx.guild.id,))
            await dab.commit()
        await ctx.message.add_reaction("✅")

    @config.command(help="Attempts to automatically setup config")
    async def auto(self, ctx):
        typical_names = {
            "lobby_vc": ["lobby", "waiting room"],
            "coordinator_roles": ["coordinator", "staff"],
            "ignored_roles": ["caster", "spectator"]
        }
        results = {
            "Lobby VC": (False, "Not Found"),
            "BeatKhana Page": (False, "Not Found"),
            "Coordinator Roles": (False, "Not Found"),
            "Ignored Roles": (False, "Not Found")
        }
        async with ctx.channel.typing():
            logging.info("Attempting to find lobby_vc")
            for channel in ctx.guild.channels:
                if isinstance(channel, VoiceChannel) and channel.name.lower() in typical_names["lobby_vc"]:
                    logging.info(f"Using {channel.name}")
                    results["Lobby VC"] = (True, channel.id)
                    break
            logging.info("Attempting to find coordinator and ignored roles")
            coord_ids = list()
            ignored_ids = list()
            for role in ctx.guild.roles:
                if role.name.lower() in typical_names["coordinator_roles"]:
                    logging.info(f"Appending {role.name} to coord list")
                    coord_ids.append(role.id)
                if role.name.lower() in typical_names["ignored_roles"]:
                    logging.info(f"Appending {role.name} to ignored list")
                    ignored_ids.append(role.id)
            if coord_ids:
                results["Coordinator Roles"] = (True, coord_ids)
            if ignored_ids:
                results["Ignored Roles"] = (True, ignored_ids)
            del coord_ids, ignored_ids # Because this'll certainly save tons of space in the memory! :tf:
            logging.info("Attempting to find beatkhana page")
            async with self.bot.session.get(f"https://beatkhana.com/api/tournaments") as resp:
                for tournament in loads(await resp.text()):
                    if tournament["name"].lower() == ctx.guild.name.lower():
                        logging.info(f"Using {tournament['name']}")
                        results["BeatKhana Page"] = (True, tournament["tournamentId"])
            if results["BeatKhana Page"][0] is False:
                logging.info("No main tournament found. Checking mini-tournaments")
                async with self.bot.session.get(f"https://beatkhana.com/api/mini-tournaments") as resp:
                    for tournament in loads(await resp.text()):
                        if tournament["name"].lower() == ctx.guild.name.lower():
                            logging.info(f"Using {tournament['name']}")
                            results["BeatKhana Page"] = (True, tournament["tournamentId"])
            # I don't like this but I can't think of a better way to do it :(
            async with connect("database.db") as dab:
                if results["Lobby VC"][0] is True:
                    self.bot.config[ctx.guild.id]["lobby_vc_id"] = results["Lobby VC"][1]
                    await dab.execute("UPDATE guilds SET lobby_vc=? WHERE guild_id=?", (results["Lobby VC"][1], ctx.guild.id))
                if results["BeatKhana Page"][0] is True:
                    self.bot.config[ctx.guild.id]["beatkhana_id"] = results["BeatKhana Page"][1]
                    await dab.execute("UPDATE guilds SET beatkhana=? WHERE guild_id=?", (results["BeatKhana Page"][1], ctx.guild.id))
                if results["Coordinator Roles"][0] is True:
                    self.bot.config[ctx.guild.id]["coord_roles_ids"] = list()
                    await dab.execute("DELETE FROM coord_roles WHERE guild_id=?", (ctx.guild.id,))
                    for role in results["Coordinator Roles"][1]:
                        self.bot.config[ctx.guild.id]["coord_roles_ids"].append(role)
                        await dab.execute("INSERT INTO coord_roles (guild_id, role) VALUES (?,?)", (ctx.guild.id, role))
                if results["Ignored Roles"][0] is True:
                    self.bot.config[ctx.guild.id]["ignored_roles_ids"] = list()
                    await dab.execute("DELETE FROM ignored_roles WHERE guild_id=?", (ctx.guild.id,))
                    for role in results["Ignored Roles"][1]:
                        self.bot.config[ctx.guild.id]["ignored_roles_ids"].append(role)
                        await dab.execute("INSERT INTO ignored_roles (guild_id, role) VALUES (?,?)", (ctx.guild.id, role))
                await dab.commit()
            result_embed = Embed(
                title="Results",
                colour=Colour.light_grey()
            )
            for result in results:
                result_embed.add_field(
                    name=result,
                    value=results[result][1],
                    inline=False
                )
        await ctx.send(embed=result_embed)


    @config.command(help="Sets the bot's prefix for this guild")
    async def set_prefix(self, ctx, *, prefix):
        logging.info(f"Recieved set_prefix {prefix} in {ctx.guild.name}")
        if prefix[:1]!='"' or prefix[-1:]!='"':
            raise commands.BadArgument
        self.bot.config[ctx.guild.id]["prefix"] = prefix.strip('"')
        async with connect("database.db") as dab:
            await dab.execute("UPDATE guilds SET prefix=? WHERE guild_id=?", (prefix, ctx.guild.id))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("Prefix set")

    @config.command(help="Sets the lobby vc id for this guild")
    async def set_lobby(self, ctx, lobby_id: int):
        logging.info(f"Recieved set_lobby {lobby_id} in {ctx.guild.name}")
        channel_object = ctx.guild.get_channel(lobby_id)
        if channel_object is None or isinstance(channel_object, TextChannel):
            raise commands.BadArgument
        self.bot.config[ctx.guild.id]["lobby_vc_id"] = lobby_id
        async with connect("database.db") as dab:
            await dab.execute("UPDATE guilds SET lobby_vc=? WHERE guild_id=?", (lobby_id, ctx.guild.id))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("lobby vc id set")

    @config.command(help="Sets the coordinator roles for this guild")
    async def set_coords(self, ctx, *roles: int):
        logging.info(f"Recieved set_coords {roles} in {ctx.guild.name}")
        for role in roles:
            if ctx.guild.get_role(role) is None:
                raise commands.BadArgument
        self.bot.config[ctx.guild.id]["coord_roles_ids"] = list()
        async with connect("database.db") as dab:
            await dab.execute("DELETE FROM coord_roles WHERE guild_id=?", (ctx.guild.id,))
            for role in roles:
                self.bot.config[ctx.guild.id]["coord_roles_ids"].append(role)
                await dab.execute("INSERT INTO coord_roles (guild_id, role) VALUES (?,?)", (ctx.guild.id, role))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("coord roles set")

    @config.command(help="Sets the ignored roles for this guild")
    async def set_ignored(self, ctx, *roles: int):
        logging.info(f"Recieved set_ignored {roles} in {ctx.guild.name}")
        for role in roles:
            if ctx.guild.get_role(role) is None:
                raise commands.BadArgument
        self.bot.config[ctx.guild.id]["ignored_roles_ids"] = list()
        async with connect("database.db") as dab:
            await dab.execute("DELETE FROM ignored_roles WHERE guild_id=?", (ctx.guild.id,))
            for role in roles:
                self.bot.config[ctx.guild.id]["ignored_roles_ids"].append(role)
                await dab.execute("INSERT INTO ignored_roles (guild_id, role) VALUES (?,?)", (ctx.guild.id, role))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("ignored roles set")

    @config.command(help="Sets the beatkhana page for this guild")
    async def set_beatkhana(self, ctx, beatkhana_id: int):
        logging.info(f"Recieved set_beatkhana {beatkhana_id} in {ctx.guild.name}")
        async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{beatkhana_id}") as resp:
            if "Tournament Not Found" in await resp.text():
                raise commands.BadArgument
        self.bot.config[ctx.guild.id]["beatkhana_id"] = beatkhana_id
        async with connect("database.db") as dab:
            await dab.execute("UPDATE guilds SET beatkhana=? WHERE guild_id=?", (beatkhana_id, ctx.guild.id))
            await dab.commit()
        await ctx.message.add_reaction("✅")
        logging.info("beatkhana id set")

def setup(bot):
    bot.add_cog(Configuration(bot))
