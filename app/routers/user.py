from .. import models, schemas, utils
from ..database import get_db
from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError


router = APIRouter()


@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_one_user(id: int, db: Session = Depends(get_db)):
    """ Retrieves a single user from the database, given a user id. """

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
            )
    
    return user


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """ Adds a new user into the database, given the email and password. """
    
    # Hash password.
    user.password = utils.hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)

    # Check if email is available.
    try:
        db.commit()

    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_200_OK,
            detail="Email is already in use."
            )
    
    db.refresh(new_user)
    return new_user