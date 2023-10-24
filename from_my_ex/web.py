from fastapi import FastAPI

from from_my_ex import repost

app = FastAPI()


@app.get("/")
def home():
    repost()
