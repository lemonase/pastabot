async def send_post_as_msg(ctx, posts, post_limit):
    """Takes discord context, reddit posts and number of posts
    and uses the discord discord context to send the post as a discord message
    """
    for i, post in enumerate(posts):
        if i == post_limit - 1:
            await ctx.send(post.title + "\n")
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
