from dataclasses import dataclass
from datetime import datetime
from re import compile
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from httpx import get

from from_my_ex.settings import NITTER_DOMAIN

DATE_FORMAT = "%a, %d %b %Y %H:%M:%S %Z"
ACCOUNT_HANDLER = compile(r"^@[A-Za-z0-9_]{4,15}$")


def back_to_ex(url):
    if not url:
        return url

    parsed = urlparse(url)
    if parsed.netloc != NITTER_DOMAIN:
        return url

    parsed = parsed._replace(netloc="x.com")
    return parsed.geturl()


@dataclass
class Media:
    content: bytes
    mime: str
    alt: str = ""

    @classmethod
    def from_img_tag(cls, img):
        resp = get(img["src"])
        return cls(resp.content, resp.headers.get("content-type"), img.get("alt", ""))


class Post:
    def __init__(self, text, utc, media):
        self.text = text
        self.utc = utc
        self.media = media

    @classmethod
    def from_rss_entry(cls, entry):
        nodes = BeautifulSoup(entry["summary"], "html.parser")

        for tag in nodes.find_all("a"):
            tag["href"] = back_to_ex(tag.get("href", ""))
            if ACCOUNT_HANDLER.match(tag.text):
                tag.replace_with(f"{tag['href']} ")
            elif tag.text.startswith("#"):
                tag.replace_with(tag.text)
            else:
                tag.replace_with(tag["href"])

        media = []
        for img in nodes.find_all("img"):
            media.append(Media.from_img_tag(img))
            img.decompose()

        published = datetime.strptime(entry["published"], DATE_FORMAT)
        return cls(nodes.text, published, media=tuple(media))

    def is_repost(self):
        return self.text.startswith("RT by @")

    def is_reply(self):
        return self.text.startswith("R to @")
