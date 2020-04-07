> skolk  [skål'k] substantiv ~et
>
> frånvaro från obligatorisk skolundervisning utan giltig anledning
> 
> äv. om annan frånvaro el. försummelse
>
> [Svensk Ordbok](https://svenska.se/so/?id=47195&pz=7)

## Installation

1. [Create a Discord bot account and invite the bot to your
   server.](https://discordpy.readthedocs.io/en/latest/discord.html)
2. Download required packages through pip, either globally or, if you're cool
   (unlike me), in a virtualenv.
   * apscheduler
   * discord.py

## Configuration

Configuration is done through a `config.json`. At the moment this is created and
written to manually. Soon&#8482 (#8) the configuration will be interactive.

## The output

The file `statistics.json` contains a list of all users who have at some point
been connected to any voice channel. `connected` contains the number of times the
user was connected during a check and `total` the number of checks since the
user was first checked. (Might change in the future, #3.)
