# Coordy McCoordFace
[![CodeFactor](https://www.codefactor.io/repository/github/sirspam/coordy-mccoordface/badge)](https://www.codefactor.io/repository/github/sirspam/coordy-mccoordface)

Coordy McCoordFace is a discord bot I've made to help assist in the coordination of Beat Saber tournaments.

[Invite Link](https://discord.com/api/oauth2/authorize?client_id=813699805150838795&permissions=29748288&scope=bot) (Currently not hosted 24/7. it's recommended to locally host it yourself.)

[Support Server](https://discord.gg/dWX6fpGUK9)

## Readme Index
* [Coordy McCoordFace](#Coordy-McCoordFace)
* [Readme Index](#Readme-Index) (You're already here!)
* [Commands](#Commands)
    * [General Commands](#General-Commands)
        * [BeatKhana! Commands](#BeatKhana-Commands)
        * [Super Duper Secret Commands](#Super-Duper-Secret-Commands)
    * [Coordination Commands](#Coordination-Commands)
        * [Voice Channel Management](#Voice-Channel-Management)
        * [Utilities](#Utilities)
    * [Administrator Commands](#Administrator-Commands)
        * [General Admin Commands](#General-Admin-Commands)
        * [Configuration Commands](#Configuration-Commands)
* [Hosting Coordy McCoordFace](#Setting-up-Coordy-McCoordFace)
* [Previous Tournaments Coordy Has Been Used In](#Previous-Tournaments-Coordy-Has-Been-Used-In)


## Commands
The default prefix for Coordy is `CC ` although it can be changed with the [Configuration Commands](#Configuration-Commands).
If you set a custom prefix but forget it, mentioning the bot also works as a viable prefix. The help command will display the current prefix.

Commands under the [General Commands](#General-Commands) header can be used by anyone
Commands under the [Coordination Commands](#Coordination-Commands) header can only be used by admins or those with the coordination role / roles specified in the config
Commands under the [Administrator Commands](#Administrator-Commands) header can only be used by admins

[ ] represents a required parameter while ( ) represents an optional parameter.

### General Commands
| Command | Alias | Description |
| --- | --- | --- |
| help | | Posts a help message |
| links |  | Post an embed containing relevant links for the bot. |
| beatsaver \[key\] \(difficulty\)| bs, bsr | Gets information on a certain beatmap. |
| beatsaver search \[query\] | map, s | Searches for maps on BeatSaver |

#### BeatKhana! Commands
| Command | Alias | Description |
| --- | --- | --- |
| beatkhana \[mention\] | bk | Gets information on a mentioned user from BeatKhana! |
| beatkhana tournament | tourney, t | Gets general information on the tournament |
| beatkhana maps | maps, m | Gets information on the tournament map pool |
| beatkhana brackets | bracket, b | Gets information on the tournament bracket (WIP) |
| beakthana qualifiers | quals, q | Gets information on the tournament qualifiers |
| beatkhana staff | s | Gets information on the tournament staff |

#### Super Duper Secret Commands
| Command | Alias | Description |
| --- | --- | --- |
| waifu | wa | Posts a waifu. |
| neko | nya | Posts a neko. |

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
| seperator \(text\) | seperate, sep | Posts a line seperator to help organise match text channels. Includes text in seperator line if provided.|
| difference \[TA results\] | diff | Calculates the difference between two players from TA results. |
| multistream \(mentions\) | ms | Generates a [Multistream](https://multistre.am/) link with either mentioned users or users in vc. |
| pick_user | p_u | Picks a random person in the author's vc. | 
| pick_number \[value\] | pick_num, p_n | Picks a random number between 1 and the given argument. | 

### Administrator Commands
All of the commands below require admin privileges.

#### General Admin Commands
| Command | Description |
| --- | --- |
| nickname | Changes the bot's nickname to the provided argument. |
| leave | Makes the bot leave the guild. |
| ta_to_txt \[message id\] | Parses the TA bot leaderboard to a txt file. Useful for importing the contents into a Google Sheet. |

#### Configuration Commands
The bot **must** be configured before usage, otherwise the majority of commands won't work correctly.
Notes:
* Multiple roles can be given for set_coords and set_ignored. The IDs for each role need to be seperate by a space.
* A config will be automatically created when the bot joins a guild or if it detects there's no config when running a command which accesses it.

| Command | Description |
| --- | --- |
| config | Posts the configuration for the current guild |
| config raw | Posts the configuration for the current guild in a raw format. |
| config remove | Removes the guild from the config. |
| config set_prefix \[prefix\] | Sets the bot's prefix for the guild. |
| config set_lobby  \[vc ID\] | Sets the lobby vc id for the guild. |
| config set_coords \[role IDs\] | Sets the coordinator roles for the guild. |
| config set_ignored \[role IDs\] | Sets the ignored roles for the guild. |


## Hosting Coordy McCoordFace
* Download the master branch.
* Install modules defined in 'requirements.txt' via pip.
* Create an .env file and define your bot's token in a variable named 'TOKEN'.
* Run 'bot.py'.
* Invite the bot to your server and set-up the config with the [configuration commands](#Configuration-Commands).

## Previous Tournaments Coordy Has Been Used In
* Scuffed Tourneys
* Cillerian e-Sports
* LMAO Clan Double Elimination
* [Dach Tournament Season 1](https://beatkhana.com/tournament/2147484227)
* [NBST Spring 2021](https://beatkhana.com/tournament/2147484215)
* [Beat Sage Royale](https://beatkhana.com/tournament/2147484230)
* [ATI - Austrian Tournament 1](https://beatkhana.com/tournament/2147484231)
* [115 Royale](https://beatkhana.com/tournament/2147484236)