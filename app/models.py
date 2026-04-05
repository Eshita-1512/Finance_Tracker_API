from datetime import datetime,timezone
import enum
from sqlalchemy.orm import relationship
from sqlmodel import Field,Column, Integer, String, Boolean, DateTime, ForeignKey,Numeric,Enum
from app.database import base

class UserRole(enum.Enum):
    ADMIN = "admin"
    ANALYST = "analyst"
    VIEWER = "viewer"

class transaction_type(enum.Enum):
    INCOME = "income"
    EXPENSES = "expense"


class User(base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(Enum(UserRole, name='user_roles_enum', values_callable=lambda obj: [e.value for e in obj]), default=UserRole.VIEWER)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda:datetime.now(timezone.utc))

    transactions = relationship('Transaction', back_populates='user')


class Transaction(base):
    __tablename__ = 'transaction'
    id=Column(Integer, primary_key=True, index=True)
    user_id=Column(Integer, ForeignKey('user.id'))
    amount=Column(Numeric(12,2))
    type=Column(Enum(transaction_type,name='transaction_type_enum', values_callable=lambda obj: [e.value for e in obj]), default=transaction_type.INCOME)
    category=Column(String)
    notes=Column(String,default=None)
    created_at=Column(DateTime,default=lambda:datetime.now(timezone.utc))
    updated_at=Column(DateTime,default=lambda:datetime.now(timezone.utc),onupdate=lambda:datetime.now(timezone.utc))
    user=relationship('User', back_populates='transactions')