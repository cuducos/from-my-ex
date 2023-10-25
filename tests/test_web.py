from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from pytest import mark

from from_my_ex.clients.bsky import BlueskyError
from from_my_ex.clients.mastodon import MastodonError
from from_my_ex.web import app


def test_home_success():
    with patch("from_my_ex.web.repost"):
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 204


@mark.parametrize("cls", (MastodonError, BlueskyError))
def test_home_error(cls):
    with patch("from_my_ex.web.repost") as mock:
        error = Mock()
        error.json.return_value = {
            "error": "Boom!",
            "message": "Here comes the details",
        }
        error.status_code = 42
        mock.side_effect = cls(error)
        client = TestClient(app)

        response = client.get("/")
        assert response.status_code == 500
        assert "Boom!" in response.text
        assert "42" in response.text
