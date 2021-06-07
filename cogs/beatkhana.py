# {"discordId":"232574143818760192","ssId":"76561198091128855","name":"Sirspam","twitchName":"sirspam_","avatar":"5c191725bf1b19e089ddc3fba4d8c359","globalRank":683,"localRank":45,"country":"GB","tourneyRank":null,"TR":null,"pronoun":"He/Him","tournaments":["Spark The Challenge!","Beat The Hub","Beat Sage Royale"],"badges":[]}

import discord
import logging
import json
from discord.ext import commands
from json.decoder import JSONDecodeError


class BeatKhana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.group(invoke_without_command=True, help="Gets information on a user from BeatKhana!", aliases=["bk"])
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

    @beatkhana.command(help="Gets general information on the tournament", aliases=["tourney","t"])
    async def tournament(self, ctx):
        logging.info(f"beatkhana tournament invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[str(ctx.guild.id)]['beatkhana_id']}") as resp:
                json_data = json.loads(await resp.text())[0]
            embed = discord.Embed(colour=0xc8825a)
            embed.set_author(
                name=f"{json_data['name']} Map Pools",
                url=f"https://beatkhana.com/tournament/{self.bot.config[str(ctx.guild.id)]['beatkhana_id']}/map-pool",
                icon_url=f"https://beatkhana.com/assets/images/{json_data['image']}"
            )
            embed.add_field(
                name="Info",
                value=json_data["info"],
                inline=False
            )
            embed.add_field(
                name="Staff",
                value="a",
                inline=False
            )
            await ctx.send(embed=embed)

    @beatkhana.command(help="Gets information on the tournament map pool", aliases=["map","m"])
    async def maps(self, ctx):
        logging.info(f"beatkhana maps invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[str(ctx.guild.id)]['beatkhana_id']}") as resp:
                tourney_json_data = json.loads(await resp.text())[0]
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[str(ctx.guild.id)]['beatkhana_id']}/map-pools") as resp:
                pool_json_data = json.loads(await resp.text())
        embed=discord.Embed(colour=0xc8825a)
        embed.set_author(
            name=f"{tourney_json_data['name']} Map Pools",
            url=f"https://beatkhana.com/tournament/{self.bot.config[str(ctx.guild.id)]['beatkhana_id']}/map-pool",
            icon_url=f"https://beatkhana.com/assets/images/{tourney_json_data['image']}"
        )
        for pool in pool_json_data:
            message = str()
            for song in pool_json_data[pool]["songs"]:
                message = f"{message}[{song['name']} - {song['songAuthor']}](https://beatsaver.com/beatmap/{song['key']}) [{song['levelAuthor']}] - **{song['diff']}** ``{song['key']}``\n"
            message = f"{message}\n**[[Download Pool]](https://beatkhana.com/api/download-pool/{pool})**"
            embed.add_field(
                name=pool_json_data[pool]["poolName"],
                value=message,
                inline=False
            )
        try:
            await ctx.send(embed=embed)
        except discord.HTTPException:
            await ctx.send(embed=discord.Embed(
            title="Uh oh. I couldn't send the map pool embed <:NotLikeAqua:822089498866221076>",
            description=f"**[Here's a link to BeatKhana's map pool page](https://beatkhana.com/tournament/{self.bot.config[str(ctx.guild.id)]['beatkhana_id']}/map-pool)**\n\nThis was likely caused by the embed going over discord's length cap.\nYou can easily fix this by removing some maps from your map pool <:AquaTroll:845802819634462780>",
            colour=discord.Colour.red()
        ))
        logging.info("Beatkhana maps concluded")

    @beatkhana.command(help="Gets information on the tournament bracket", aliases=["bracket","b"])
    async def brackets(self, ctx):
        logging.info(f"beatkhana brackets invoked in {ctx.guild.name}")


def setup(bot):
    bot.add_cog(BeatKhana(bot))
