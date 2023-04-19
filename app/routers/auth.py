from .. import models, schemas, utils, oauth2
from ..database import get_db
from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(prefix="/login", tags=['Authentication'])


@router.post("/", response_model=schemas.TokenResponse)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
    ) -> dict[str, str]:
    """ Verifies user email and password during login, returns token. """

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # Check if email exists in database.
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid credentials."
            )
    
    # Check if given password matches hashed password in database.
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials."
        )
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token, 
        "token_type": "bearer"
        }