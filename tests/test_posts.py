from unittest.mock import patch

from from_my_ex.posts import Post


def test_post_from_rss_entry_change_mentions_to_urls():
    summary = '<p>Hello, <a href="https://instan.ce/apyb">@apyb</a>!</p>'
    entry = {"summary": summary}
    post = Post.from_rss_entry(entry)
    assert post.text == "Hello, https://x.com/apyb !"


def test_post_from_rss_entry_cleans_up_hashtag_links():
    summary = '<p>Hello, <a href="https://instan.ce/hashtag/world">#world</a>!</p>'
    entry = {"summary": summary}
    post = Post.from_rss_entry(entry)
    assert post.text == "Hello, #world!"


def test_post_from_rss_entry_uses_links_urls():
    summary = '<p>Hello, <a href="https://not.my.instan.ce/">not.my.instan.ce</a> !</p>'
    entry = {"summary": summary}
    post = Post.from_rss_entry(entry)
    assert post.text == "Hello, https://not.my.instan.ce/ !"


def test_post_from_rss_entry_get_image_bytes():
    summary = '<p>Hello <img src="https://instan.ce/image.jpg" /></p>'
    entry = {"summary": summary}
    with patch("from_my_ex.posts.get") as mock:
        mock.return_value.content = b"42"
        post = Post.from_rss_entry(entry)
        mock.assert_called_once_with("https://instan.ce/image.jpg")
    assert post.media == (b"42",)
