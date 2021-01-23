# Copybotsa

This is a simple copypasta bot for Discord.
It fetches submissions from /r/copypasta and writes them in Discord.

## Commands (so far)

Command Prefix(es) = "pasta!" | "pastabot!" | "pb!" | "p!"

Commands:
- `get [hot|top|new] count` Return a singular copypasta that is <count> posts from the top.
- `list [hot|top|new] count` Lists the titles of the top <count> copypasta posts.
- `rand [hot|top|new] count` Get a random copypasta where <count> is the max. 

## Installation

```sh
git clone ...
pip install -r requirements.txt
python3 copybotsa.py
```

## Libraries used

- [PRAW](https://github.com/praw-dev/praw)
- [Discord.py](https://github.com/Rapptz/discord.py)
