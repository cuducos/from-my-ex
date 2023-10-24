from io import BytesIO

from httpx import post

from from_my_ex import settings


class MastodonCredentialsNotFoundError(Exception):
    pass


class MastodonError(Exception):
    def __init__(self, response, *args, **kwargs):
        data = response.json()
        msg = (
            f"Error from Mastodon instance server - "
            f"[HTTP Status {response.status_code}] {data['error']}"
        )
        super().__init__(msg, *args, **kwargs)


class Mastodon:
    def __init__(self):
        if "mastodon" not in settings.CLIENTS_AVAILABLE:
            raise MastodonCredentialsNotFoundError(
                "FROM_MY_EX_MASTODON_ACCESS_TOKEN environment variables not set"
            )
        self.headers = {"Authorization": f"Bearer {settings.MASTODON_ACCESS_TOKEN}"}

    def req(self, path, **kwargs):
        return post(
            f"{settings.MASTODON_INSTANCE}{path}", headers=self.headers, **kwargs
        )

    def upload(self, media):
        data = {"description": media.alt} if media.alt else None
        ext = media.mime.split("/")[1]

        with BytesIO(media.content) as attachment:
            files = {"file": (f"image.{ext}", attachment, media.mime)}
            resp = self.req("/api/v2/media", data=data, files=files)

        if resp.status_code not in (202, 200):
            raise MastodonError(resp)

        data = resp.json()
        return data["id"]

    def post(self, status):
        data = {"status": status.text}
        if status.media:
            data["media_ids"] = [self.upload(media) for media in status.media]

        resp = self.req("/api/v1/statuses", json=data)
        if resp.status_code != 200:
            raise MastodonError(resp)
