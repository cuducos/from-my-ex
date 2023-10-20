from unittest.mock import patch

from pytest import raises

from from_my_ex import settings
from from_my_ex.clients.bsky import (
    Bluesky,
    BlueskyCredentialsNotFoundError,
    BlueskyError,
)
from from_my_ex.posts import Media


def test_bsky_client_raises_error_when_not_set():
    with patch.object(settings, "CLIENTS_AVAILABLE", new_callable=set):
        with raises(BlueskyCredentialsNotFoundError):
            Bluesky()


def test_bsky_client_uses_the_correct_credentials():
    with patch("from_my_ex.clients.bsky.post") as mock:
        Bluesky()
        mock.assert_called_once_with(
            f"{settings.BSKY_AGENT}/xrpc/com.atproto.server.createSession",
            json={
                "identifier": settings.BSKY_EMAIL,
                "password": settings.BSKY_PASSWORD,
            },
        )


def test_bsky_client_raises_error_for_invalid_credentials():
    with patch("from_my_ex.clients.bsky.post") as mock:
        mock.return_value.status_code = 401
        mock.return_value.json.return_value = {"error": "SomeError", "message": "Oops"}
        with raises(BlueskyError):
            Bluesky()


def test_bsky_client_gets_a_jwt_token_and_did():
    with patch("from_my_ex.clients.bsky.post") as mock:
        mock.return_value.json.return_value = {
            "accessJwt": "a very long string",
            "did": "42",
        }
        bsky = Bluesky()
        assert bsky.token == "a very long string"
        assert bsky.did == "42"


def test_bsky_client_post():
    with patch("from_my_ex.clients.bsky.post"):
        bsky = Bluesky()

    bsky.token = "fourty-two"
    bsky.did = "42"
    with patch("from_my_ex.clients.bsky.post") as mock:
        mock.return_value.status_code = 200
        assert bsky.post("Hello") is None


def test_bsky_client_post_raises_error_from_server():
    with patch("from_my_ex.clients.bsky.post"):
        bsky = Bluesky()

    with patch("from_my_ex.clients.bsky.post") as mock:
        mock.return_value.status_code = 501
        mock.return_value.json.return_value = {"error": "SomeError", "message": "Oops"}
        with raises(BlueskyError):
            bsky.post("Hello")


def test_bsky_client_post_data_includes_urls_in_facets():
    with patch("from_my_ex.clients.bsky.post"):
        bsky = Bluesky()

    text = "✨ example mentioning @atproto.com to share the URL 👨‍❤️‍👨 https://en.wikipedia.org/wiki/CBOR."
    data = bsky.data(text, None)
    assert data["record"]["facets"] == [
        {
            "index": {"byteStart": 74, "byteEnd": 108},
            "features": [
                {
                    "$type": "app.bsky.richtext.facet#link",
                    "uri": "https://en.wikipedia.org/wiki/CBOR",
                }
            ],
        }
    ]


def test_bsky_client_post_data_includes_images_blobs():
    with patch("from_my_ex.clients.bsky.post"):
        bsky = Bluesky()

    bsky.token = "token"
    bsky.did = "did"

    with patch("from_my_ex.clients.bsky.post") as mock:
        mock.return_value.status_code = 200
        mock.return_value.json.return_value = {"blob": "42"}
        data = bsky.data("hi", (Media(b"42", "image/png"),))
        mock.assert_any_call(
            f"{settings.BSKY_AGENT}/xrpc/com.atproto.repo.uploadBlob",
            headers={
                "Authorization": "Bearer token",
                "Content-type": "image/png",
            },
            data=b"42",
        )

    assert data["record"]["embed"] == {
        "$type": "app.bsky.embed.images",
        "images": [{"alt": "", "image": "42"}],
    }
