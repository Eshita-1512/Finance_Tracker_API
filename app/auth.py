from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime, timedelta,timezone
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
import os
pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto',
)
SECRET_KEY = os.environ.get("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "dev-only-change-in-production-use-env-file"
ALGORITHM = "HS256"
TOKEN_EXPIRATION_SECONDS = 60 * 60 * 24

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
def create_token(user_id:int,role:str) -> str:
    payload = {
        "sub":str(user_id),
        "role":role.value if hasattr(role, 'value') else str(role),
        "exp":datetime.now(timezone.utc) + timedelta(seconds=TOKEN_EXPIRATION_SECONDS)
    }
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM)
def decode_token(token:str) -> dict:
    return jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user_id = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user