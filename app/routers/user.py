from .. import models, schemas, utils
from ..database import get_db
from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter(prefix="/users", tags=['Users'])


@router.get("/{id}", response_model=schemas.UserResponse)
def get_one_user(
    id: int, 
    db: Session = Depends(get_db)
    ) -> models.User:
    """ Retrieves a single user from the database, given a user id. """

    user = db.query(models.User).filter(models.User.id == id).first()

    # Check if user exists in database.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
            )
    
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db)
    ) -> models.User:
    """ Adds a new user into the database, given the email and password. """
    
    # Hash password.
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
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