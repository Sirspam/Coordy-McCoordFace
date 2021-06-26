from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def help(self, ctx):
        try:
            prefix = self.bot.config[str(ctx.guild.id)]
        except KeyError:
            prefix = "cc "
        await ctx.reply(f"Prefix for this guild is ``{prefix}``\n\n**Commands Table:**\n<https://github.com/Sirspam/Coordy-McCoordFace/blob/main/README.md#Commands>")


def setup(bot):
    bot.add_cog(Help(bot))