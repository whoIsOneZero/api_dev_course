from fastapi import status, HTTPException, Depends, APIRouter
from database import utils
from models import models
from schemas import schemas
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database.db import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user in the database.

    Args:
        user (schemas.UserCreate): The user data for creation.
        db (Session): The database session.

    Returns:
        models.User: The newly created user.

    Raises:
        HTTPException: If the email already exists in the database.
    """

    # hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(
        **user.model_dump())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        # rollback the transaction
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already taken.")

    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a user by their ID.

    Args:
        id (int): The unique identifier of the user.
        db (Session): The database session dependency.

    Returns:
        schemas.UserResponse: The user data if found.

    Raises:
        HTTPException: If the user with the specified ID does not exist.
            - Status Code: 404
            - Detail: "user with id: {id} does not exist"
    """
    
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    return user
