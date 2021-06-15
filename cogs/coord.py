import logging
from discord.ext import commands
from random import getrandbits, choice, randint
from utils.role_checks import guild_coord_role_check


async def member_edit(self, ctx, action_type):
    if ctx.author.voice is None:
        return await ctx.send("You aren't in a voice channel!")
    voice = self.bot.get_channel(ctx.author.voice.channel.id)
    ignored_roles_ids = self.bot.config[ctx.guild.id]["ignored_roles_ids"]
    logging.info(f"Running member_edit in {voice.name}")
    for x in voice.members:
        if x.id == ctx.author.id:
            continue
        member = ctx.guild.get_member(x.id)
        if ignored_roles_ids:
            for xd in ignored_roles_ids:
                logging.info(f"Checking for ignored role: {xd}")
                if xd in str(member.roles):
                    logging.info(f"{x.name} ignored")
                    continue
                else:
                    if action_type == "mute":
                        await member.edit(mute=True)
                        logging.info(f"{x.name} muted")
                    elif action_type == "deafen":
                        await member.edit(mute=True, deafen=True)
                        logging.info(f"{x.name} muted deafened")
        else:
            if action_type == "mute":
                await member.edit(mute=True)
                logging.info(f"{x.name} muted")
            elif action_type == "deafen":
                await member.edit(mute=True, deafen=True)
                logging.info(f"{x.name} muted deafened")
    await ctx.message.delete()
    logging.info("Finished member_edit")


class Coord(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(aliases=["m"], help="Mutes users in your vc.")
    @guild_coord_role_check()
    async def mute(self, ctx):
        logging.info("mute ran")
        await member_edit(self, ctx, "mute")
        logging.info("Finished muting")

    @commands.command(aliases=["d"], help="Deafens and mutes users in your vc")
    @guild_coord_role_check()
    async def deafen(self, ctx):
        logging.info("deafen ran")
        await member_edit(self, ctx, "deafen")
        logging.info("Finished deafening")
    
    @commands.command(aliases=["um"], help="Unmutes users in your vc.")
    @guild_coord_role_check()
    async def unmute(self, ctx):
        logging.info("Unmute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Unmuting in {voice.name}")
        for x in voice.members:
            member = ctx.guild.get_member(x.id)
            if member.voice.mute is True:
                await member.edit(mute=False)
                logging.info(f"{x.name} unmuted")
        await ctx.message.delete()
        logging.info("Finished unmuting")

    @commands.command(aliases=["ud"], help="Undeafens and unmutes users in your vc.")
    @guild_coord_role_check()
    async def undeafen(self, ctx):
        logging.info("undeafen ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"undeafen in {voice.name}")
        for x in voice.members:
            member = ctx.guild.get_member(x.id)
            if member.voice.deaf is True:
                await member.edit(mute=False, deafen=False)
                logging.info(f"{x.name} undeafened")
        await ctx.message.delete()
        logging.info("Finished undeafening")

    @commands.command(aliases=["out"], help="Moves users to the lobby vc.")
    @guild_coord_role_check()
    async def move_out(self, ctx):
        logging.info("Move_in ran")
        lobby_vc_id = self.bot.config[ctx.guild.id]["lobby_vc_id"]
        ignored_roles_ids = self.bot.config[ctx.guild.id]["ignored_roles_ids"]
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Moving players in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            if ignored_roles_ids:
                for xd in ignored_roles_ids:
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
    @guild_coord_role_check()
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

    @commands.command(help="Flips a coin", aliases=["flip","coinflip"])
    @guild_coord_role_check()
    async def coin(self, ctx):
        logging.info("Coin ran")
        if getrandbits(1) == 1:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")
        logging.info("Coin ended")

    @commands.command(aliases=["p_u"], help="Picks a random user in your vc")
    @guild_coord_role_check()
    async def pick_user(self, ctx):
        logging.info(f"pick_user invoked in {ctx.guild.name}")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        ignored_roles_ids = self.bot.config[ctx.guild.id]["ignored_roles_ids"]
        logging.info(f"Picking user in {voice.name}")
        valid_users = list()
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            if ignored_roles_ids:
                for xd in ignored_roles_ids:
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
        logging.info("pick_user concluded")

    @commands.command(aliases=["pick_num","p_n"], help="Picks a random number inbetween 1 and the given argument")
    @guild_coord_role_check()
    async def pick_number(self, ctx, value: int):
        logging.info(f"pick_number invoked in {ctx.guild.name}")
        await ctx.send(randint(1,value))
        logging.info("pick_number concluded")

    @commands.command(aliases=["seperate","sep"], help="Posts a line seperator to help organise match text channels")
    @guild_coord_role_check()
    async def seperator(self, ctx):
        logging.info(f"seperator invoked in {ctx.guild.name}")
        await ctx.send("--------------------------------------------------------------")
        logging.info("seperator concluded")

# RESULTS:
# 1: AuriRex - 1190357
# 2: FreakFriends - 1158335

    @commands.command(aliases=["diff"], help="Calculates the difference between two players from TA results")
    @guild_coord_role_check()
    async def difference(self, ctx, *, results):
        splitted = results.split("\n")
        if len(splitted) > 3:
            raise commands.BadArgument
        await ctx.send(f"{int((splitted[1].rsplit(' - ',1))[1]) - int((splitted[2].rsplit(' - ',1))[1]):,}")


def setup(bot):
    bot.add_cog(Coord(bot))
