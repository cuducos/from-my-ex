from datetime import datetime
from unittest.mock import ANY, patch

from pytest import raises

from from_my_ex import settings
from from_my_ex.clients.mastodon import (
    Mastodon,
    MastodonCredentialsNotFoundError,
    MastodonError,
)
from from_my_ex.posts import Media, Post


def create_post(text):
    return Post(text, datetime.utcnow(), None)


def test_mastodon_client_raises_error_when_not_set():
    with patch.object(settings, "CLIENTS_AVAILABLE", new_callable=set):
        with raises(MastodonCredentialsNotFoundError):
            Mastodon()


def test_mastodon_client_post_raises_error_from_server():
    with patch("from_my_ex.clients.mastodon.post") as mock:
        mock.return_value.status_code = 401
        mock.return_value.json.return_value = {"error": "oops"}
        post = create_post("Hello")
        with raises(MastodonError):
            Mastodon().post(post)


def test_mastodon_client_post():
    with patch("from_my_ex.clients.mastodon.post") as mock:
        mock.return_value.status_code = 200
        mastodon = Mastodon()
        post = create_post("Hello")

        assert mastodon.post(post) is None
        mock.assert_called_once_with(
            f"{settings.MASTODON_INSTANCE}/api/v1/statuses",
            headers={"Authorization": "Bearer 40two"},
            json={"status": post.text},
        )


def test_mastodon_client_upload():
    mastodon = Mastodon()
    media = Media(b"42", "image/png", "desc")

    with patch("from_my_ex.clients.mastodon.post") as mock:
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"id": 42}
        resp = mastodon.upload(media)

        assert resp == 42
        mock.assert_called_once_with(
            f"{settings.MASTODON_INSTANCE}/api/v2/media",
            headers={"Authorization": "Bearer 40two"},
            data={"description": "desc"},
            files={"file": ("image.png", ANY, "image/png")},
        )


def test_mastodon_client_post_with_media():
    with patch.object(Mastodon, "upload") as upload:
        upload.return_value = 42
        with patch("from_my_ex.clients.mastodon.post") as mock:
            mock.return_value.status_code = 200
            mastodon = Mastodon()
            post = create_post("Hello")
            post.media = (Media(b"42", "image/png"),)

            assert mastodon.post(post) is None
            mock.assert_called_once_with(
                f"{settings.MASTODON_INSTANCE}/api/v1/statuses",
                headers={"Authorization": "Bearer 40two"},
                json={"status": post.text, "media_ids": [42]},
            )
