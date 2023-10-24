from datetime import datetime
from unittest.mock import patch

from from_my_ex.posts import Media, Post


def create_post(text):
    return {"summary": text, "published": "Tue, 25 Jul 2023 01:27:48 GMT"}


def test_post_from_rss_entry_change_mentions_to_urls():
    entry = create_post('<p>Hello, <a href="https://instan.ce/apyb">@apyb</a>!</p>')
    post = Post.from_rss_entry(entry)
    assert post.text == "Hello, https://x.com/apyb !"


def test_post_from_rss_entry_cleans_up_hashtag_links():
    entry = create_post(
        '<p>Hello, <a href="https://instan.ce/hashtag/world">#world</a>!</p>'
    )
    post = Post.from_rss_entry(entry)
    assert post.text == "Hello, #world!"


def test_post_from_rss_entry_uses_links_urls():
    entry = create_post(
        '<p>Hello, <a href="https://not.my.instan.ce/">not.my.instan.ce</a> !</p>'
    )
    post = Post.from_rss_entry(entry)
    assert post.text == "Hello, https://not.my.instan.ce/ !"


def test_post_from_rss_entry_get_image_bytes():
    entry = create_post('<p>Hello <img src="https://instan.ce/image.jpg" /></p>')
    with patch("from_my_ex.posts.get") as mock:
        mock.return_value.content = b"42"
        mock.return_value.headers = {"content-type": "image/png"}
        post = Post.from_rss_entry(entry)
        mock.assert_called_once_with("https://instan.ce/image.jpg")
    assert post.media == (Media(b"42", "image/png"),)


def test_post_from_rss_entry_parses_timestamp():
    entry = create_post('Hello <img src="https://instan.ce/image.jpg" /></p>')
    with patch("from_my_ex.posts.get"):
        post = Post.from_rss_entry(entry)
    assert post.utc == datetime(2023, 7, 25, 1, 27, 48)
