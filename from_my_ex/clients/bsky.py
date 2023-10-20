from datetime import datetime
from re import compile

from httpx import post

from from_my_ex import settings

URL = compile(
    r"(http(s?):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-]))"
)


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

    def data(self, text):
        data = {
            "repo": self.did,
            "collection": "app.bsky.feed.post",
            "record": {
                "$type": "app.bsky.feed.post",
                "text": text,
                "createdAt": datetime.utcnow().isoformat(),
            },
        }

        if matches := URL.findall(text):
            data["record"]["facets"] = []
            start = 0
            source = text.encode()
            for url, *_ in matches:
                target = url.encode()
                start = source.find(target, start)
                end = start + len(target)
                data["record"]["facets"].append(
                    {
                        "index": {"byteStart": start, "byteEnd": end},
                        "features": [
                            {
                                "$type": "app.bsky.richtext.facet#link",
                                "uri": url,
                            }
                        ],
                    }
                )
                start = end

        return data

    def post(self, text, media=None):
        if media:
            raise NotImplementedError("Uploading media not implemented yet.")

        resp = post(
            f"{settings.BSKY_AGENT}/xrpc/com.atproto.repo.createRecord",
            headers={"Authorization": f"Bearer {self.token}"},
            json=self.data(text),
        )
        if resp.status_code != 200:
            raise BlueskyPostError(resp)
