## Commands
### General commands
| Command | Description |
| --- | --- |
| links | Post an embed containing relevent links for the bot. |
| nickname | Changes the bot's nickname to the provided argument. Requires admin privilages. |
| leave | Makes the bot leave the guild. Requires admin privilages. |

### Coordination commands
All of the commands below require the role specified in the coord_roles_ids list. Furthermore, individuals with a role specified in the ignored_roles list will not be effected when these commands are ran, the command author will also be excempt.
| Command | Alias | Description |
| --- | --- | --- |
| mute | m | Mutes and deafens all users in the author's vc |
| unmute | um | Unmutes and undeafens all users in the author's vc |
| move_out | mout | Moves all users into the vc specified in the lobby_vc_id variable |
| move_in <mentions> | min | Moves all users mentioned into the author's vc |


