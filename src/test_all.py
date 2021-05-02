import os

import praw
import pytest
from dotenv import load_dotenv

import bot
import reddit_utils


@pytest.fixture
def test_reddit_client():
    load_dotenv()

    assert (
        os.environ.get("REDDIT_ID") is not None
    ), "must have REDDIT_ID environment variable set"
    assert (
        os.environ.get("REDDIT_SECRET") is not None
    ), "must have REDDIT_SECRET environment variable set"

    client = praw.Reddit(
        client_id=os.environ.get("REDDIT_ID"),
        client_secret=os.environ.get("REDDIT_SECRET"),
        user_agent=bot.UA_STRING,
        check_for_async=False,
    )
    return client


def test_subreddits(test_reddit_client):
    test_subreddits = test_reddit_client.subreddit(bot.DEFAULT_SUBS)

    hot_posts = reddit_utils.get_posts(test_subreddits, "hot", 10)
    top_posts = reddit_utils.get_posts(test_subreddits, "top", 10)
    new_posts = reddit_utils.get_posts(test_subreddits, "new", 10)

    for p in hot_posts:
        pass
    for p in top_posts:
        pass
    for p in new_posts:
        pass

    return test_subreddits


def test_submission_url(test_reddit_client):
    url1 = "https://www.reddit.com/r/copypasta/comments/n345c9/anyone_else_kill_people_in_skyrimfallout_undress/"
    url2 = "https://www.reddit.com/r/copypasta/comments/n3941g/ascii_penis_collection/?utm_source=share&utm_medium=web2x&context=3"
    url3 = "https://www.reddit.com/r/copypasta/comments/n37jyj/dolphin_pussy_jelly/"

    assert (
        reddit_utils.get_submission_from_url(test_reddit_client, url1) == "n345c9"
    ), "incorrect submission id"
    assert (
        reddit_utils.get_submission_from_url(test_reddit_client, url2) == "n3941g"
    ), "incorrect submission id"
    assert (
        reddit_utils.get_submission_from_url(test_reddit_client, url3) == "n37jyj"
    ), "incorrect submission id"
