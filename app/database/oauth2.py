from jose import JWTError, jwt
from datetime import datetime, timedelta

# openssl rand -hex 32
SECRET_KEY = "a78680504dddf2067a04e4b631fd64d15b341165ef4ab593912f5022e382226d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
