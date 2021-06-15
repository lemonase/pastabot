# PastaBot 🍝

Made with ♥ for all the copypasta lovers.

This bot fetches submissions from [/r/copypasta](https://reddit.com/r/copypasta)
and [/r/emojipasta](https://reddit.com/r/emojipasta) and sends them as a message
in Discord.

## Adding the bot to a server

Anyone is welcome to add the bot!

You can check it out on [Top.gg](https://top.gg/bot/802369923845455933) (moderated site for Discord bots)

or

Follow [this link](https://discord.com/api/oauth2/authorize?client_id=802369923845455933&permissions=280576&scope=bot)
directly to authorize and add to your server:

It should have the following permissions in the server - no more and no less:

- Send Messages
- Embed Links
- Use External Emojis

## Usage

### Commands

Command Prefixes = `pastabot!` | `pasta!` | `pb!` | `p!`

Full Commands:

- `pasta!get [hot|top|new] <count>`
  Get a singular copypasta that is \<count\> posts from the top.
- `pasta!list [hot|top|new] <count>`
  Lists title of the top \<count\> copypasta posts.
- `pasta!rand [hot|top|new] [<count>]`
  Get a random copypasta where \<count\> is the max. (Default is 50)
- `pasta!show <url>`
  Sends a message with the contents of post body from the URL supplied

Short Commands:

- `pasta!get`
  - alias: `p!g`
- `pasta!list`
  - alias: `p!l`
- `pasta!random`
  - alias: `p!r`
- `pasta!show`
  - alias: `p!s`

## Running

### Getting API keys

The script currently needs some API credentials from both Discord and Reddit.

#### Discord Client ID

1. Go to the Discord API portal:
   https://discord.com/developers/applications

2. Click "New Application" button on top right, name it anything

3. In the newly created application, go to the "Bot" tab on the menu on the left

4. Under "Build A Bot" there will be a token label with a Copy button.
   Copy that token

5. Set your environment variable `DISCORD_BOT_TOKEN=<YOUR_BOT_TOKEN>`

#### Reddit ID and Secret

1. Go to the Reddit app portal:
   https://www.reddit.com/prefs/apps/

2. Create a "script" type key and name it whatever

3. Copy your Client ID (not labelled, but found in bold under the name of the script)
   and the Client Secret (is labelled).

4. Set environment variables `REDDIT_ID=<YOUR_CLIENT_ID>`
   and the Client Secret as `REDDIT_SECRET=<YOUR_CLIENT_SECRET>`

#### Storing credentials using dotenv

Environment variables can be stored in a `.env` in the directory where the
project is run. In the future, I may decide to use a configuration file instead.

### Running the bot

In the examples below, I assume that all API credentials are in their
corresponding environment variables or in a `.env` file.

#### Running Locally

```sh
git clone https://github.com/lemonase/pastabot.git
cd pastabot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 src/bot.py
```

#### Running with Docker

Running with a `.env` file in the current directory:

```sh
docker run -d --env-file $(PWD)/.env jamesdixon/pastabot:latest
```

Running with environment variables:

```sh
docker run -d -e REDDIT_ID=<YOUR_ID> \
              -e REDDIT_SECRET=<YOUR_SECRET> \
              -e DISCORD_BOT_TOKEN=<YOUR_TOKEN> \
              jamesdixon/pastabot
```

## Libraries used

- [PRAW](https://github.com/praw-dev/praw)
- [Discord.py](https://github.com/Rapptz/discord.py)

## TODOs

- Upgrade to AsyncPRAW
