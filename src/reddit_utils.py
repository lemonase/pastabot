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


def get_submission_from_url(
    reddit_client: praw.models.reddit, url: str
) -> praw.models.reddit.submission:
    """Gets the submission ID from a reddit URL"""
    # Split by /'s, find comments, find id, get submission
    url_arr = url.split("/")
    submission_id = url_arr[url_arr.index("comments") + 1]

    return reddit_client.submission(submission_id)
