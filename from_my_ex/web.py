from fastapi import FastAPI, HTTPException

from from_my_ex import repost
from from_my_ex.clients.bsky import BlueskyError
from from_my_ex.clients.mastodon import MastodonError

app = FastAPI()


@app.get("/", status_code=204)
def home():
    try:
        repost()
    except (BlueskyError, MastodonError) as err:
        raise HTTPException(status_code=500, detail=str(err))
