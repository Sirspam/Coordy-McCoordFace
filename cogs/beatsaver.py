#https://beatsaver.com/api/maps/detail/{key} - Map stats
#https://beatsaver.com/api/stats/key/{key} - BS stats


import discord
import json
import logging
from discord.ext import commands


diff_emotes = {
    "easy": "<:Easy_1:822072552570486804><:Easy_2:822072552407040051>",
    "normal": "<:Normal_1:822072552544927774><:Normal_2:822072552582021120><:Normal_3:822072552540864532>",
    "hard": "<:Hard_1:822072552288813108><:Hard_2:822072552452522035>",
    "expert": "<:Expert_1:822072552556855317><:Expert_2:822072552532738068>",
    "expertPlus": "<:ExpertPlus_1:822072552268496917><:ExpertPlus_2:822072552506916884><:ExpertPlus_3:822072552514912328>",
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
                detail_text = json.loads(await resp.text())
            async with self.bot.session.get(f"https://beatsaver.com/api/stats/key/{key}") as resp:
                stats_text = json.loads(await resp.text())
            difficulties = []
            for x in detail_text["metadata"]["difficulties"]:
                if detail_text["metadata"]["difficulties"][x] is True:
                    difficulties.append(x)
            difficulties = await diff_sort(difficulties)
            if diff is not None and diff in difficulties:
                diff_stats = detail_text["metadata"]["characteristics"][0]["difficulties"][diff]
            else:
                diff = difficulties[-1]
                diff_stats = detail_text["metadata"]["characteristics"][0]["difficulties"][diff]
            if detail_text["metadata"]["songSubName"] == '':
                title = detail_text["metadata"]["songName"]
            else:
                title = detail_text["metadata"]["songName"]+" - "+detail_text["metadata"]["songSubName"]
            m, s = divmod(detail_text["metadata"]["duration"], 60)
            embed = discord.Embed(
                title=title,
                url=f"https://beatsaver.com/beatmap/{key}",
                description=f"**{detail_text['metadata']['songAuthorName']}**",
                colour=0x232325,
                timestamp=ctx.message.created_at
            )
            embed.add_field(
                name="Map Stats",
                value=f"Duration: {m:02d}:{s:02d}\nBPM: {detail_text['metadata']['bpm']}\nMapper: {detail_text['metadata']['levelAuthorName']}",
                inline=True
            )
            embed.add_field(
                name="BeatSaver Stats",
                value=f"Key: {stats_text['key']}\nDownloads: {stats_text['stats']['downloads']}\nRating: {int(stats_text['stats']['rating']*100)}%",
                inline=True
            )
            embed.add_field(
                name=f"Difficulty Stats {diff_emotes[diff]}",
                value=f"NJS: {diff_stats['njs']}\nOffset: {diff_stats['njsOffset']}\n Notes: {diff_stats['notes']}\n Bombs: {diff_stats['bombs']}\n Obstacles: {diff_stats['obstacles']}",
                inline=False
            )
            embed.set_image(url="https://beatsaver.com"+detail_text["coverURL"])
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(BeatSaver(bot))