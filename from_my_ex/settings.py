from os import environ
from urllib.parse import urlparse


class EnvironmentVariableNotFoundError(Exception):
    pass


try:
    EX_USERNAME = environ["FROM_MY_EX_USERNAME"]
    NITTER_INSTANCE = environ["FROM_MY_EX_NITTER_INSTANCE"]
except KeyError as err:
    missing_key, *_ = err.args
    raise EnvironmentVariableNotFoundError(missing_key)

NITTER_FEED_URL = f"{NITTER_INSTANCE}/{EX_USERNAME}/rss"
NITTER_DOMAIN = urlparse(NITTER_INSTANCE).netloc
