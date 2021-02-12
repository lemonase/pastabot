import asyncpraw
import asyncio


def get_reddit_client():
    """ Returns a async praw object that represents one (or multiple) subreddits """
    reddit_client = asyncpraw.Reddit(
        client_id="ZAtjAOvaQFdmrQ",
        client_secret="uT6VYKNXUjFwS2ll58ITk1aHJREtbA",
        user_agent="Reddit Bot 0.0.1",
    )
    return reddit_client


def get_subreddit_client(client, sub):
    return client.subreddit(sub, fetch=True)


async def main():
    reddit = get_reddit_client()
    subreddit = await get_subreddit_client(reddit, "copypasta")
    async for post in subreddit.hot(limit=10):
        print(post.title)
        print("-"*10)
        print(post.selftext)

    await reddit.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    # asyncio.run(main())
