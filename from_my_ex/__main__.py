from sys import argv

from from_my_ex import repost
from from_my_ex.db import LastRepost, db


def create_tables():
    with db:
        db.create_tables((LastRepost,))
    exit()


def run():
    if "--create-db" in argv:
        create_tables()
        return

    repost()


if __name__ == "__main__":
    run()
