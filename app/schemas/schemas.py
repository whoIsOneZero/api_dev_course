from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Union
from pydantic.types import conint


class PostBase(BaseModel):
    """
    Represents the base schema for a post, containing common fields
    used in both creation and response models.

    Attributes:
        title (str): The title of the post.
        content (str): The content of the post.
        published (bool): Indicates if the post is published. Defaults to True.
    """
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    """
    Schema for creating a new post. Inherits all fields from PostBase.
    """
    pass


class UserResponse(BaseModel):
    """
    Schema for user response, including metadata - ID and creation time.

    Attributes:
        id (int): The unique identifier for the user.
        email (EmailStr): The user's email address.
        created_at (datetime): The timestamp when the user was created.
    """

    id: int
    email: EmailStr
    created_at: datetime


# response
class Post(PostBase):
    """
    Schema for a post response, including additional metadata - ID and creation time.

    Attributes:
        id (int): The unique identifier for the post.
        created_at (datetime): The timestamp when the post was created.
        owner_id (int): ID of the creator of the post
    """

    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        """
        Configuration for enabling attribute-based ORM mode, which allows
        compatibility with database models.
        """

        from_attributes = True


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        email (EmailStr): The user's email address, validated for correct format.
        password (str): The user's password.
    """

    email: EmailStr
    password: str

    class Config:
        """
        Configuration for enabling attribute-based ORM mode, which allows
        compatibility with database models.
        """
        from_attributes = True


class UserLogin(BaseModel):
    """
    Schema for user login requests.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """

    email: EmailStr
    password: str


class Token(BaseModel):
    """
    Schema for authentication tokens.

    Attributes:
        access_token (str): The token used to authenticate requests.
        token_type (str): The type of token (e.g., "Bearer").
    """

    access_token: str
    token_type: str


class TokenData(BaseModel):
    """
    Schema for token data extracted from authentication tokens.

    Attributes:
        id (Optional[Union[str, int]]): The user's ID, which can be a string or an integer.
    """

    # handle as integer and string
    id: Optional[Union[str, int]] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)
