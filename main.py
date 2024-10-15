from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
    return {"data": "These are your posts"}


@app.post("/create_post")
def create_post(body: dict = Body(...)):
    # print(body)
    return {"new_post": f"title {body['title']} content: {body['content']}"}
