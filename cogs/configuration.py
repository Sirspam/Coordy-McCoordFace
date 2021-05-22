import json
import logging
from discord.ext import commands


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
        json.dump(self.bot.config,open("config.json","w"))
        logging.info(f"{guild.name} removed from config json")

    @commands.group(invoke_without_command=True, help="Posts the current configuration")
    @commands.has_permissions(administrator = True)
    async def config(self, ctx):
        await ctx.send(self.bot.config[str(ctx.guild.id)])

    @config.command(help="Creates a config for this guild")
    async def create(self, ctx):
        await create_config(self, ctx.guild)
        await ctx.message.add_reaction("✅")

    @config.command(help="Removes this guild from the config")
    async def remove(self, ctx):
        logging.info(f"Removing {ctx.guild.name} from config")
        del self.bot.config[str(ctx.guild.id)]
        json.dump(self.bot.config,open("config.json","w"))
        await ctx.message.add_reaction("✅")

    @config.command(help="Sets the bot's prefix for this guild")
    async def set_prefix(self, ctx, *, prefix):
        logging.info(f"Recieved set_prefix {prefix} in {ctx.guild.name}")
        if prefix[:1]!='"' or prefix[-1:]!='"':
            raise commands.BadArgument
        self.bot.config[str(ctx.guild.id)]["prefix"] = prefix.strip('"')
        json.dump(self.bot.config,open("config.json","w"))
        await ctx.message.add_reaction("✅")
        logging.info("Prefix set")

    @config.command(help="Sets the lobby vc id for this guild")
    async def set_lobby(self, ctx, lobby_id: int):
        logging.info(f"Recieved set_lobby {lobby_id} in {ctx.guild.name}")
        if ctx.guild.get_channel(lobby_id) is None:
            raise commands.BadArgument
        self.bot.config[str(ctx.guild.id)]["lobby_vc_id"] = lobby_id
        json.dump(self.bot.config,open("config.json","w"))
        await ctx.message.add_reaction("✅")
        logging.info("lobby vc id set")

    @config.command(help="Sets the coordinator roles for this guild")
    async def set_coords(self, ctx, *roles: int):
        logging.info(f"Recieved set_coords {roles} in {ctx.guild.name}")
        self.bot.config[str(ctx.guild.id)]["coord_roles_ids"] = list()
        for role in roles:
            if ctx.guild.get_role(role) is None:
                raise commands.BadArgument
            self.bot.config[str(ctx.guild.id)]["coord_roles_ids"].append(role)
            json.dump(self.bot.config,open("config.json","w"))
        await ctx.message.add_reaction("✅")
        logging.info("coord roles set")

    @config.command(help="Sets the ignored roles for this guild")
    async def set_ignored(self, ctx, *roles: int):
        logging.info(f"Recieved set_ignored {roles} in {ctx.guild.name}")
        self.bot.config[str(ctx.guild.id)]["ignored_roles"] = list()
        for role in roles:
            if ctx.guild.get_role(role) is None:
                raise commands.BadArgument
            self.bot.config[str(ctx.guild.id)]["ignored_roles"].append(role)
            json.dump(self.bot.config,open("config.json","w"))
        await ctx.message.add_reaction("✅")
        logging.info("ignored roles set")

def setup(bot):
    bot.add_cog(Configuration(bot))

async def create_config(self, guild):
        logging.info(f"Creating config for {guild.name}")
        self.bot.config[str(guild.id)]={
            "prefix": "cc ",
            "lobby_vc_id":None,
            "coord_roles_ids":[None],
            "ignored_roles":[None]
        }
        json.dump(self.bot.config,open("config.json","w"))
        logging.info(f"{guild.name} added to config json")
