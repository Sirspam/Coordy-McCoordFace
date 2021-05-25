# {"discordId":"232574143818760192","ssId":"76561198091128855","name":"Sirspam","twitchName":"sirspam_","avatar":"5c191725bf1b19e089ddc3fba4d8c359","globalRank":683,"localRank":45,"country":"GB","tourneyRank":null,"TR":null,"pronoun":"He/Him","tournaments":["Spark The Challenge!","Beat The Hub","Beat Sage Royale"],"badges":[]}

import discord
import logging
import json
from discord.ext import commands
from json.decoder import JSONDecodeError
from utils.role_checks import guild_coord_role_check


class BeatKhana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(help="Gets information on a user from BeatKhana!", aliases=["bk"])
    @guild_coord_role_check()
    async def beatkhana(self, ctx, user:discord.User):
        logging.info(f"beatkhana invoked with {user} in {ctx.guild.name}")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/user/{user.id}") as resp:
                try:
                    json_data = json.loads(await resp.text())
                except JSONDecodeError:
                    return await ctx.send("Failed to decode json response. This likely means the user isn't registered on BeatKhana!")
            embed=discord.Embed(
                description=json_data["pronoun"],
                colour=0xc8825a
            )
            embed.set_author(
                name=json_data["name"],
                url=f"https://beatkhana.com/user/{user.id}",
                icon_url=str(user.avatar_url)
            )
            embed.add_field(
                name="Links",
                value=f"[ScoreSaber](https://scoresaber.com/u/{json_data['ssId']})\n[Twitch](https://www.twitch.tv/{json_data['twitchName']})\n↳ {json_data['twitchName']}",
                inline=True
            )
            embed.add_field(
                name="Rankings",
                value=f"Global: #{json_data['globalRank']}\nCountry: #{json_data['localRank']}\n↳ :flag_{json_data['country'].lower()}:",
                inline=True
            )
            message = str()
            for tournament in json_data["tournaments"]:
                message = f"{message}\n{tournament}"
            if not message:
                message = "None"
            embed.add_field(
                name="Previous Tournaments",
                value=message,
                inline=False
            )
        await ctx.reply(embed=embed)
        logging.info("beatkhana concluded")


def setup(bot):
    bot.add_cog(BeatKhana(bot))
