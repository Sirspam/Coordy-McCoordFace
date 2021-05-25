import discord
from discord.ext import commands
from functools import partial


def guild_coord_role_check(): # haha I certainly didn't just steal and slightly alter the has_any_role function from the discord module :tf:
    def predicate(ctx):
        if not isinstance(ctx.channel, discord.abc.GuildChannel):
            raise commands.NoPrivateMessage
        if ctx.author.guild_permissions.administrator is True:
            return True
        getter = partial(discord.utils.get, ctx.author.roles)
        if any(getter(id=item) is not None if isinstance(item, int) else getter(name=item) is not None for item in ctx.bot.config[str(ctx.guild.id)]["coord_roles_ids"]):
            return True
        raise commands.MissingPermissions("Coordinator Role")
    return commands.check(predicate)