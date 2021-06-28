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
        await ctx.reply(f"""Prefix for this guild is ``{prefix}``

<https://github.com/Sirspam/Coordy-McCoordFace#readme-index>
*I'll make a proper help command soon™*""")


def setup(bot):
    bot.add_cog(Help(bot))