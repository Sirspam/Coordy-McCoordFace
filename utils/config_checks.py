from discord.ext.commands import CheckFailure, check

class ConfigBeatKhana(CheckFailure):
    pass

class ConfigLobbyVC(CheckFailure):
    pass

def config_beatkhana_check():
    async def predicate(ctx):
        if not ctx.bot.config[ctx.guild.id]['beatkhana_id']:
            raise ConfigBeatKhana()
        return True
    return check(predicate)

def config_lobby_vc_check():
    async def predicate(ctx):
        if not ctx.bot.config[ctx.guild.id]['lobby_vc']:
            raise ConfigLobbyVC()
        return True
    return check(predicate)
