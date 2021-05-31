import discord
import logging
from io import StringIO
from datetime import datetime
from discord.errors import NotFound
from discord.ext import commands
from discord.ext.commands.errors import BadArgument


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["link"], help="Links relevant for the bot")
    async def links(self, ctx):
        logging.info(f'Recieved link in {ctx.guild.name}')
        embed = discord.Embed(
            description="[Github Repo](https://github.com/Sirspam/Coordy-McCoordFace) | [Bot Invite Link](https://discord.com/api/oauth2/authorize?client_id=813699805150838795&permissions=29682688&scope=bot)\n\nI hope you're having a good day :)",
            color=0x00A9E0)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/787809230639202354.png?v=1")
        await ctx.send(embed=embed)
        logging.info(f'Link embed sent')

    @commands.command(aliases=["nick"], help="Changes the bot's nickname")
    @commands.has_permissions(administrator = True)
    async def nickname(self, ctx, *, arg):
        logging.info(f"Recieved nickname in {ctx.guild.name} from {ctx.author.name}")
        if arg == "None":
            await ctx.guild.me.edit(nick=None)
            return logging.info(f"Nickname successfully reverted to default")
        else:
            await ctx.guild.me.edit(nick=arg)
            return logging.info(f"Nickname successfully changed to: {arg}")

    @commands.command(help="Makes the bot leave the guild")
    @commands.has_permissions(administrator = True)
    async def leave(self, ctx):
        logging.info(f"Recieved leave in {ctx.guild.name} from {ctx.author.name}")
        await ctx.guild.leave()
        logging.info(f"Successfully left the guild")

    @commands.command(help="Parses the TA bot leaderboard to a txt file")
    @commands.has_permissions(administrator = True)
    async def ta_to_txt(self, ctx, id: int):
        logging.info(f"ta_to_txt invoked in {ctx.guild.name}")
        try:
            message = await ctx.fetch_message(id)
        except NotFound:
            raise BadArgument
        if not message.embeds or message.embeds[0].title != ":page_with_curl: Leaderboards":
            raise BadArgument
        scores = dict()
        maps = str()
        iteration = 0 
        for field in message.embeds[0].fields:
            maps = maps+f", {field.name}"
            content = field.value[4:][:-5]
            content = content.replace("FC","")
            splitted = content.split(" \n\n")
            for x in splitted:
                split_score = (x.rsplit(" ",1))
                if split_score[0] not in scores:
                    scores[split_score[0]] = list([0]*len(message.embeds[0].fields))
                scores[split_score[0]][iteration] = int(split_score[1])
            iteration = iteration + 1
        for player in scores:
            total = sum(scores[player])
            scores[player].insert(0,total)
        scores = {key: val for key, val in sorted(scores.items(), key = lambda ele: ele[1][0], reverse = True)}
        result = f"Seeding, Name, Overall Score{maps}\n"
        iteration = 1
        for player in scores:
            result = result+f"#{iteration}, {player}, {str(scores[player])[1:-1]}\n"
            iteration = iteration+1
        await ctx.reply(file=discord.File(StringIO(str(result)),f"{ctx.guild.name} {datetime.now()}.txt"))
        logging.info("ta_to_txt concluded")


def setup(bot):
    bot.add_cog(General(bot))