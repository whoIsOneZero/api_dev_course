from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg.connect(dbname='social_media_fastapi', user='postgres',
                               host='localhost', password='password1', row_factory=dict_row)
        cursor = conn.cursor()
        print("Database connection successful")
        break
    except Exception as error:
        print("Connection to database failed")
        print(f"Error: {error}")
        time.sleep(2)


my_posts = [{"title": "Title of Post 1",
             "content": "Content of Post 1", "id": 4},
            {"title": "Title of Post 2",
            "content": "Content of Post 2", "id": 5}]


def find_post(id: int):
    for p in my_posts:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()

    return {"data": posts}


# default status code
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(new_post: Post):
    post_dict = new_post.model_dump()

    # manually assign ID
    post_dict['id'] = randrange(0, 3000000)

    my_posts.append(post_dict)
    return {"data": post_dict}


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    my_posts.pop(index)

    # Don't send any data back with 204 for FastAPI
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict

    return {"data": post_dict}
