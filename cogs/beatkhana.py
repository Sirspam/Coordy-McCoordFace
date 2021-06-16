import discord
import logging
import json
from datetime import datetime
from discord.ext import commands, menus
from utils.database_cache import add_to_cache

class QualifiersMenu(menus.ListPageSource):
    def __init__(self, data, embed):
        super().__init__(data, per_page=15)
        self.embed = embed

    async def format_page(self, menu, entries):
        offset = menu.current_page * self.per_page
        self.embed.clear_fields()
        self.embed.set_footer(text=f"Page {(menu.current_page+1)}/{self.get_max_pages()}")
        self.embed.add_field(
            name="\u200b", # Names
            value='\n'.join(f"#{i+1} **{v[0]}**" for i, v in enumerate(entries, start=offset)),
            inline=True
        )
        self.embed.add_field(
            name="\u200b", # Scores
            value='\n'.join(f"**{v[1]:,}**" for i, v in enumerate(entries, start=offset)),
            inline=True
        )
        return self.embed


class BeatKhana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_before_invoke(self, ctx):
        await add_to_cache(self.bot, ctx.guild)

    @commands.group(invoke_without_command=True, help="Gets information on a user from BeatKhana!", aliases=["bk"])
    async def beatkhana(self, ctx, user:discord.User):
        logging.info(f"beatkhana invoked with {user} in {ctx.guild.name}")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/user/{user.id}") as resp:
                try:
                    json_data = json.loads(await resp.text())
                except json.JSONDecodeError:
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
        logging.info("successfully concluded beatkhana")

    @beatkhana.command(help="Gets general information on the tournament", aliases=["tourney","t"])
    async def tournament(self, ctx):
        logging.info(f"beatkhana tournament invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                json_data = json.loads(await resp.text())[0]
            embed = discord.Embed(colour=0xc8825a)
            embed.set_author(
                name=f"{json_data['name']} Tournament",
                url=f"https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}",
                icon_url=f"https://beatkhana.com/assets/images/{json_data['image']}"
            )
            embed.add_field(
                name="Start Date",
                value=(datetime.fromisoformat(json_data["startDate"][:-1])).strftime('%Y/%m/%d\n%H:%M UTC'),
                inline=True
            )
            embed.add_field(
                name="End Date",
                value=(datetime.fromisoformat(json_data["endDate"][:-1])).strftime('%Y/%m/%d\n%H:%M UTC'),
                inline=True
            )
            embed.add_field(
                name="Links",
                value=f"[BeatKhana! Page](https://beatkhana.com/tournament/{json_data['tournamentId']})\n[Discord]({json_data['discord']})\n[Twitch]({json_data['twitchLink']})"
            )
            embed.add_field(
                name="Tournament Owner",
                value=f"<@{json_data['owner']}>",
                inline=True
            )
            embed.add_field(
                name="TA URL",
                value=f"``{json_data['ta_url']}``",
                inline=True
            )
            await ctx.send(embed=embed)
        logging.info("Successfully concluded beatkhana tournament")

    @beatkhana.command(help="Gets information on the tournament map pool", aliases=["map","m"])
    async def maps(self, ctx):
        logging.info(f"beatkhana maps invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                tourney_json_data = json.loads(await resp.text())[0]
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/map-pools") as resp:
                pool_json_data = json.loads(await resp.text())
        embed=discord.Embed(colour=0xc8825a)
        embed.set_author(
            name=f"{tourney_json_data['name']} Map Pools",
            url=f"https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/map-pool",
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
            description=f"**[Here's a link to BeatKhana's map pool page](https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/map-pool)**\n\nThis was likely caused by the embed going over discord's length cap.\nYou can easily fix this by removing some maps from your map pool <:AquaTroll:845802819634462780>",
            colour=discord.Colour.red()
        ))
        logging.info("Successfully concluded beatkhana maps")

    @beatkhana.command(help="Gets information on the tournament bracket", aliases=["bracket","b"])
    async def brackets(self, ctx):
        logging.info(f"beatkhana brackets invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                tourney_json_data = json.loads(await resp.text())[0]
            # async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/bracket") as resp:
            #     pool_json_data = json.loads(await resp.text())
        embed=discord.Embed(colour=0xc8825a)
        embed.set_author(
            name=f"{tourney_json_data['name']} Brackets",
            url=f"https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/bracket",
            icon_url=f"https://beatkhana.com/assets/images/{tourney_json_data['image']}"
        )
        await ctx.send(embed=embed)
        logging.info("Successfully cncluded beatkhana brackets")

    @beatkhana.command(help="Gets information on the tournament qualifiers", aliases=["quals","q"])
    async def qualifiers(self, ctx):
        logging.info(f"beakthana qualifiers invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/qualifiers") as resp:
                qualifiers_json_data = json.loads(await resp.text())
            if not qualifiers_json_data:
                logging.info("tournament doesn't have qualifier page")
                return await ctx.send("This tournament doesn't have a qualifier page!")
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                tourney_json_data = json.loads(await resp.text())[0]
        embed=discord.Embed(colour=0xc8825a, timestamp=ctx.message.created_at)
        embed.set_author(
            name=f"{tourney_json_data['name']} Qualifiers",
            url=f"https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/qualifiers",
            icon_url=f"https://beatkhana.com/assets/images/{tourney_json_data['image']}"
        )
        players = list()
        for player in qualifiers_json_data:
            scores = int()
            for score in player["scores"]:
                scores = scores + int(score["score"])
            players.append((f"[{player['name']}](https://beatkhana.com/user/{player['discordId']})",scores))
        players.sort(key=lambda a: a[1],reverse=True)
        pages = menus.MenuPages(source=QualifiersMenu(players, embed), timeout=30.0, clear_reactions_after=True)
        await pages.start(ctx)
        logging.info("Successfully concluded beatkhana qualifiers")

    @beatkhana.command(help="Gets information on the tournament staff", aliases=["s"])
    async def staff(self, ctx):
        logging.info(f"beatkhana staff invoked in {ctx.guild.name}")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                tourney_json_data = json.loads(await resp.text())[0]
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/staff") as resp:
                staff_json_data = json.loads(await resp.text())
        embed=discord.Embed(colour=0xc8825a)
        embed.set_author(
            name=f"{tourney_json_data['name']} Staff",
            url=f"https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/staff",
            icon_url=f"https://beatkhana.com/assets/images/{tourney_json_data['image']}"
        )
        for member in staff_json_data:
            message=str()
            for role in member["roles"]:
                message = f"{message} {role['role']},"
            embed.add_field(
                name=member["name"],
                value=message[:-1],
                inline=True
            )
        await ctx.send(embed=embed)
        logging.info("Successfully concluded beatkhana staff")


def setup(bot):
    bot.add_cog(BeatKhana(bot))
