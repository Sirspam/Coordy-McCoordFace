import discord
import logging
from random import randint, choice
from discord.ext import commands, tasks

switch = True

def random_emote(list):
    reaction = randint(0, len(list))
    reaction = reaction - 1
    return reaction


class Text(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=["bonk"])
    async def ping(self, ctx):
        await ctx.send(f'<a:bonk:750089165512638616> ``{round(self.bot.latency * 1000)}ms``')
        logging.info("bonk ran")

    @commands.command(case_insensitive=True, aliases=["coomlist"])
    async def nonce(self, ctx):
        await ctx.send(f"<:Pepegahands:741779918001799259>\n{self.bot.coomlist}")
        logging.info("nonce ran")

    @commands.command(case_insensitive=True, aliases=["switch"])
    async def retard(self, ctx):
        global switch
        if switch is False:
            switch = True
            # await self.bot.change_presence(activity=discord.Game(name="Retardation Engaged"))
            logging.info("Reactions ON")
        elif switch is True:
            switch = False
            # await self.bot.change_presence(activity=discord.Game(name="Retardation Disengaged"))
            logging.info("Reactions OFF")
        await ctx.send("<a:crybaby:777526112149700619>")
        logging.info("retard ran")

    @commands.command(case_insensitive=True, aliases=["link"])
    async def invite(self, ctx):
        embed = discord.Embed(
            title="Jushy invite link",
            description="https://discord.com/api/oauth2/authorize?bot_id=778565225213329438&permissions=314432&scope=bot",
            colour=0x7fa7ea
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/446791704805244940/783452640193282148/unknown.png")
        await ctx.send(embed=embed)

    @commands.command(name="spongebob")
    async def sb(self, ctx, *, text: str):
        out = ""
        for i, l in enumerate(text):
            if i % 2:
                out += l.upper()
            else:
                out += l.lower()
        await ctx.send(out)


def setup(bot: commands.Bot):
    bot.add_cog(Text(bot))
