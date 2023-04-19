from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    """ Returns hashed password, given a plain password. """

    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    """ Compares a plain password to hashed password. """
    
    return pwd_context.verify(plain_password, hashed_password)