from os import environ, getenv
from urllib.parse import urlparse


class EnvironmentVariableNotFoundError(Exception):
    pass


try:
    EX_USERNAME = environ["FROM_MY_EX_USERNAME"]
    NITTER_INSTANCE = environ["FROM_MY_EX_NITTER_INSTANCE"]
    DATABASE_URL = environ["FROM_MY_EX_DATABASE_URL"]
except KeyError as err:
    missing_key, *_ = err.args
    raise EnvironmentVariableNotFoundError(missing_key)

NITTER_FEED_URL = f"{NITTER_INSTANCE}/{EX_USERNAME}/rss"
NITTER_DOMAIN = urlparse(NITTER_INSTANCE).netloc

BSKY_AGENT = getenv("FROM_MY_EX_BSKY_AGENT", "https://bsky.social")
BSKY_EMAIL = getenv("FROM_MY_EX_BSKY_EMAIL")
BSKY_PASSWORD = getenv("FROM_MY_EX_BSKY_PASSWORD")

CLIENTS_AVAILABLE = set(
    key for key, value in (("bsky", BSKY_EMAIL and BSKY_PASSWORD),) if value
)
