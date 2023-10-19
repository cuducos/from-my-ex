from unittest.mock import patch

from from_my_ex.clients.rss import RSS
from from_my_ex.settings import NITTER_FEED_URL


def create_post(is_reply=False, is_repost=False):
    summary = "I am a post"
    if is_repost:
        summary = f"RT by @whoever: {summary}"
    if is_reply:
        summary = f"R to @whoever: {summary}"
    return {"summary": summary}


def create_feed(*posts):
    return {"entries": posts or (create_post(),)}


def test_rss_client_calls_feedparser():
    with patch("from_my_ex.clients.rss.parse") as mock:
        feed = create_feed()
        mock.return_value = feed
        rss = RSS()
        mock.assert_called_once_with(NITTER_FEED_URL)
        assert rss.feed == feed


def test_rss_client_skips_replies():
    with patch("from_my_ex.clients.rss.parse") as mock:
        post = create_post()
        reply = create_post(is_reply=True)
        mock.return_value = create_feed(post, reply)
        rss = RSS()
        posts = tuple(rss.posts)
        assert 1 == len(posts)
        assert "reply" not in (post.text for post in posts)


def test_rss_client_skips_reposts():
    with patch("from_my_ex.clients.rss.parse") as mock:
        post = create_post()
        repost = create_post(is_repost=True)
        mock.return_value = create_feed(post, repost)
        rss = RSS()
        posts = tuple(rss.posts)
        assert 1 == len(posts)
        assert "repost" not in (post.text for post in posts)
