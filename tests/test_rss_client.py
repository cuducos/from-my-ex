from datetime import datetime, timedelta
from unittest.mock import patch

from pytz import utc

from from_my_ex.clients.rss import RSS
from from_my_ex.posts import DATE_FORMAT
from from_my_ex.settings import NITTER_FEED_URL


def create_post(is_reply=False, is_repost=False, published=None):
    published = published or datetime.utcnow().replace(tzinfo=utc)
    summary = "I am a post"
    if is_repost:
        summary = f"RT by @whoever: {summary}"
    if is_reply:
        summary = f"R to @whoever: {summary}"

    return {"summary": summary, "published": published.strftime(DATE_FORMAT)}


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


def test_rss_client_feed_puts_older_posts_first():
    with patch("from_my_ex.clients.rss.parse") as mock:
        yesterday = datetime.utcnow().replace(tzinfo=utc) - timedelta(days=1)
        old_post = create_post(published=yesterday)
        new_post = create_post()
        mock.return_value = create_feed(new_post, old_post)
        rss = RSS()
        first, second = rss.posts
        assert first.utc < second.utc
