import math
import logging
import asyncio
from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        logging.info(f"on_command_error triggered")
        
        if hasattr(ctx.command, "on_error"):
            return
        
        elif isinstance(error, commands.BadArgument):
            logging.info("BadArgument handler ran")
            return await ctx.send(f"You've given a bad argument!\nCheck ``{ctx.prefix}help`` for what arguments you need to give")

        elif isinstance(error, commands.CommandNotFound):
            logging.info("CommandNotFound handler ran")
            return await ctx.send("Command not found")

        elif isinstance(error, commands.BotMissingPermissions):
            logging.info(f"BotMissingPermissions handler ran - {error.missing_perms}")
            return await ctx.send(f"Bot missing the following permissions: {error.missing_perms}")

        elif isinstance(error, commands.NotOwner):
            logging.info("NotOwner handler ran")
            return await ctx.send("This is an owner only command.")

        elif isinstance(error, commands.CommandOnCooldown):
            logging.info("CommandOnCooldown handler ran")
            message = await ctx.send(f"Command on cooldown, ``{math.ceil(error.retry_after)} seconds``")
            await asyncio.sleep(int(math.ceil(error.retry_after)))
            return await message.add_reaction("✅")

        elif isinstance(error, commands.MissingRequiredArgument):
            logging.info(f"MissingRequiredArgument handler ran. Missing: {error.param.name}")
            return await ctx.send("You didn't give a required argument.")

        elif isinstance(error, commands.MissingPermissions):
            logging.info("MissingPermissions handler ran")
            return await ctx.send("You don't have the permissions for this command.")
        
        elif isinstance(error, commands.NSFWChannelRequired):
            logging.info("NSFWChannelRequired hander ran")
            return await ctx.reply("How lewd of you <:AYAYAFlushed:822094723199008799>\n``This command can only be ran in an nsfw channel``")

        logging.error(f"{error}")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
