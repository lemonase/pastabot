""" Discord bot main module

This modules is where all the action happens.
It takes care of parsing arguments, environment variables, creating
the clients, setting up the logger and running the bot.
"""
import argparse
import os
import random
import sys

import praw

import discord
import discord_utils
import emoji_utils
import logger
import reddit_utils
from discord.ext import commands
from dotenv import load_dotenv

__version__ = "0.0.2"
DEFAULT_SUBS = "copypasta+emojipasta"


def get_args():
    """ Returns arguments passed in from the command line """
    load_dotenv()

    cmd_parser = argparse.ArgumentParser(description="pasta_bot options")
    cmd_parser.add_argument(
        "--discord-bot-token",
        type=str,
        default=os.environ.get("DISCORD_BOT_TOKEN"),
    )

    cmd_parser.add_argument(
        "--reddit-id",
        type=str,
        default=os.environ.get("REDDIT_ID"),
    )

    cmd_parser.add_argument(
        "--reddit-secret",
        type=str,
        default=os.environ.get("REDDIT_SECRET"),
    )

    cmd_parser.add_argument("--reddit-ua", type=str, default="PastaBot " + __version__)
    cmd_parser.add_argument("--subreddits", type=str, default=DEFAULT_SUBS)

    args = cmd_parser.parse_args()

    # TODO: Read from a configuration file where options can be specified
    if not args.reddit_id:
        print(
            "Error: please supply REDDIT_ID as environment variable or flag",
            file=sys.stderr,
        )
        sys.exit(cmd_parser.print_usage())
    if not args.reddit_secret:
        print(
            "Error: please supply REDDIT_SECRET as environment variable or flag",
            file=sys.stderr,
        )
        sys.exit(cmd_parser.print_usage())
    if not args.discord_bot_token:
        print(
            "Error: please supply DISCORD_BOT_TOKEN as environment variable or flag",
            file=sys.stderr,
        )
        sys.exit(cmd_parser.print_usage())

    return args


def get_subreddit_client(args):
    """ Returns a praw object that represents one (or multiple) subreddits """
    reddit_client = praw.Reddit(
        client_id=args.reddit_id,
        client_secret=args.reddit_secret,
        user_agent=args.reddit_ua,
    )
    return reddit_client.subreddit(args.subreddits)


def get_discord_bot(args):
    """ Returns a discord.py bot which we will use to listen to commands """
    help_cmd = commands.DefaultHelpCommand(no_category="Commands", width=120)
    description = """Hello I am PastaBot, I get copypasta posts from Reddit
    so you don't have to!

    Prefix from longest to shortest: \"pastabot!\", \"pasta!\", \"pb!\", \"p!\"
    or you can mention @PastaBot with a command

    Examples:
    ---------
    p!rand
    Get random submission (defaults to 100 hot pastas)

    p!rand top 10
    Get random submission from 10 top pastas

    p!get new 10
    Get 10th submission from new

    p!list top 10
    List 10 submissions from top
    """
    pastabot = commands.Bot(
        command_prefix=commands.when_mentioned_or("pasta!", "pastabot!", "pb!", "p!"),
        description=description,
        help_command=help_cmd,
    )

    return pastabot


def create_bot_callbacks():
    """ This function creates async callback functions for bot events like commands """

    @bot.event
    async def on_ready():
        logger.logging.info("PastaBot is online")
        await bot.change_presence(
            status=discord.Status.online, activity=discord.Game("pasta!help")
        )

    @bot.command(
        help="""Lists a number posts from a sort type.
        Arg 1: Sorting type [hot|new|top]
        Arg 2: Number of submission to fetch""",
        aliases=["l", "li"],
    )
    async def list(ctx, sort_type: str, post_limit: int):
        logger.log_discord_command("list", ctx.author)
        posts = reddit_utils.get_posts(sub, sort_type, post_limit)
        await discord_utils.list_posts_as_msg(ctx, posts, post_limit, sort_type)

    @bot.command(
        help="""Get a specific post from a sorting type.
        Arg 1: Sorting type [hot|new|top]
        Arg 2: Number of submission to fetch""",
        aliases=["g", "ge"],
    )
    async def get(ctx, sort_type: str, post_limit: int):
        logger.log_discord_command("get", ctx.author)
        posts = reddit_utils.get_posts(sub, sort_type, post_limit)
        await discord_utils.send_post_as_msg(ctx, posts, post_limit)

    @bot.command(
        help="""Picks a random post (out of 100).
        If no sorting is specified, a random one is chosen.
        Optional Arg 1: Sorting type [hot|new|top]
        Optional Arg 2: Max post limit""",
        aliases=["r", "random"],
    )
    async def rand(ctx, sort_type: str = "random", post_limit: int = 50):
        logger.log_discord_command(sort_type, ctx.author)
        post_limit = random.randint(1, post_limit)
        posts = reddit_utils.get_posts(sub, sort_type, post_limit)
        await discord_utils.send_post_as_msg(ctx, posts, post_limit)


def main():
    """ Main entrypoint for the bot """
    # bot must be global for function decorators
    global bot
    global sub

    # get arguments and create clients
    args = get_args()
    sub = get_subreddit_client(args)
    bot = get_discord_bot(args)

    # output logging header
    logger.set_basic_logger()
    logger.log_begin()

    # define async callback functions and run the bot
    create_bot_callbacks()
    bot.run(args.discord_bot_token)

    # stop logging
    logger.log_end()


if __name__ == "__main__":
    main()