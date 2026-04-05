from datetime import datetime
from typing import Optional,List

from fastapi import APIRouter
from pydantic import BaseModel,ConfigDict
from app.models import UserRole


class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TransactionCreate(BaseModel):
    amount: float
    type:str
    category: str
    date: datetime

class TransactionUpdate(BaseModel):
    amount: Optional[float]
    type: Optional[str]
    category: Optional[str]
    date: Optional[datetime]

class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    amount: float
    type: Optional[str]
    category: Optional[str]

class PaginatedTransactions(BaseModel):
    total: int
    page: int
    page_size: int
    results: List[TransactionUpdate]

class SummaryResponse(BaseModel):
    total_income:float
    total_expense:float
    balance:float
    total_transactions:int
    category_breakdown:List[dict[str,object]]


class RoleUpdate(BaseModel):
    role: UserRole
