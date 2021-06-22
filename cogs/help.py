from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def help(self, ctx):
        await ctx.reply("<https://github.com/Sirspam/Coordy-McCoordFace/blob/main/README.md#Commands>")


def setup(bot):
    bot.add_cog(Help(bot))