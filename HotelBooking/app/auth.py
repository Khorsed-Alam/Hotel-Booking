from passlib.context import CryptContext
from app import models

from datetime import datetime, timedelta

SECRET_KEY = "SECRET123"
ALGORITHM = "HS256"

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password):
    return pwd.hash(password)

def verify_password(password, hashed):
    return pwd.verify(password, hashed)

def create_token(data: dict):
    data["exp"] = datetime.utcnow() + timedelta(hours=3)
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
