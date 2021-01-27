import argparse
import logging
import os
import random
import sys

import praw
from discord.ext import commands
from dotenv import load_dotenv


def generate_emoji(num_emojis: int) -> str:
    emojis = [
        "🙄", "😙", "😐", "🤤", "😤", "😲", "😬", "😭", "🥵", "🥺", "🤠", "🤫", "😳", "😢"
    ]
    s: str = ""
    for i in range(num_emojis):
        s += random.choice(emojis) + "🍝"
    return s


def set_basic_logging():
    logging.basicConfig(
        encoding="utf-8",
        format="%(asctime)s:%(name)s:%(levelname)s - %(message)s",
        level=logging.INFO,
        handlers=[
            logging.FileHandler("copybotsa.log"),
            logging.StreamHandler()
        ]
    )


def set_advanced_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(filename="copybotsa.log",
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
    if sort_type == "random" or sort_type not in ["hot", "top", "new"]:
        sort_type = random.choice(["hot", "top", "new"])

    if sort_type == "hot":
        posts = pasta_sub.hot(limit=num)
    if sort_type == "top":
        posts = pasta_sub.top(limit=num)
    if sort_type == "new":
        posts = pasta_sub.new(limit=num)

    logging.info(f"Getting {num} posts from sort type {sort_type}")

    return posts


def log_discord_command(command_name: str, discord_user: str):
    logging.info(f'🍝 {command_name} command issued by "{discord_user}" 🍝')


def create_bot_commands():
    @bot.command(
        help="""Lists a number posts from a sort type.
        First arg is sort type and second is number""",
        aliases=["l", "li"],
    )
    async def list(ctx, sort_type: str, post_limit: int):
        log_discord_command("list", ctx.author)
        posts = get_reddit_posts(sort_type, post_limit)

        for i, post in enumerate(posts):
            await ctx.send(sort_type + " post: " + str(i + 1) + ": " +
                           post.title)

    @bot.command(
        help="""Get a specific post from a sorting type.
        First arg is sorting type and second is a number""",
        aliases=["g", "ge"],
    )
    async def get(ctx, sort_type: str, post_limit: int):
        log_discord_command("get", ctx.author)
        posts = get_reddit_posts(sort_type, post_limit)

        for i, post in enumerate(posts):
            if i == post_limit - 1:
                await ctx.send(sort_type + " pasta #" + str(i + 1) + ": " +
                               post.title)
                if post.selftext:
                    await ctx.send(post.selftext)
                if post.url:
                    await ctx.send("sauce: " + post.url)

    @bot.command(
        help="""Picks a random post (out of 100).
        If no sorting is specified, a random one is chosen.
        Optional Arg 1: Sorting type [hot|new|top]
        Optional Arg 2: Max post limit""",
        aliases=["r", "random"],
    )
    async def rand(ctx, sort_type: str = "random", post_limit: int = 50):
        log_discord_command(sort_type, ctx.author)
        post_limit = random.randint(1, post_limit)
        posts = get_reddit_posts(sort_type, post_limit)

        for i, post in enumerate(posts):
            if i == post_limit - 1:
                await ctx.send(sort_type + " pasta #" + str(i + 1))

                if post.title:
                    await ctx.send(post.title)

                if post.selftext:
                    if len(post.selftext) < 2000:
                        await ctx.send(post.selftext)
                    else:
                        for m in range(0, len(post.selftext), 1500):
                            await ctx.send(post.selftext[m:m + 1500])

                if post.url:
                    await ctx.send("sauce: " + post.url)


def main():
    global pasta_sub
    global bot

    load_dotenv()

    # discord_bot_token = os.environ.get('DISCORD_BOT_TOKEN')
    # reddit_id = os.environ.get('REDDIT_ID')
    # reddit_secret = os.environ.get('REDDIT_SECRET')

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
    args = parser.parse_args()

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

    pasta_sub = reddit.subreddit("copypasta+emojipasta")

    help_cmd = commands.DefaultHelpCommand(no_category="Commands")
    description = "I get copypasta posts from Reddit"
    bot = commands.Bot(
        command_prefix=["pasta!", "pastabot!", "pb!", "p!"],
        description=description,
        help_command=help_cmd,
    )

    logging.info(generate_emoji(6))
    logging.info("PastaBot has started")
    logging.info(generate_emoji(6))

    create_bot_commands()
    bot.run(args.discord_bot_token)

    logging.info(generate_emoji(6))
    logging.info("PastaBot has shut down")
    logging.info(generate_emoji(6))


set_basic_logging()
main()
