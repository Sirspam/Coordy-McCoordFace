import discord
import json
import logging
from discord.ext import commands
from datetime import datetime


diff_emotes = { # Emotes from sus
    "easy": "<:Easy_1:848911334237012030><:Easy_2:848911334435455007>",
    "normal": "<:Normal_1:848911334108299265><:Normal_2:848911334442926100><:Normal_3:848911334447513651>",
    "hard": "<:Hard_1:848911334430212156><:Hard_2:848911334422478899>",
    "expert": "<:Expert_1:848911334405177364><:Expert_2:848911334422216714>",
    "expertPlus": "<:ExpertPlus_1:848911334392201246><:ExpertPlus_2:848911334426148874><:ExpertPlus_3:848911334400983050>",
}


async def diff_sort(difficulties):
    diff_order = ["easy","normal","hard","expert","expertPlus"]
    diff_copy = ["easy","normal","hard","expert","expertPlus"]
    for diff in diff_order:
        if diff not in difficulties:
            diff_copy.remove(diff)
    return [x for _,x in sorted(zip(difficulties,diff_copy))]


class BeatSaver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["bs","bsr"])
    async def beatsaver(self, ctx, key, diff=None):
        logging.info(f"Running beatsaver with {key} as key")
        async with ctx.channel.typing():
            async with self.bot.session.get(f"https://beatsaver.com/api/maps/detail/{key}") as resp:
                if await resp.text() == "Not Found":
                    raise commands.BadArgument
                response = json.loads(await resp.text())
            difficulties = []
            for x in response["metadata"]["difficulties"]:
                if response["metadata"]["difficulties"][x] is True:
                    difficulties.append(x)
            difficulties = await diff_sort(difficulties)
            if diff is not None and diff in difficulties:
                diff_stats = response["metadata"]["characteristics"][0]["difficulties"][diff]
            else:
                diff = difficulties[-1]
                diff_stats = response["metadata"]["characteristics"][0]["difficulties"][diff]
            if response["metadata"]["songSubName"] == '':
                title = response["metadata"]["songName"]
            else:
                title = response["metadata"]["songName"]+" - "+response["metadata"]["songSubName"]
            m, s = divmod(response["metadata"]["duration"], 60)
            embed = discord.Embed(
                title=title,
                url=f"https://beatsaver.com/beatmap/{key}",
                description=f"**{response['metadata']['songAuthorName']}**",
                colour=0x232325
            )
            embed.add_field(
                name="Map Stats",
                value=f"Duration: {m:02d}:{s:02d}\nBPM: {response['metadata']['bpm']}\nMapper: {response['metadata']['levelAuthorName']}",
                inline=True
            )
            embed.add_field(
                name="BeatSaver Stats",
                value=f"Key: {response['key']}\nDownloads: {response['stats']['downloads']}\nRating: {int(response['stats']['rating']*100)}%\nUploaded: {(datetime.fromisoformat(response['uploaded'][:-1])).strftime('%Y-%m-%d')}",
                inline=True
            )
            message=str()
            for difficulty in difficulties:
                message=f"{message}\n{diff_emotes[difficulty]}"
            embed.add_field(
                name="Difficulties",
                value=message,
                inline=True
            )
            embed.add_field(
                name=f"Difficulty Stats {diff_emotes[diff]}",
                value=f"NJS: {diff_stats['njs']}\nOffset: {diff_stats['njsOffset']}\n Notes: {diff_stats['notes']}\n Bombs: {diff_stats['bombs']}\n Obstacles: {diff_stats['obstacles']}",
                inline=True
            )
            embed.add_field(
                name="Links",
                value=f"[Preview Map](https://skystudioapps.com/bs-viewer/?id={response['key']})\n[Download Map](https://beatsaver.com/api/download/key/{response['key']})\n[Song on Youtube](https://www.youtube.com/results?search_query={response['metadata']['songAuthorName'].replace(' ','+')}+{title.replace(' ','+')})\n[Song on Spotify](https://open.spotify.com/search/{response['metadata']['songName'].replace(' ','%20')})",
                inline=True
            )
            embed.set_image(url="https://beatsaver.com"+response["coverURL"])
            await ctx.reply(embed=embed)
        logging.info("successfully concluded beatsaver")

    @beatsaver.error
    async def beatsaver_error(self, ctx, error):
        if isinstance (error, commands.BadArgument):
            await ctx.send("You've given a bad argument!\nYou should totally try ``e970`` though <:AYAYATroll:839891422140432405>")
        elif isinstance (error, commands.MissingRequiredArgument):
            return await ctx.send("You didn't give a required argument.\nYou should totally try ``e970`` though <:AquaTroll:845802819634462780>")
        logging.error(error)


def setup(bot):
    bot.add_cog(BeatSaver(bot))