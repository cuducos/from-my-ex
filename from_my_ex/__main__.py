from from_my_ex.clients import RSS

if __name__ == "__main__":
    feed = RSS()
    for post in feed.posts:
        print(post.text)
