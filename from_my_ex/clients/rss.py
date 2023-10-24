from feedparser import parse

from from_my_ex.posts import Post
from from_my_ex.settings import NITTER_FEED_URL


class RSS:
    def __init__(self):
        self.feed = parse(NITTER_FEED_URL)

    @property
    def posts(self):
        for entry in reversed(self.feed["entries"]):
            post = Post.from_rss_entry(entry)
            if not post.is_repost() and not post.is_reply():
                yield post
