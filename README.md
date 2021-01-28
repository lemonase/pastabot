# PastaBot

Made with ♥ for all you copypasta lovers.

It fetches submissions from [/r/copypasta](https://reddit.com/r/copypasta) and writes them as a message in Discord.

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

The script currently needs some API credentials from both Discord and Reddit.

### Discord Client ID

1. Go to the Discord API portal:
   https://discord.com/developers/applications

2. Create a discord bot application

3. Copy the "Client ID"

4. Set environment variable `DISCORD_BOT_TOKEN=<client id>`

### Reddit ID and Secret

1. Go to the Reddit app portal:
   https://www.reddit.com/prefs/apps/

2. Create a "script" type key and name it whatever

3. Copy your Client ID (not labelled, but found under the name of the script)
   and the Client Secret (is labelled).

4. Set environment variable `REDDIT_ID=<client id>` and the Client Secret as `REDDIT_SECRET=<client secret>`

### Storing credentials using dotenv

Instead of setting environment variables, you can also put credentials in
a `.env` file in the project root and they will also be picked up.

### Running

Below, I'm assuming the correct API credentials are in corresponding environment variables.

```sh
git clone https://github.com/lemonase/copybotsa.git
cd copybotsa
pip install -r requirements.txt
python3 copybotsa.py
```

## Libraries used

- [PRAW](https://github.com/praw-dev/praw)
- [Discord.py](https://github.com/Rapptz/discord.py)

## TODOs

- Make a more helpful/prettier help message
- Have bot respond when someone mentions @PastaBot
- Show Upvotes/Downvotes in title
- Store logs somewhere other than the project root
- Read settings like user_agent, subreddits, default_post_limit, credentials, etc., from a configuration file
