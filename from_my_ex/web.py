from fastapi import FastAPI, HTTPException

from from_my_ex import repost
from from_my_ex.clients.errors import ClientError

app = FastAPI()


@app.get("/", status_code=204)
def home():
    try:
        repost()
    except ClientError as err:
        raise HTTPException(status_code=500, detail=str(err))
