from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import db, utils, oauth2
from schemas import schemas
from models import models

router = APIRouter(
    tags=['Authentication']
)


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db.get_db)):
    """
    Authenticate a user and generate an access token.

    Args:
        user_credentials (OAuth2PasswordRequestForm): The form data containing the user's email (as `username`) and password.
        db (Session): The database session dependency.

    Returns:
        dict: A dictionary containing:
            - `access_token` (str): The generated JWT access token.
            - `token_type` (str): The type of token, typically "bearer".

    Raises:
        HTTPException: If authentication fails due to invalid credentials.
            - Status Code: 403
            - Detail: "Invalid credentials"
    """

    # extract `username` (email) and `password` from `OAuth2PasswordRequestForm`.
    user_email = user_credentials.username

    # query the database to find a user with the provided email.
    user = db.query(models.User).filter(
        models.User.email == user_email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    # verify the provided password against the hashed password stored in the database.
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    # if authentication succeeds, generate a JWT token containing the user's ID.
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}
