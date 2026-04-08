from app.schemas import UserLogin
from fastapi import APIRouter,FastAPI,Depends,HTTPException,status

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, declarative_base
from app.database import get_db
from app.models import *
from app.schemas import *
from app.auth import *


router = APIRouter(prefix="/auth", tags=["auth"])

from sqlalchemy import func

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def register(user:UserRegister,db:Session = Depends(get_db)):
    if (db.query(User).filter(func.lower(User.email) == user.email.lower()).first()):
        raise HTTPException(status_code=409, detail="Email already registered")
    
    hash_pass=hash_password(user.password)
    new_user=User(
        email=user.email.lower(),
        username=user.username,
        hashed_password=hash_pass,
        role=UserRole.viewer
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login",response_model=TokenResponse,status_code=status.HTTP_200_OK)
def login(user:UserLogin,db:Session = Depends(get_db)):
    db_user=db.query(User).filter(func.lower(User.email) == user.email.lower()).first()
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    if not db_user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    
    token=create_token(db_user.id, db_user.role)
    return TokenResponse(access_token=token,user=db_user)




