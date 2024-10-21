from passlib.context import CryptContext

# Context for hashing passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Returns the hashed password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compares the provided password with the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
