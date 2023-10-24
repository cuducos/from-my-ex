from sys import argv

from from_my_ex.clients.bsky import Bluesky
from from_my_ex.clients.rss import RSS
from from_my_ex.db import LastRepost, db
from from_my_ex.settings import CLIENTS_AVAILABLE


def create_tables():
    with db:
        db.create_tables((LastRepost,))
    exit()


def load_limit():
    if "--limit" not in argv:
        return None

    limit = argv[argv.index("--limit") + 1]
    try:
        return int(limit)
    except ValueError:
        print("Limit must be an integer")
        exit(1)


def load_clients():
    if "bsky" in CLIENTS_AVAILABLE:
        yield Bluesky()


def run():
    if "--create-db" in argv:
        create_tables()
        return

    feed = RSS()
    pending = (post for post in feed.posts if LastRepost.should_repost(post))

    limit, clients = load_limit() or 1, load_clients()
    for count, post in enumerate(pending, 1):
        if count > limit:
            return

        for client in clients:
            client.post(post)

        LastRepost.save_last_repost(post)


if __name__ == "__main__":
    run()
