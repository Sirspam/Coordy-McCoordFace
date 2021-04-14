import math
import logging
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logging.info(f"on_command_error triggered")
        if isinstance(error, commands.BadArgument):
            logging.info("BadArgument handler ran")
            return await ctx.send("You've given a bad argument", delete_after=20)

        elif isinstance(error, commands.CommandNotFound):
            logging.info("CommandNotFound handler ran")
            return await ctx.send("Command not found", delete_after=20)

        elif isinstance(error, commands.BotMissingPermissions):
            logging.info(f"BotMissingPermissions handler ran - {error.missing_perms[0]}")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms[0]}", delete_after=20)

        elif isinstance(error, commands.NotOwner):
            logging.info("NotOwner handler ran")
            return await ctx.send('Owner only command', delete_after=20)

        elif isinstance(error, commands.CommandOnCooldown):
            logging.info("CommandOnCooldown handler ran")
            return await ctx.send(f"Command on cooldown, ``{math.ceil(error.retry_after)} seconds``", delete_after=int(math.ceil(error.retry_after)))

        elif isinstance(error, commands.MissingRequiredArgument):
            logging.info("MissingRequiredArgument handler ran")
            # \n``Missing: {error.param.name}``")
            return await ctx.send(f"You didn't give a required argument.", delete_after=20)

        elif isinstance(error, commands.MissingPermissions):
            logging.info("MissingPermissions handler ran")
            return await ctx.send("You don't have the permissions for this command.", delete_after=20)
        
        elif isinstance(error, commands.NSFWChannelRequired):
            logging.info("NSFWChannelRequired hander ran")
            return await ctx.reply("How lewd of you <:AYAYAFlushed:822094723199008799>")

        elif isinstance(error, commands.CheckFailure):
            logging.error(f"{error}")
        logging.error(f"{error}")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
