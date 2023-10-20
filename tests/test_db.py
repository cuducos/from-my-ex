from datetime import datetime, timedelta
from unittest.mock import Mock

from from_my_ex.db import LastRepost, db


def test_last_repost():
    db.create_tables((LastRepost,))

    old_post, post, new_post = Mock(), Mock(), Mock()
    post.utc = datetime.utcnow()
    new_post.utc = post.utc + timedelta(days=1)
    old_post.utc = post.utc - timedelta(days=1)

    LastRepost.save_last_repost(post)
    assert LastRepost.should_repost(new_post)
    assert not LastRepost.should_repost(old_post)
