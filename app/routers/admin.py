from fastapi import APIRouter, Depends, HTTPException, status, FastAPI
from app.models import *
from app.database import *
from app.schemas import *
from app.auth import *
from typing import List

router=APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    if cur_user.role != UserRole.ADMIN:
        raise HTTPException(403,"You are not allowed to perform this action")

    rows = db.query(User).all()
    return rows

@router.put("/users/{id}/role", response_model=UserResponse)
def change_role( id: int, role:RoleUpdate,db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    if cur_user.role != UserRole.ADMIN:
        raise HTTPException(403,"You are not allowed to perform this action")
    user=db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(404,"User not found")
    if user.role == UserRole.ADMIN:
        raise HTTPException(403,"You are not allowed to perform this action")
    user.role = role.role
    db.commit()
    db.refresh(user)
    return user