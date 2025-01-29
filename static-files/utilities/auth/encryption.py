from bcrypt import hashpw, gensalt, checkpw
from passlib.context import CryptContext
from ...config.manager import settings
import jwt

SECRET_KEY = settings.JWT_SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def gen_hash(text: str) -> str:
    return pwd_context.hash(text).encode('utf-8')


def check_hash(text: str, hashed_text: str) -> bool:
    return pwd_context.verify(text, hashed_text)


def gen_apiKey_jwt() -> str:
    '''
    Returns a jwt as an apiKey
    '''
    return jwt.encode({"type": "apiKey"}, SECRET_KEY, ALGORITHM)