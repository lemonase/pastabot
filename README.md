# Copybotsa

This is a simple copypasta bot for Discord.
It fetches submissions from /r/copypasta and writes them in Discord.

## Commands (so far)

Command Prefix(es) = `pasta!` | `pastabot!` | `pb!` | `p!`

Commands:
- `pasta!get [hot|top|new] <count>` Return a singular copypasta that is <count> posts from the top.
    - aliases: `g`, `ge`
- `pasta!list [hot|top|new] <count>` Lists the titles of the top <count> copypasta posts.
    - aliases: `l`, `li`
- `pasta!rand [hot|top|new] [<count>]` Get a random copypasta where <count> is the highest number. Default is 50
    - aliases: `r`, `random`

## Installation

The script currently needs API credentials from both
Discord and Reddit.

### Discord Client ID

1. Go to the Discord API portal:
https://discord.com/developers/applications

2. Create a discord bot application

3. Copy the "Client ID"

### Reddit Credentials

1. Go to the Reddit app portal:
https://www.reddit.com/prefs/apps/

2. Create a "script" type key and name it whatever

3. Copy your Client ID (not labelled, but found under the name of the script)
and the Client Secret (is labelled).

### Running

Below, I'm assuming the correct API credentials are in corresponding environment variables.

```sh
git clone https://github.com/lemonase/copybotsa.git
cd copybotsa
pip install -r requirements.txt
python3 copybotsa.py --discord-bot-token $DISCORD_BOT_TOKEN --reddit-id $REDDIT_ID --reddit-secret $REDDIT_SECRET
```

## Libraries used

- [PRAW](https://github.com/praw-dev/praw)
- [Discord.py](https://github.com/Rapptz/discord.py)
