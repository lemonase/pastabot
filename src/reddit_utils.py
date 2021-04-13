""" Reddit utils

Currently the script only fetches submissions, but later on we can think about
adding comments and other reddit features
"""
import random

import praw
import logger


def get_posts(
    sub: praw.models.reddit.subreddit.Subreddit, sort_type: str, num: int = 100
) -> praw.models.listing.generator.ListingGenerator:
    """Takes a praw subreddit model, sort type, and a limit for num of posts retrieved
    The returned object is a generator, so posts are not really "fetched" until iterated on
    """
    posts = []
    if sort_type == "random":
        sort_type = random.choice(["hot", "top", "new"])

    if sort_type == "top":
        posts = sub.top(limit=num)
    if sort_type == "new":
        posts = sub.new(limit=num)
    else:
        posts = sub.hot(limit=num)

    logger.logging.info("Getting %s posts sorted by: %s", num, sort_type)

    return posts
