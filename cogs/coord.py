import logging
from random import getrandbits, choice, randint
from json import loads, JSONDecodeError

from discord.ext import commands
from utils.role_checks import guild_coord_role_check
from utils.database_management import add_to_cache
from utils.config_checks import config_lobby_vc_check


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


    async def cog_check(self, ctx):
        await add_to_cache(self.bot, ctx.guild)
        return True


    @commands.command(aliases=["m"], help="Mutes users in your vc.")
    @guild_coord_role_check()
    async def mute(self, ctx):
        await member_edit(self, ctx, "mute")

    @commands.command(aliases=["d"], help="Deafens and mutes users in your vc")
    @guild_coord_role_check()
    async def deafen(self, ctx):
        await member_edit(self, ctx, "deafen")
    
    @commands.command(aliases=["um"], help="Unmutes users in your vc.")
    @guild_coord_role_check()
    async def unmute(self, ctx):
        if ctx.author.voice is None:
            logging.info("User not in vc")
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Unmuting in {voice.name}")
        for x in voice.members:
            member = ctx.guild.get_member(x.id)
            if member.voice.mute is True:
                await member.edit(mute=False)
                logging.info(f"{x.name} unmuted")
        await ctx.message.delete()

    @commands.command(aliases=["ud"], help="Undeafens and unmutes users in your vc.")
    @guild_coord_role_check()
    async def undeafen(self, ctx):
        if ctx.author.voice is None:
            logging.info("User not in vc")
            return await ctx.send("You aren't in a voice channel!")
        voice = self.bot.get_channel(ctx.author.voice.channel.id)
        logging.info(f"undeafen in {voice.name}")
        for x in voice.members:
            member = ctx.guild.get_member(x.id)
            if member.voice.deaf is True:
                await member.edit(mute=False, deafen=False)
                logging.info(f"{x.name} undeafened")
        await ctx.message.delete()

    @commands.command(aliases=["out"], help="Moves users to the lobby vc.")
    @guild_coord_role_check()
    @config_lobby_vc_check()
    async def move_out(self, ctx):
        lobby_vc_id = self.bot.config[ctx.guild.id]["lobby_vc_id"]
        ignored_roles_ids = self.bot.config[ctx.guild.id]["ignored_roles_ids"]
        if ctx.author.voice is None:
            logging.info("Author not in vc")
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

    @commands.command(aliases=["in"], help="Moves mentioned users to your vc.")
    @guild_coord_role_check()
    async def move_in(self, ctx, *, argument):
        victims = argument.split() # I thought "victims" was a funny variable name for the users being moved :)
        for x in victims:
            victim = await commands.MemberConverter().convert(ctx, x)
            try:
                await victim.move_to(self.bot.get_channel(ctx.author.voice.channel.id))
            except Exception as e:
                logging.error(f"moving of {victim.name} failed: {e}")
        await ctx.message.delete()

    @commands.command(help="Flips a coin", aliases=["flip","coinflip"])
    @guild_coord_role_check()
    async def coin(self, ctx):
        if getrandbits(1) == 1:
            await ctx.send("Heads")
        else:
            await ctx.send("Tails")

    @commands.command(aliases=["p_u"], help="Picks a random user in your vc")
    @guild_coord_role_check()
    async def pick_user(self, ctx):
        if ctx.author.voice is None:
            logging.info("User not in vc")
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

    @commands.command(aliases=["pick_num","p_n"], help="Picks a random number inbetween 1 and the given argument")
    @guild_coord_role_check()
    async def pick_number(self, ctx, value: int):
        await ctx.send(randint(1,value))

    @commands.command(aliases=["seperate","sep"], help="Posts a line seperator to help organise match text channels")
    @guild_coord_role_check()
    async def seperator(self, ctx, *, text="--"):
        await ctx.message.delete()
        await ctx.send(f"------------------------{text}------------------------")

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

# https://multistre.am/stream1/stream2

    @commands.command(aliases=["ms"], help="Generates a Multistream link with either mentioned users or users in VC")
    @guild_coord_role_check()
    async def multistream(self, ctx, *, users=None):
        if users is None:
            logging.info("Users None, getting users from voice channel")
            users = str()
            if ctx.author.voice is None:
                logging.info("Author not in vc")
                return await ctx.send("You aren't in a voice channel!\nEither join a VC or mention some users.")
            voice = self.bot.get_channel(ctx.author.voice.channel.id)
            logging.info(f"Getting users in {voice.name}")
            for x in voice.members:
                if x.id == ctx.author.id:
                    continue
                member = ctx.guild.get_member(x.id)
                if self.bot.config[ctx.guild.id]["ignored_roles_ids"]:
                    for xd in self.bot.config[ctx.guild.id]["ignored_roles_ids"]:
                        logging.info(f"Checking for ignored role: {xd}")
                        if xd in str(member.roles):
                            logging.info(f"{x.name} ignored")
                            continue
                        else:
                            users = f"{users} {x.id}"
                else:
                    users = f"{users} {x.id}"
        users = users.split()
        multistream_link = "https://multistre.am"
        for user in users:
            user = await commands.MemberConverter().convert(ctx, user)
            async with ctx.channel.typing():
                async with self.bot.session.get(f"https://beatkhana.com/api/user/{user.id}") as resp:
                    try:
                        json_data = loads(await resp.text())
                    except JSONDecodeError:
                        logging.error("JSONDecodeError")
                        return await ctx.send(f"Failed to decode json response for __{user.name}__. This likely means they aren't registered on BeatKhana!")
                    multistream_link = f"{multistream_link}/{json_data['twitchName']}"
        await ctx.reply(f"<{multistream_link}>\n\nAll of these twitch names were taken from BeatKhana!. If someone has an invalid name, tell them to correct it on their BeatKhana! profile.")


def setup(bot):
    bot.add_cog(Coord(bot))
