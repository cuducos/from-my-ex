from logging import ERROR, INFO, Formatter, StreamHandler, getLogger
from sys import argv, stderr, stdout

from from_my_ex import repost
from from_my_ex.clients.errors import ClientError
from from_my_ex.db import LastRepost, db


def logger():
    logger = getLogger(__name__)
    logger.setLevel(INFO)

    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    out = StreamHandler(stream=stdout)
    out.setLevel(INFO)
    out.setFormatter(formatter)
    logger.addHandler(out)

    err = StreamHandler(stream=stderr)
    err.setLevel(ERROR)
    err.setFormatter(formatter)
    logger.addHandler(err)

    return logger


def create_tables():
    with db:
        db.create_tables((LastRepost,))
    exit()


def run():
    if "--create-db" in argv:
        create_tables()
        return

    log = logger()
    try:
        repost()
    except ClientError as err:
        log.error(str(err))


if __name__ == "__main__":
    run()
