# Coordy McCoordFace
[![CodeFactor](https://www.codefactor.io/repository/github/sirspam/coordy-mccoordface/badge)](https://www.codefactor.io/repository/github/sirspam/coordy-mccoordface)

Coordy McCoordFace is a discord bot I've made to help assist in the coordination of Beat Saber tournaments.

## Readme Index
* [Readme Index](#Readme-Index)
* [Commands](#Commands)
    * [General Commands](#General-Commands)
        * [BeatKhana! Commands](#BeatKhana!-Commands)
    * [Coordination Commands](#Coordination-Commands)
        * [Voice Channel Management](#Voice-Channel-Management)
        * [Utilities](#Utilities)
    * [Administrator Commands](#Administrator-Commands)
        * [Configuration Commands](#Configuration-Commands)
        * [Quality of Life Commands](#Quality-of-Life-Commands)
    * [Super Duper Secret Commands](#Super-Duper-Secret-Commands)
* [Setting up Coordy McCoordFace](#Setting-up-Coordy-McCoordFace)
    * [config.json definitions](#config.json-definitions)
        * [prefix](#prefix)
        * [lobby_vc_id](#lobby_vc_id)
        * [beatkhana_id](#beatkhana_id)
        * [coord_roles_ids](#coord_roles_ids)
        * [ignored_roles_ids](ignored_roles_ids)
* [To-Do](#To-Do)



## Commands
[ ] represents a required parameter while ( ) represents an optional parameter.

### General Commands
| Command | Alias | Description |
| --- | --- | --- |
| links |  | Post an embed containing relevant links for the bot. |
| beatsaver \[key\] \(difficulty\)| bs, bsr | Gets information on a certain beatmap. |

#### BeatKhana! Commands
| Command | Alias | Description |
| --- | --- | --- |
| beatkhana \[mention\] | bk | Gets information on a mentioned user from BeatKhana! |
| beatkhana tournament | bk tourney, bk t | Gets general information on the tournament |
| beatkhana maps | bk maps, bk m | Gets information on the tournament map pool |
| beatkhana brackets | bk bracket, bk b | Gets information on the tournament bracket (WIP) |

### Coordination Commands
All of the commands below require the role specified in the coord_roles_ids list or admin privileges. Furthermore, individuals with a role specified in the ignored_roles_ids list will not be affected when these commands are ran, the command author will also be exempt.

#### Voice Channel Management
| Command | Alias | Description |
| --- | --- | --- |
| mute | m | Mutes all users in the author's vc. |
| deafen | d | Mutes and deafens all users in the author's vc. |
| unmute | um | Unmutes all users in the author's vc. |
| undeafen | ud | Unmutes and undeafens all users in the author's vc. |
| move_out | out | Moves all users into the vc specified in the lobby_vc_id variable. |
| move_in \[mentions\] | in | Moves all users mentioned into the author's vc. |

#### Utilities
| Command | Alias | Description |
| --- | --- | --- |
| coin | flip, coinflip | Flips a coin. |
| seperator | seperate, sep | Posts a line seperator to help organise match text channels. |
| difference \[TA results\] | diff | Calculates the difference between two players from TA results. |
| pick_user | p_u | Picks a random person in the author's vc. | 
| pick_number \[value\] | pick_num, p_n | Picks a random number between 1 and the given argument. | 

### Administrator Commands
All of the commands below require admin privileges.

#### Configuration Commands
The bot **must** be configured before usage, otherwise the majority of commands won't work correctly.
Notes:
* Multiple roles can be given for set_coords and set_ignored. The IDs for each role need to be seperate by a space.
* A config will be automatically created when the bot joins a guild so config create would only be needed if the config has been removed.

| Command | Description |
| --- | --- |
| config | Posts the configuration for the current guild |
| config_raw | Posts the configuration for the current guild in a raw format. |
| config create | Creates a config for the guild. |
| config remove | Removes the guild from the config. |
| config set_prefix \[prefix\] | Sets the bot's prefix for the guild. |
| config set_lobby  \[vc ID\] | Sets the lobby vc id for the guild. |
| config set_coords \[role IDs\] | Sets the coordinator roles for the guild. |
| config set_ignored \[role IDs\] | Sets the ignored roles for the guild. |

#### Quality of Life Commands
Not necessarily needed for the bot to function.
| Command | Description |
| --- | --- |
| nickname | Changes the bot's nickname to the provided argument. |
| leave | Makes the bot leave the guild. |
| ta_to_txt \[message id\] | Parses the TA bot leaderboard to a txt file. Useful for importing the contents into a Google Sheet. |

### Super Duper Secret Commands
| Command | Alias | Description |
| --- | --- | --- |
| waifu | wa | Posts a waifu. |
| neko |  | Posts a neko. |

## Setting up Coordy McCoordFace
* Download the master branch.
* Install modules defined in 'requirements.txt' via pip.
* Create an .env file and define your bot's token in a variable named 'TOKEN'.
* Run 'bot.py'.
* Set-up Coordy with the [configuration commands](#Configuration Commands).

### config.json definitions
#### prefix
The value defined here will act as the bot's prefix.

#### lobby_vc_id
This value should be the ID for your discord server's lobby/waiting room voice channel.

#### beatkhana_id
This is the ID for the tournament's [BeatKhana!](https://beatkhana.com/) page. If an ID isn't configured than only the root BeatKhana! command will work. 

#### coord_roles_ids
This list should contain the role IDs for those who should have access to the coordination commands.

#### ignored_roles_ids
Roles defined in this list, as IDs, will be ignored by all coordination command. This may be helpful if there's casters or spectators in the same voice channel as players.

## To-Do
* Beatkhana brackets command
* Configurable Best Of X pick and ban procedure
* Google Translate command? (Blame the Austrians)
