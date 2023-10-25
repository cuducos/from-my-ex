from unittest.mock import patch

from fastapi.testclient import TestClient

from from_my_ex.clients.errors import ClientError
from from_my_ex.web import app


def test_home_success():
    with patch("from_my_ex.web.repost"):
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 204


def test_home_error():
    with patch("from_my_ex.web.repost") as mock:
        mock.side_effect = ClientError("Ooops!")
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 500
        assert "Ooops!" in response.text
