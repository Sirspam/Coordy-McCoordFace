# https://waifu.pics/docs

import discord
import io
import json
import logging
from discord.ext import commands
from os.path import splitext

class Waifu(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot


    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(aliases=["wa"], help="Posts a waifu")
    async def waifu(self, ctx):
        logging.info(f"waifu invoked")
        async with ctx.channel.typing():
            results = await get_image(self, f"sfw/waifu")
            try:
                await ctx.reply(file=discord.File(results[0], f"waifu{results[1]}"))
            except discord.HTTPException:
                await ctx.reply(results[2])
        logging.info("attachment sent")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(help="Posts a neko")
    async def neko(self, ctx):
        logging.info(f"neko invoked")
        async with ctx.channel.typing():
            results = await get_image(self, f"sfw/neko")
            try:
                await ctx.reply(file=discord.File(results[0], f"neko{results[1]}"))
            except discord.HTTPException:
                await ctx.reply(results[2])
        logging.info("attachment sent")

def setup(bot):
    bot.add_cog(Waifu(bot))


async def get_image(self, endpoint):
    logging.info(f"get_image function invoked with {endpoint}")
    link = "https://api.waifu.pics/"+endpoint
    async with self.bot.session.get(link) as resp:
        json_data = json.loads(await resp.text())
        logging.info(json_data["url"])
        async with self.bot.session.get(json_data["url"]) as resp:
            root, ext = splitext(json_data["url"])
            return (io.BytesIO(await resp.read()),ext)