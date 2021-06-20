# Waifu API documentation
# https://waifu.pics/docs


import logging
from io import BytesIO
from json import loads

from discord import File, HTTPException

from discord.ext import commands
from os.path import splitext


class Waifu(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot


    async def cog_before_invoke(self, ctx):
        logging.info(f"Invoked {ctx.command} in {ctx.guild.name} by {ctx.author.name}\nArgs: {ctx.args}" )

    async def cog_after_invoke(self, ctx):
        logging.info(f"Concluded {ctx.command}")


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["wa"], help="Posts a waifu")
    async def waifu(self, ctx):
        async with ctx.channel.typing():
            results = await get_image(self, f"sfw/waifu")
            try:
                await ctx.reply(file=File(results[0], f"waifu{results[1]}"))
            except HTTPException:
                await ctx.reply(results[2])

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["nya"], help="Posts a neko")
    async def neko(self, ctx):
        async with ctx.channel.typing():
            results = await get_image(self, f"sfw/neko")
            try:
                await ctx.reply(file=File(results[0], f"neko{results[1]}"))
            except HTTPException:
                await ctx.reply(results[2])

def setup(bot):
    bot.add_cog(Waifu(bot))


async def get_image(self, endpoint):
    logging.info(f"get_image function invoked with {endpoint}")
    link = "https://api.waifu.pics/"+endpoint
    async with self.bot.session.get(link) as resp:
        json_data = loads(await resp.text())
        logging.info(json_data["url"])
        async with self.bot.session.get(json_data["url"]) as resp:
            root, ext = splitext(json_data["url"])
            return (BytesIO(await resp.read()), ext, link)