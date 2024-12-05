from fastapi import FastAPI
import psycopg
from psycopg.rows import dict_row
import time
from models import models
from database.db import engine
from routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
