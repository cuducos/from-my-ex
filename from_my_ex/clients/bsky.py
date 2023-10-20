from datetime import datetime

from httpx import post

from from_my_ex import settings


class BlueskyCredentialsNotFoundError(Exception):
    pass


class BlueskyError(Exception):
    def __init__(self, response, *args, **kwargs):
        data = response.json()
        msg = (
            f"Error from Bluesky agent/instance - "
            f"[HTTP Status {response.status_code}] "
            f"{data['error']}: {data['message']}"
        )
        super().__init__(msg, *args, **kwargs)


class InvalidBlueskyCredentialsError(BlueskyError):
    pass


class BlueskyPostError(BlueskyError):
    pass


class Bluesky:
    def __init__(self):
        if "bsky" not in settings.CLIENTS_AVAILABLE:
            raise BlueskyCredentialsNotFoundError(
                "FROM_MY_EX_BSKY_EMAIL and/or FROM_MY_EX_BSKY_PASSWORD "
                "environment variables not set"
            )

        credentials = {
            "identifier": settings.BSKY_EMAIL,
            "password": settings.BSKY_PASSWORD,
        }
        resp = post(
            f"{settings.BSKY_AGENT}/xrpc/com.atproto.server.createSession",
            json=credentials,
        )

        if resp.status_code == 401:
            raise InvalidBlueskyCredentialsError(resp)

        resp.raise_for_status()
        data = resp.json()
        self.token, self.did = data["accessJwt"], data["did"]

    def post(self, text, media=None):
        if media:
            raise NotImplementedError("Uploading media not implemented yet.")

        data = {
            "repo": self.did,
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "text": text,
                "createdAt": datetime.utcnow().isoformat(),
            },
        }
        resp = post(
            f"{settings.BSKY_AGENT}/xrpc/com.atproto.repo.createRecord",
            headers={"Authorization": f"Bearer {self.token}"},
            json=data,
        )
        if resp.status_code != 200:
            raise BlueskyPostError(resp)
