from app.database.database import get_db
from app.database.models import User
from app.libs.utils import hash
from .schemas.schemas import UserCreate, UserResponse

from fastapi import status, APIRouter, HTTPException, Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session


router = APIRouter(prefix="/users", tags=['Users'])


@router.get("/{id}", response_model=UserResponse)
def get_one_user(
    id: int, 
    db: Session = Depends(get_db)
) -> User:
    """ Retrieves a single user from the database, given a user id. """

    user = db.query(User).filter(User.id == id).first()

    # Check if user exists in database.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )
    
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
) -> User:
    """ Adds a new user into the database, given the email and password. """
    
    # Hash password.
    user.password = hash(user.password)

    new_user = User(**user.dict())
    db.add(new_user)

    # Write into database if email is available.
    try:
        db.commit()

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Email is already in use."
        )
    
    db.refresh(new_user)

    return new_user