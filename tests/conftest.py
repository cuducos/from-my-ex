from os import environ

SETTINGS = {
    "USERNAME": "bird",
    "NITTER_INSTANCE": "https://instan.ce",
    "BSKY_EMAIL": "python@mailinator.com",
    "BSKY_PASSWORD": "fourty2",
}


def pytest_configure(config):
    for key, value in SETTINGS.items():
        environ[f"FROM_MY_EX_{key}"] = value
    return config
