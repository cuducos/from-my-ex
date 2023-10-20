from peewee import DateTimeField, Model, PostgresqlDatabase, SqliteDatabase

from from_my_ex.settings import DATABASE_URL

if DATABASE_URL.startswith("postgres"):
    Database = PostgresqlDatabase
else:
    Database = SqliteDatabase


db = Database(DATABASE_URL)


class LastRepost(Model):
    at = DateTimeField()

    class Meta:
        database = db

    @classmethod
    def should_repost(cls, post):
        last = cls.select().first()
        if not last:
            return True

        return post.utc > last.at

    @classmethod
    def save_last_repost(cls, post):
        last = cls.select().first()
        if not last:
            last = cls(at=post.utc)
        else:
            last.at = post.utc
        last.save()
