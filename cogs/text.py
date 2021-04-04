import discord
import logging
from discord.ext import commands


class Text(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(case_insensitive=True, aliases=["link"], help="Links relevant for the bot")
    async def links(self, ctx):
        logging.info(f'Recieved link in {ctx.guild.name}')
        embed = discord.Embed(
            description="[Github Repo](https://github.com/Sirspam/Coordy-McCoordFace) | [Bot Invite Link](https://discord.com/api/oauth2/authorize?client_id=813699805150838795&permissions=29371392&scope=bot)\nI hope you're having a good day :)\nor not...\nthis is all just filler anyway",
            color=0x00A9E0)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/787809230639202354.png?v=1")
        await ctx.send(embed=embed)
        logging.info(f'Link embed sent\n----------')

    @commands.command(case_insensitive=True, aliases=["nick"], help="Changes the bot's nickname")
    @commands.has_permissions(administrator = True)
    async def nickname(self, ctx, *, arg):
        logging.info(f"Recieved nickname in {ctx.guild.name} from {ctx.author.name}")
        if arg == "None":
            await ctx.guild.me.edit(nick=None)
        else:
            await ctx.guild.me.edit(nick=arg)
        logging.info(f"Nickname successfully changed to: {arg}")

    @commands.command(case_insensitive=True, help="Makes the bot leave the guild")
    @commands.has_permissions(administrator = True)
    async def leave(self, ctx):
        logging.info(f"Recieved leave in {ctx.guild.name} from {ctx.author.name}")
        await ctx.guild.leave()
        logging.info(f"Successfully left the guild")

def setup(bot):
    bot.add_cog(Text(bot))