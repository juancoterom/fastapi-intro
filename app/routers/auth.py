from app.database.models import User
from app.database.database import get_db
from app.libs.oauth2 import create_access_token
from app.libs.utils import verify
from .schemas.schemas import TokenResponse

from fastapi import status, HTTPException, APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router = APIRouter(prefix="/login", tags=['Authentication'])


@router.post("/", response_model=TokenResponse)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
    ) -> dict[str, str]:
    """ Verifies user email and password during login, returns token. """

    user = db.query(User).filter(User.email == user_credentials.username).first()

    # Check if email exists in database or if given password matches hashed password.
    if not user or not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Invalid credentials."
            )
    
    access_token = create_access_token(data={"user_id": user.id})

    return {
        "access_token": access_token, 
        "token_type": "bearer"
        }