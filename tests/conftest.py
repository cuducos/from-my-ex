from os import environ


def pytest_configure(config):
    environ["FROM_MY_EX_USERNAME"] = "bird"
    environ["FROM_MY_EX_NITTER_INSTANCE"] = "https://instan.ce"
    return config
