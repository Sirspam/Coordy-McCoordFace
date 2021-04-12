Coordy McCoordFace is a discord bot I've made to help assist in the coordination of Beat Saber tournaments.

## Commands
### General commands
| Command | Description |
| --- | --- |
| links | Post an embed containing relevant links for the bot. |
| nickname | Changes the bot's nickname to the provided argument. Requires admin privileges. |
| leave | Makes the bot leave the guild. Requires admin privileges. |

### Coordination commands
All of the commands below require the role specified in the coord_roles_ids list. Furthermore, individuals with a role specified in the ignored_roles list will not be affected when these commands are ran, the command author will also be exempt.
| Command | Alias | Description |
| --- | --- | --- |
| mute | m | Mutes and deafens all users in the author's vc |
| unmute | um | Unmutes and undeafens all users in the author's vc |
| move_out | out | Moves all users into the vc specified in the lobby_vc_id variable |
| move_in \[mentions\] | in | Moves all users mentioned into the author's vc |
| coin |  | Flips a coin |
| pick |  | Picks a random person in the author's vc | 

## Setting up Coordy McCoordFace
* Install modules defined in 'requirements.txt' via pip.
* Create an .env file and define your bot's token in a variable named 'TOKEN'.
* Rename 'example_config.json' to 'config.json' and alter the values appropriately.
* Run 'bot.py'

### config.json definitions
#### prefix
The value defined here will act as the bot's prefix.
#### lobby_vc_id
This value should be the ID for your discord server's lobby/waiting room voice channel.
#### coord_roles_ids
This list should contain the role IDs for those who should have access to the coordination commands.
#### ignored_roles
Roles defined in this list, as a name or ID, will be ignored by all coordination command. This may be helpful if there's casters or spectators in the same voice channel as players.