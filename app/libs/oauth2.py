from app.database.config import settings
from app.database.database import get_db
from app.database.models import User
from app.routers.schemas.schemas import TokenData

from datetime import datetime, timedelta
from fastapi import status, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict) -> str:
    """ Creates access token, given a piece of data. """

    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception) -> TokenData:
    """ Decodes and verifies a given token, returns token data. """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(
    token: TokenData = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """ Returns current user, given a token. """
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    token = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token.id).first()

    return user