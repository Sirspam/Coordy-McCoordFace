Coordy McCoordFace is a discord bot I've made to help assist in the coordination of Beat Saber tournaments.

## Commands
### General Commands
| Command | Description |
| --- | --- |
| links | Post an embed containing relevant links for the bot. |
| nickname | Changes the bot's nickname to the provided argument. Requires admin privileges. |
| leave | Makes the bot leave the guild. Requires admin privileges. |

### Coordination Commands
All of the commands below require the role specified in the coord_roles_ids list. Furthermore, individuals with a role specified in the ignored_roles list will not be affected when these commands are ran, the command author will also be exempt.
| Command | Alias | Description |
| --- | --- | --- |
| mute | m | Mutes all users in the author's vc |
| deafen | d | Mutes and deafens all users in the author's vc |
| unmute | um | Unmutes all users in the author's vc |
| undeafen | ud | Unmutes and undeafens all users in the author's vc |
| move_out | out | Moves all users into the vc specified in the lobby_vc_id variable |
| move_in \[mentions\] | in | Moves all users mentioned into the author's vc |
| beatsaver \[key\] | bs, bsr | Gets information on a certain beatmap |
| coin |  | Flips a coin |
| pick |  | Picks a random person in the author's vc | 

### Configuration Commands
All of the commands below require admin privileges.
Multiple roles can be given for set_coords and set_ignored. The IDs for each role needs to be seperate by a space.
| Command | Alias | Description |
| --- | --- | --- |
| config |  | Posts the configuration for the current guild |
| config create |  | Creates a config for the guild |
| config remove |  | Removes the guild from the config |
| config set_prefix \[prefix\] |  | Sets the bot's prefix for the guild |
| config set_lobby  \[vc ID\]|  | Sets the lobby vc id for the guild |
| config set_coords \[role IDs\]|  | Sets the coordinator roles for the guild |
| config set_ignored \[role IDs\]|  | Sets the ignored roles for the guild |

## Setting up Coordy McCoordFace
* Install modules defined in 'requirements.txt' via pip.
* Create an .env file and define your bot's token in a variable named 'TOKEN'.
* Run 'bot.py'.
* Set-up Coordy with the configuration commands.

### config.json definitions
#### prefix
The value defined here will act as the bot's prefix.
#### lobby_vc_id
This value should be the ID for your discord server's lobby/waiting room voice channel.
#### coord_roles_ids
This list should contain the role IDs for those who should have access to the coordination commands.
#### ignored_roles
Roles defined in this list, as a name or ID, will be ignored by all coordination command. This may be helpful if there's casters or spectators in the same voice channel as players.
