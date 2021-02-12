# PastaBot

Made with ♥ for all you copypasta lovers.

It fetches submissions from [/r/copypasta](https://reddit.com/r/copypasta) and writes them as a message in Discord.

## Commands (so far)

Command Prefixes = `pastabot!` | `pasta!` | `pb!` | `p!`

Commands:

- `pasta!get [hot|top|new] <count>`
  Return a singular copypasta that is <count> posts from the top.
  - aliases: `g`, `ge`
- `pasta!list [hot|top|new] <count>`
  Lists the titles of the top <count> copypasta posts.
  - aliases: `l`, `li`
- `pasta!rand [hot|top|new] [<count>]`
  Get a random copypasta where <count> is the highest number. Default is 100
  - aliases: `r`, `random`

## Installation

The script currently needs some API credentials from both Discord and Reddit.

### Discord Client ID

1. Go to the Discord API portal:
   https://discord.com/developers/applications

2. Click "New Application" button on top right, name it anything

3. In you newly created application, go to the "Bot" tab on the left

4. Under "Build A Bot" there will be a token label with a Copy button.
   Copy that token

5. Set your environment variable `DISCORD_BOT_TOKEN=<YOUR_BOT_TOKEN>`

### Reddit ID and Secret

1. Go to the Reddit app portal:
   https://www.reddit.com/prefs/apps/

2. Create a "script" type key and name it whatever

3. Copy your Client ID (not labelled, but found in bold under the name of the script)
   and the Client Secret (is labelled).

4. Set environment variables `REDDIT_ID=<YOUR_CLIENT_ID>`
   and the Client Secret as `REDDIT_SECRET=<YOUR_CLIENT_SECRET>`

### Storing credentials using dotenv

Environment variables can also be stored in a `.env` in the directory where the
project is run. In the future, I may decide to use a configuration file instead.

### Running

Below, I'm assuming all API credentials are in their corresponding
environment variables.

```sh
git clone https://github.com/lemonase/pastabot.git
cd pastabot
pip install -r requirements.txt
python3 src/bot.py
```

## Libraries used

- [PRAW](https://github.com/praw-dev/praw)
- [Discord.py](https://github.com/Rapptz/discord.py)

## TODOs

- Store logs somewhere other than the project root
- Read settings like user_agent, subreddits, default_post_limit, credentials, etc., from a configuration file
- Upgrade to AsyncPRAW
