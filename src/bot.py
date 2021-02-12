""" Discord bot main module

This modules is where all the action happens.
It takes care of parsing arguments, environment variables, creating
the clients, setting up the logger and running the bot.
"""
import argparse
import os
import random
import pathlib
import sys

import asyncio
import asyncpraw

import discord
import logger
from discord.ext import commands
from dotenv import load_dotenv

__version__ = "0.0.2"
DEFAULT_SUBS = "copypasta"


def get_args():
    """ Returns arguments passed in from the command line """
    load_dotenv()

    cmd_parser = argparse.ArgumentParser(
        description="PastaBot ver {} options".format(__version__)
    )

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
    cmd_parser.add_argument("--log-path", type=pathlib.Path)
    cmd_parser.add_argument("--version", action="store_true")

    args = cmd_parser.parse_args()

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

    if args.version:
        print("PastaBot ver {}".format(__version__))
        sys.exit(0)

    return args


def get_reddit_client(args):
    client = asyncpraw.Reddit(
        client_id=args.reddit_id,
        client_secret=args.reddit_secret,
        user_agent=args.reddit_ua,
    )
    return client


def get_subreddit_client(client, args):
    """ Returns a async praw object that represents one (or multiple) subreddits """
    return client.subreddit(args.subreddits, fetch=True)


def get_discord_bot(args):
    """ Returns a discord.py bot which we will use to listen to commands """
    help_cmd = commands.DefaultHelpCommand(no_category="Commands", width=120)
    description = """Hello I am PastaBot, I get copypasta posts from Reddit
    so you don't have to!

    Prefixs: \"pastabot!\" | \"pasta!\" | \"pb!\" | \"p!\"
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
        logger.logging.info("* PastaBot is online *")
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
        posts = get_reddit_posts(subreddit, sort_type, post_limit)
        await discord_utils.list_posts_as_msg(ctx, posts, post_limit, sort_type)

    @bot.command(
        help="""Get a specific post from a sorting type.
        Arg 1: Sorting type [hot|new|top]
        Arg 2: Number of submission to fetch""",
        aliases=["g", "ge"],
    )
    async def get(ctx, sort_type: str, post_limit: int):
        logger.log_discord_command("get", ctx.author)
        posts = get_reddit_posts(subreddit, sort_type, post_limit)
        await send_post_msg(ctx, posts, post_limit)

    @bot.command(
        help="""Picks a random post (out of 100).
        If no sorting is specified, a random one is chosen.
        Optional Arg 1: Sorting type [hot|new|top]
        Optional Arg 2: Max post limit""",
        aliases=["r", "random"],
    )
    async def rand(ctx, sort_type: str = "random", post_limit: int = 50):
        logger.log_discord_command("rand", ctx.author)
        post_limit = random.randint(1, post_limit)
        posts = await get_reddit_posts(subreddit, sort_type, post_limit)
        await send_post_msg(ctx, posts, post_limit)


# Discord Utils


async def send_post_msg(ctx, posts, post_limit):
    """Takes discord context, reddit posts and number of posts
    and uses the discord discord context to send the post as a discord message
    """
    for i, post in enumerate(posts):
        if i == post_limit - 1:
            await ctx.send("🍝 " + post.title + "\n" + "-" * 10)

            if post.selftext:
                if len(post.selftext) < 2000:
                    await ctx.send(post.selftext)
                else:
                    for m in range(0, len(post.selftext), 1500):
                        await ctx.send(post.selftext[m : m + 1500])
            await ctx.send("sauce: " + post.url)


async def list_posts_as_msg(ctx, posts, post_limit, sort_type):
    """Takes discord context, reddit posts, number of posts, and the sort_type
    and uses the discord context to send the titles as a message
    """
    msg_output = ""
    for i, post in enumerate(posts):
        msg_output += "\U00002B06 {}\n".format(post.score)
        msg_output += "{0} post: {1}: {2}\n\n".format(sort_type, str(i + i), post.title)

    await ctx.send(msg_output)


# Reddit Utils


async def get_reddit_posts(target_sub, sort_type: str, num: int = 100):
    """Takes a praw subreddit model, sort type, and a limit for num of posts retrieved
    The returned object is a generator, so posts are not really "fetched" until iterated on
    """
    posts = []
    if sort_type == "random":
        sort_type = random.choice(["hot", "top", "new"])

    if sort_type == "top":
        posts = target_sub.top(limit=num)
    if sort_type == "new":
        posts = target_sub.new(limit=num)
    else:
        posts = target_sub.hot(limit=num)

    logger.logging.info("Getting %s posts sorted by: %s", num, sort_type)

    return posts


async def init_reddit(args):
    global subreddit
    reddit = get_reddit_client(args)
    subreddit = await get_subreddit_client(reddit, args)
    await reddit.close()


def init_discord(args):
    global bot
    bot = get_discord_bot(args)
    create_bot_callbacks()
    bot.run(args.discord_bot_token)


async def main():
    """ Main entrypoint for the bot """
    # get arguments
    args = get_args()
    # start logging
    logger.set_basic_logger(filename=logger.get_log_filename(args))
    logger.log_action("started")
    # init clients
    await init_reddit(args)
    init_discord(args)
    # stop logging
    logger.log_action("shutdown")


if __name__ == "__main__":
    # asyncio.run(main())

    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
