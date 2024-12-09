from datetime import time
import psycopg
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg.rows import dict_row
from config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{
    settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg.connect(dbname='social_media_fastapi', user='postgres',
#                                host='localhost', password='password1', row_factory=dict_row)
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print(f"Error: {error}")
#         time.sleep(2)
