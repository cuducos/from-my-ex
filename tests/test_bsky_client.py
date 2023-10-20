from unittest.mock import patch

from pytest import raises

from from_my_ex import settings
from from_my_ex.clients.bsky import (
    Bluesky,
    BlueskyCredentialsNotFoundError,
    BlueskyPostError,
    InvalidBlueskyCredentialsError,
)


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
        with raises(InvalidBlueskyCredentialsError):
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
        with raises(BlueskyPostError):
            bsky.post("Hello")
