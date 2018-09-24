from src.classes.db import db


class Tweet:
    def __init__(self, tweet_id):
        self.tweet_id = tweet_id

    def exists(self):
        return db.get_cursor().execute(
            "SELECT * FROM tweets WHERE id=?", (self.tweet_id,)
        ).fetchone() is not None

    def create(self):
        if not self.exists():
            db.get_cursor().execute("INSERT INTO tweets VALUES (?)", (self.tweet_id,))
            db.commit()


