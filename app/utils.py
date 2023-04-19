from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str) -> CryptContext:
    """ Returns hashed password, given a plain password. """

    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str) -> CryptContext:
    """ Compares a plain password to hashed password. """
    
    return pwd_context.verify(plain_password, hashed_password)