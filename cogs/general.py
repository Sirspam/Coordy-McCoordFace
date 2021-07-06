import logging
from io import StringIO
from datetime import datetime

from discord import Embed, File, Permissions

from discord.errors import NotFound
from discord.ext import commands
from discord.utils import oauth_url
from utils.role_checks import admin_or_bot_owner_check


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["invite"])
    async def links(self, ctx):
        permission_names = (
            "read_messages",
            "send_messages",
            "manage_messages",
            "embed_links",
            "attach_files",
            "read_message_history",
            "add_reactions",
            "use_external_emojis"
            "mute_members",
            "deafen_members",
            "move_members"
        )
        perms = Permissions()
        perms.update(**dict.fromkeys(permission_names, True))
        embed = Embed(
            description=
f"""[**Bot Invite Link**]({oauth_url(self.bot.user.id, perms)})
[**Home Server**](https://discord.gg/dWX6fpGUK9)
[**Github Repo**](https://github.com/Sirspam/Coordy-McCoordFace)\n
I hope you're having a good day :)""",
            color=0x00A9E0)
        embed.set_thumbnail(url="https://cdn.discordapp.com/emojis/787809230639202354.png?v=1")
        await ctx.reply(embed=embed)

    @commands.command(aliases=["nick"], help="Changes the bot's nickname")
    @admin_or_bot_owner_check()
    async def nickname(self, ctx, *, arg):
        if arg == "None":
            await ctx.guild.me.edit(nick=None)
            return logging.info(f"Nickname successfully reverted to default")
        await ctx.guild.me.edit(nick=arg)

    @commands.command(help="Makes the bot leave the guild")
    @admin_or_bot_owner_check()
    async def leave(self, ctx):
        await ctx.guild.leave()

    @commands.command(help="Parses the TA bot leaderboard to a txt file")
    @admin_or_bot_owner_check()
    async def ta_to_txt(self, ctx, message_id: int):
        try:
            message = await ctx.fetch_message(message_id)
        except NotFound:
            raise commands.BadArgument
        if not message.embeds or message.embeds[0].title != ":page_with_curl: Leaderboards":
            raise commands.BadArgument
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
        await ctx.reply(file=File(StringIO(str(result)),f"{ctx.guild.name} {datetime.now()}.txt"))


def setup(bot):
    bot.add_cog(General(bot))