from fastapi import APIRouter,FastAPI,Depends,HTTPException,status,Query

from sqlalchemy import Column, Integer, String
from typing import List
from sqlalchemy.orm import Session, declarative_base
from app.database import get_db
from app.models import *
from app.schemas import *
from app.auth import *

router = APIRouter(prefix="/transactions", tags=["transactions"])



@router.get("/", response_model=PaginatedTransactions, status_code=status.HTTP_200_OK)
def get_transactions(
    type: Optional[str] = None,
    category: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    page: int = 1,
    page_size: int = Query(20, le=100),
    db: Session = Depends(get_db),
    cur_user=Depends(get_current_user)
):
    query = db.query(Transaction).filter(Transaction.user_id==cur_user.id)
    if type:
        query = query.filter(Transaction.type == type.lower())
    if category:
        query = query.filter(Transaction.category == category)
    if date_from:
        query = query.filter(Transaction.created_at >= date_from)
    if date_to:
        query = query.filter(Transaction.created_at <= date_to)
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)

    total = query.count()
    results = query.offset((page - 1) * page_size).limit(page_size).all()

    return PaginatedTransactions(total=total, page=page, page_size=page_size, results=results)

@router.get("/{id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def get_transaction(id: int, db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    query = db.query(Transaction).filter(Transaction.id == id)
    transaction = query.first()
    if not transaction:
        raise HTTPException(404, "Transaction not found")
    return transaction

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction:TransactionCreate,db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    if cur_user.role == UserRole.VIEWER:
        raise HTTPException(status_code=403, detail="Viewers cannot create transactions")
    new_transaction = Transaction(
        user_id=cur_user.id,
        amount=transaction.amount,
        category=transaction.category,
        type=transaction.type.lower(),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),

    )
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction

@router.put("/{id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def update_transaction(id:int,update_transaction:TransactionUpdate,db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    if cur_user.role not in [UserRole.ADMIN,UserRole.ANALYST]:
        raise HTTPException(403, "You are not authorized to perform this action")
    query = db.query(Transaction).filter(Transaction.id == id).first()
    if not query:
        raise HTTPException(404, "Transaction not found")

    update_fields=update_transaction.model_dump(exclude_unset=True)
    if 'type' in update_fields and update_fields['type']:
        update_fields['type'] = update_fields['type'].lower()
        
    for(key, value) in update_fields.items():
        setattr(query, key, value)

    db.commit()
    db.refresh(query)
    return query

@router.delete("/{id}", response_model=TransactionResponse, status_code=status.HTTP_200_OK)
def delete_transaction(id:int,db: Session = Depends(get_db), cur_user=Depends(get_current_user)):
    query = db.query(Transaction).filter(Transaction.id == id)
    transaction = query.first()
    if not transaction:
        raise HTTPException(404, "Transaction not found")
    result = TransactionResponse.model_validate(transaction)
    db.delete(transaction)
    db.commit()
    return result

