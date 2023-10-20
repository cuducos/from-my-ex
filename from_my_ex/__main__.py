from sys import argv

from from_my_ex.clients.rss import RSS
from from_my_ex.db import LastRepost, db

if "--create-db" in argv:
    with db:
        db.create_tables((LastRepost,))
    exit()

feed = RSS()
for post in feed.posts:
    print(post.text)
