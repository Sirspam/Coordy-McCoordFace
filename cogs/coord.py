import logging
from discord.ext import commands

# These variables need to be changed for whatever discord server the bot is being used in
coord_role_id = int()
lobby_vc_id = int()
ignored_roles = []


class coord(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.group(invoke_without_command=True, case_insensitive=True, aliases=["coord","c"])
    @commands.has_role(coord_role_id)
    async def coordinator(self, ctx):
        await ctx.send("Hi coordinator-kun ^w^")

    @coordinator.command(aliases=["m"])
    @commands.has_role(coord_role_id)
    async def mute(self, ctx):
        logging.info("coord mute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.client.get_channel(ctx.author.voice.channel.id)
        logging.info(f"muting in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            for xd in ignored_roles:
                logging.info(f"checking for ignored role: {xd}")
                if x in str(member.roles):
                    logging.info(f"")
                    continue
            await member.edit(mute=True, deafen=True)
            logging.info(f"{x.name} muted")
        await ctx.message.delete()
        logging.info("Finished muting\n-------------")

    @coordinator.command(aliases=["um"])
    @commands.has_role(coord_role_id)
    async def unmute(self, ctx):
        logging.info("coord unmute ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.client.get_channel(ctx.author.voice.channel.id)
        logging.info(f"unmuting in {voice.name}")
        for x in voice.members:
            await ctx.guild.get_member(x.id).edit(mute=False, deafen=False)
            logging.info(f"{x.name} unmuted")
        await ctx.message.delete()
        logging.info("Finished unmuting\n-------------")
    
    @coordinator.command(aliases=["mout"])
    @commands.has_role(coord_role_id)
    async def move_out(self, ctx):
        logging.info("coord move_in ran")
        if ctx.author.voice is None:
            return await ctx.send("You aren't in a voice channel!")
        voice = self.client.get_channel(ctx.author.voice.channel.id)
        logging.info(f"Moving players in {voice.name}")
        for x in voice.members:
            if x.id == ctx.author.id:
                continue
            member = ctx.guild.get_member(x.id)
            for x in ignored_roles:
                if x in str(member.roles):
                    continue
            await member.move_to(self.client.get_channel(lobby_vc_id))
            logging.info(f"{x.name} moved")
        await ctx.message.delete()
        logging.info("Finished moving\n-------------")

    @coordinator.command(aliases=["moin"])
    @commands.has_role(coord_role_id)
    async def move_in(self, ctx, *, argument):
        logging.info("coord move_in ran")
        victims = argument.split() # I thought "victims" was a funny variable name for the users being moved :)
        logging.info(victims)
        for x in victims:
            if x.isdigit():
                victim = ctx.guild.get_member(int(x))
            else:
                ID = x[3:]
                ID = ID[:-1]
            victim = ctx.guild.get_member(int(ID))
            if victim is None:
                logging.info("victim is None, continuing")
                continue
            logging.info(victim)
            try:
                await victim.move_to(self.client.get_channel(ctx.author.voice.channel.id))
            except Exception as e:
                logging.info(f"moving of {victim.name} failed: {e}")
        await ctx.message.delete()
        logging.info("Finished moving\n-------------")

def setup(client):
    client.add_cog(coord(client))