import argparse
import logging
import os
import random
import sys

import discord
import praw
from discord.ext import commands
from dotenv import load_dotenv


def generate_emoji(num_emojis: int) -> str:
    emojis = [
        "🙄", "😙", "😐", "🤤", "😤", "😲", "😬", "😭", "🥵", "🥺", "🤠", "🤫", "😳", "😢"
    ]
    output: str = ""
    for _ in range(num_emojis):
        output += random.choice(emojis) + "🍝"
    return output


# TODO: Add configuration to control logging
# and put logs somewhere that makes sense
def set_basic_logging():
    logging.basicConfig(
        format="%(asctime)s:%(name)s:%(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[
            logging.FileHandler("pastabot.log"),
            logging.StreamHandler()
        ],
    )


def set_advanced_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename="pastabot.log",
                                       encoding="utf-8")
    stdout_handler = logging.StreamHandler(sys.stdout)

    file_handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def get_reddit_posts(
        sort_type: str,
        num: int = 100) -> praw.models.listing.generator.ListingGenerator:
    posts = []
    if sort_type == "random":
        sort_type = random.choice(["hot", "top", "new"])

    if sort_type == "top":
        posts = pasta_sub.top(limit=num)
    if sort_type == "new":
        posts = pasta_sub.new(limit=num)
    else:
        posts = pasta_sub.hot(limit=num)

    logging.info(f"Getting {num} posts from sort type {sort_type}")

    return posts


def log_discord_command(command_name: str, discord_user: str):
    logging.info(f'"{command_name}" command issued by "{discord_user}"')


async def print_post_message(ctx, posts, post_limit):
    for i, post in enumerate(posts):
        if i == post_limit - 1:
            await ctx.send(post.title + "\n")
            if post.selftext:
                if len(post.selftext) < 2000:
                    await ctx.send(post.selftext)
                else:
                    for m in range(0, len(post.selftext), 1500):
                        await ctx.send(post.selftext[m:m + 1500])
            await ctx.send("sauce: " + post.url)


async def list_posts_message(ctx, posts, post_limit, sort_type):
    msg_output = ""
    for i, post in enumerate(posts):
        msg_output += "\U00002B06 {}\n".format(post.score)
        msg_output += "{0} post: {1}: {2}\n\n".format(sort_type, str(i + i),
                                                      post.title)

    await ctx.send(msg_output)


def create_bot_commands():
    @bot.event
    async def on_ready():
        logging.info("PastaBot is online")
        await bot.change_presence(status=discord.Status.online,
                                  activity=discord.Game('pasta!help'))

    @bot.command(help="""Lists a number posts from a sort type.
        Arg 1: Sorting type [hot|new|top]
        Arg 2: Number of submission to fetch""",
                 aliases=["l", "li"])
    async def list(ctx, sort_type: str, post_limit: int):
        log_discord_command("list", ctx.author)
        posts = get_reddit_posts(sort_type, post_limit)
        await list_posts_message(ctx, posts, post_limit, sort_type)

    @bot.command(help="""Get a specific post from a sorting type.
        Arg 1: Sorting type [hot|new|top]
        Arg 2: Number of submission to fetch""",
                 aliases=["g", "ge"])
    async def get(ctx, sort_type: str, post_limit: int):
        log_discord_command("get", ctx.author)
        posts = get_reddit_posts(sort_type, post_limit)
        await print_post_message(ctx, posts, post_limit)

    @bot.command(help="""Picks a random post (out of 100).
        If no sorting is specified, a random one is chosen.
        Optional Arg 1: Sorting type [hot|new|top]
        Optional Arg 2: Max post limit""",
                 aliases=["r", "random"])
    async def rand(ctx, sort_type: str = "random", post_limit: int = 50):
        log_discord_command(sort_type, ctx.author)
        post_limit = random.randint(1, post_limit)
        posts = get_reddit_posts(sort_type, post_limit)
        await print_post_message(ctx, posts, post_limit)


def main():
    global pasta_sub
    global bot

    load_dotenv()

    parser = argparse.ArgumentParser(description="pasta_bot options")
    parser.add_argument(
        "--discord-bot-token",
        type=str,
        default=os.environ.get("DISCORD_BOT_TOKEN"),
    )

    parser.add_argument(
        "--reddit-id",
        type=str,
        default=os.environ.get("REDDIT_ID"),
    )

    parser.add_argument(
        "--reddit-secret",
        type=str,
        default=os.environ.get("REDDIT_SECRET"),
    )

    parser.add_argument("--reddit-UA", type=str, default="PastaBot 0.0.1")
    parser.add_argument("--subreddits",
                        type=str,
                        default="copypasta+emojipasta")

    args = parser.parse_args()

    # TODO: Read from a configuration file where options can be specified
    if not args.reddit_id:
        print(
            "Error: please supply REDDIT_ID as environment variable or flag",
            file=sys.stderr,
        )
        sys.exit(parser.print_usage())
    if not args.reddit_secret:
        print(
            "Error: please supply REDDIT_SECRET as environment variable or flag",
            file=sys.stderr,
        )
        sys.exit(parser.print_usage())
    if not args.discord_bot_token:
        print(
            "Error: please supply DISCORD_BOT_TOKEN as environment variable or flag",
            file=sys.stderr,
        )
        sys.exit(parser.print_usage())

    reddit = praw.Reddit(
        client_id=args.reddit_id,
        client_secret=args.reddit_secret,
        user_agent="PastaBot 0.0.1",
    )

    pasta_sub = reddit.subreddit(args.subreddits)

    help_cmd = commands.DefaultHelpCommand(no_category="Commands", width=120)

    description = """I get copypasta posts from Reddit\n
    Prefix Aliases are: \"pastabot!\", \"pasta!\", \"pb!\", \"p!\" \n
    Examples:
    +-----------------------------------------------------------+
    | Command       | Description                               |
    +---------------+-------------------------------------------+
    | p!rand        | Get random submission from 100 hot pastas |
    | p!rand top 10 | Get random submission from 10 top pastas  |
    | p!get new 10  | Get 10th submission from new              |
    | p!list top 10 | List 10 submissions from top              |
    +---------------+-------------------------------------------+
    """

    bot = commands.Bot(
        command_prefix=commands.when_mentioned_or("pasta!", "pastabot!", "pb!",
                                                  "p!"),
        description=description,
        help_command=help_cmd,
    )

    logging.info("*" * 10)
    logging.info("PastaBot has started")
    logging.info("*" * 10)

    create_bot_commands()
    bot.run(args.discord_bot_token)

    logging.info("*" * 10)
    logging.info("PastaBot has shut down")
    logging.info("*" * 10)


set_basic_logging()
main()
