import logging
from json import loads, JSONDecodeError
from datetime import datetime
from xml import etree

from discord import User, Embed

from discord.ext import commands, menus
from utils.database_management import add_to_cache
from utils.config_checks import config_beatkhana_check


class TournamentMenu(menus.ListPageSource):
    def __init__(self, data):
        super().__init__(data, per_page=1)

    async def format_page(self, menu, entries):
        return entries

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

class MapPoolMenu(menus.ListPageSource):
    def __init__(self, data, embed):
        super().__init__(data, per_page=1)
        self.embed = embed

    async def format_page(self, menu, entries):
        self.embed.clear_fields()
        self.embed.set_footer(text=f"Page {(menu.current_page+1)}/{self.get_max_pages()}")
        self.embed.add_field(
            name=entries[0],
            value=entries[1],
            inline=True)
        return self.embed

class BeatKhana(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def cog_check(self, ctx):
        await add_to_cache(self.bot, ctx.guild)
        return True


    @commands.group(invoke_without_command=True, help="Gets information on a user from BeatKhana!", aliases=["bk"])
    async def beatkhana(self, ctx, user:User):
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/user/{user.id}") as resp:
                try:
                    json_data = loads(await resp.text())
                except JSONDecodeError:
                    return await ctx.send("Failed to decode json response. This likely means the user isn't registered on BeatKhana!")
            embed=Embed(
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

    @beatkhana.command(help="Gets general information on the tournament", aliases=["tourney","t"])
    @config_beatkhana_check()
    async def tournament(self, ctx):
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                json_data = loads(await resp.text())[0]
            embed = Embed(colour=0xc8825a)
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
            message=str()
            if json_data["discord"]:
                message = f"[Discord]({json_data['discord']})\n"
            if json_data['twitchLink']:
                message = f"{message}[Twitch]({json_data['twitchLink']})"
            embed.add_field(
                name="Links",
                value=message
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
            embed_description = Embed(
                title="Description",
                # Might move the below into a dict and for loop within a function 
                # if something else later on needs to translate html shim sham
                description=json_data['info'].replace("&nbsp;"," ")\
                    .replace("&#39;","'")\
                    .replace("<p>","").replace("</p>","")\
                    .replace("<strong>","**").replace("</strong>","**")\
                    .replace("<em>","*").replace("</em>","*")\
                    .replace("<small>","*").replace("</small>","*")\
                    .replace("<ul>","").replace("</ul>","")\
                    .replace("<li>","- ").replace("</li>",""),
                colour=0xc8825a
            )
            embed_description.set_author(
                name=f"{json_data['name']} Tournament",
                url=f"https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}",
                icon_url=f"https://beatkhana.com/assets/images/{json_data['image']}"
            )
            embeds=[embed, embed_description]
            pages = menus.MenuPages(source=TournamentMenu(embeds), timeout=30.0, clear_reactions_after=True)
            await pages.start(ctx)

    @beatkhana.command(help="Gets information on the tournament map pool", aliases=["map","m"])
    @config_beatkhana_check()
    async def maps(self, ctx):
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                tourney_json_data = loads(await resp.text())[0]
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/map-pools") as resp:
                pool_json_data = loads(await resp.text())
        embed=Embed(colour=0xc8825a)
        embed.set_author(
            name=f"{tourney_json_data['name']} Map Pools",
            url=f"https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/map-pool",
            icon_url=f"https://beatkhana.com/assets/images/{tourney_json_data['image']}"
        )
        fields = list()
        for pool in pool_json_data:
            message = str()
            for song in pool_json_data[pool]["songs"]:
                message = f"{message}[{song['name']} - {song['songAuthor']}](https://beatsaver.com/beatmap/{song['key']}) [{song['levelAuthor']}] - **{song['diff']}** ``{song['key']}``\n"
            message = f"{message}\n**[[Download Pool]](https://beatkhana.com/api/download-pool/{pool})**"
            fields.append((pool_json_data[pool]["poolName"], message))
        pages = menus.MenuPages(source=MapPoolMenu(fields, embed), timeout=30.0, clear_reactions_after=True)
        await pages.start(ctx)

    @beatkhana.command(help="Gets information on the tournament bracket", aliases=["bracket","b"])
    async def brackets(self, ctx):
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                tourney_json_data = loads(await resp.text())[0]
            # async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/bracket") as resp:
            #     pool_json_data = loads(await resp.text())
        embed=Embed(colour=0xc8825a)
        embed.set_author(
            name=f"{tourney_json_data['name']} Brackets",
            url=f"https://beatkhana.com/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/bracket",
            icon_url=f"https://beatkhana.com/assets/images/{tourney_json_data['image']}"
        )
        await ctx.send(embed=embed)

    @beatkhana.command(help="Gets information on the tournament qualifiers", aliases=["quals","q"])
    @config_beatkhana_check()
    async def qualifiers(self, ctx):
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/qualifiers") as resp:
                qualifiers_json_data = loads(await resp.text())
            if not qualifiers_json_data:
                logging.info("tournament doesn't have qualifier page")
                return await ctx.send("This tournament doesn't have a qualifier page!")
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                tourney_json_data = loads(await resp.text())[0]
        embed=Embed(colour=0xc8825a, timestamp=ctx.message.created_at)
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

    @beatkhana.command(help="Gets information on the tournament staff", aliases=["s"])
    @config_beatkhana_check()
    async def staff(self, ctx):
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}") as resp:
                tourney_json_data = loads(await resp.text())[0]
            async with self.bot.session.get(f"https://beatkhana.com/api/tournament/{self.bot.config[ctx.guild.id]['beatkhana_id']}/staff") as resp:
                staff_json_data = loads(await resp.text())
        embed=Embed(colour=0xc8825a)
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


def setup(bot):
    bot.add_cog(BeatKhana(bot))
