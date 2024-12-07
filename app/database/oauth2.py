from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# openssl rand -hex 32
SECRET_KEY = "a78680504dddf2067a04e4b631fd64d15b341165ef4ab593912f5022e382226d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """
    Generate a JSON Web Token (JWT) for authentication.

    Args:
        data (dict): The payload data to include in the token (e.g., user details).

    Returns:
        str: The encoded JWT as a string.
    """

    # avoid modifying the original string
    to_encode = data.copy()

    # add expiration time to the payload (`"exp"` key).
    expire = datetime.now(datetime.timezone.utc) + \
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # encode payload into a JWT using the secret key and the specified algorithm.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Decode and validate a JWT token.

    Args:
        token (str): The JWT string to be verified.
        credentials_exception (HTTPException): The exception to raise if validation fails.

    Returns:
        schemas.TokenData: An object containing the user ID extracted from the token.

    Raises:
        HTTPException: If the token is invalid or the user ID is not found in the payload.
    """

    try:
        # decode the JWT using the secret key and algorithm.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # extract `user_id` from the payload.
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    # returns the user id
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Retrieve the current authenticated user based on the provided JWT.

    Args:
        token (str): The JWT string provided via the Authorization header.

    Returns:
        schemas.TokenData: The token data containing the user ID.

    Raises:
        HTTPException: If the token is invalid or cannot be verified.
    """

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)
