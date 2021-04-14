import logging
import json
from discord.ext import commands
from random import getrandbits
from random import choice


config = json.load(open("config.json",))
lobby_vc_id = config["lobby_vc_id"] # int - Must be voice channel ID
coord_roles_ids = config["coord_roles_ids"] # int - Must be role ID
ignored_roles = config["ignored_roles"] # str - Can be either role name or role ID
del config # Deleting config just to save memory


class Coord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["m"], help="Mutes users in your vc.")
    @commands.has_any_role(*coord_roles_ids)
    async def mute(self, ctx):
        logging.info("mute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Muting in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            if ignored_roles:
                for xd in ignored_roles:
                    logging.info(f"Checking for ignored role: {xd}")
                    if xd in str(member.roles):
                        logging.info(f"{x.name} ignored")
                        continue
                    else:
                        await member.edit(mute=True, deafen=True)
                        logging.info(f"{x.name} muted")
            else:
                await member.edit(mute=True, deafen=True)
                logging.info(f"{x.name} muted")
        await ctx.message.delete()
        logging.info("Finished muting")


    @commands.command(aliases=["um"], help="Unmutes users in your vc.")
    @commands.has_any_role(*coord_roles_ids)
    async def unmute(self, ctx):
        logging.info("Unmute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Unmuting in {voice.name}")
        for x in voice.members:
            member = ctx.guild.get_member(x.id)
            if member.voice.mute is True:
                await member.edit(mute=False, deafen=False)
                logging.info(f"{x.name} unmuted")
        await ctx.message.delete()
        logging.info("Finished unmuting")
    

    @commands.command(aliases=["out"], help="Moves users to the lobby vc.")
    @commands.has_any_role(*coord_roles_ids)
    async def move_out(self, ctx):
        logging.info("Move_in ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Moving players in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            if ignored_roles:
                for xd in ignored_roles:
                    logging.info(f"Checking for ignored role: {xd}")
                    if xd in str(member.roles):
                        logging.info(f"{x.name} ignored")
                        continue
                    else:
                        await member.move_to(self.bot.get_channel(lobby_vc_id))
                        logging.info(f"{x.name} moved")
            else:
                await member.move_to(self.bot.get_channel(lobby_vc_id))
                logging.info(f"{x.name} moved")
        await ctx.message.delete()
        logging.info("Finished moving")


    @commands.command(aliases=["in"], help="Moves mentioned users to your vc.")
    @commands.has_any_role(*coord_roles_ids)
    async def move_in(self, ctx, *, argument):
        logging.info("Move_in ran")
        victims = argument.split() # I thought "victims" was a funny variable name for the users being moved :)
        for x in victims:
            victim = await commands.MemberConverter().convert(ctx, x)
            try:
                await victim.move_to(self.bot.get_channel(ctx.author.voice.channel.id))
            except Exception as e:
                logging.error(f"moving of {victim.name} failed: {e}")
        await ctx.message.delete()
        logging.info("Finished moving")


    @commands.command(help="Flips a coin")
    @commands.has_any_role(*coord_roles_ids)
    async def coin(self, ctx):
        logging.info("Coin ran")
        if getrandbits(1) == 1:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")
        logging.info("Coin ended")


    @commands.command(help="Picks a random user in your vc")
    @commands.has_any_role(*coord_roles_ids)
    async def pick(self, ctx):
        logging.info("Pick ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Picking user in {voice.name}")
        valid_users = []
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            if ignored_roles:
                for xd in ignored_roles:
                    logging.info(f"Checking for ignored role: {xd}")
                    if xd in str(member.roles):
                        logging.info(f"{x.name} ignored")
                        continue
                    else:
                        valid_users.append(member.name)
                        logging.info(f"{x.name} valid")
            else:
                valid_users.append(member.name)
                logging.info(f"{x.name} valid")
        await ctx.send(choice(valid_users))
        logging.info("Picking finished")


def setup(bot):
    bot.add_cog(Coord(bot))
