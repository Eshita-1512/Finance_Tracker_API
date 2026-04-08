from datetime import datetime,timezone
import enum
from sqlalchemy.orm import relationship
from sqlmodel import Field,Column, Integer, String, Boolean, DateTime, ForeignKey,Numeric,Enum
from app.database import base

class UserRole(str, enum.Enum):
    admin = "admin"
    analyst = "analyst"
    viewer = "viewer"

class transaction_type(str, enum.Enum):
    income = "income"
    expense = "expense"


class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole, name='user_roles_enum'), default=UserRole.viewer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))

    transactions = relationship('Transaction', back_populates='user')


class Transaction(base):
    __tablename__ = 'transaction'
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey('user.id'))
    amount=Column(Numeric(12,2))
    type=Column(Enum(transaction_type, name='transaction_type_enum'), default=transaction_type.income)
    category=Column(String)
    notes=Column(String,default=None)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=Column(DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))
    user=relationship('User', back_populates='transactions')