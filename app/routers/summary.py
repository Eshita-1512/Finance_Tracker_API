from fastapi import FastAPI,APIRouter,HTTPException,Depends,status
from sqlalchemy import func, case
from sqlalchemy.orm import Session
from typing import List,Dict
from app.database import get_db
from app.models import *
from app.schemas import *
from app.auth import *
router = APIRouter(prefix="/summary", tags=["summary"])



@router.get("/",response_model=SummaryResponse,status_code=status.HTTP_200_OK)
def overall_summary(
        db:Session=Depends(get_db),
        cur_user=Depends(get_current_user)):
    totals=db.query(
        func.sum(case((Transaction.type==transaction_type.INCOME,Transaction.amount),else_=0)).label("total_income"),
        func.sum(case((Transaction.type==transaction_type.EXPENSES,Transaction.amount),else_=0)).label("total_expense"),
        func.count(Transaction.id).label("total_transactions")
    ).one()
    total_income=totals.total_income or 0
    total_expense=totals.total_expense or 0
    total_transactions=totals.total_transactions
    balance=total_income-total_expense

    rows= db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total_amount"),
        func.count(Transaction.id).label("total_count")
    ).group_by(Transaction.category).all()
    
    category_breakdown = [
        {"category": r.category, "total_amount": r.total_amount, "total_count": r.total_count} for r in rows
    ]

    return SummaryResponse(
        total_income=total_income,
        total_expense=total_expense,
        balance=balance,
        total_transactions=total_transactions,
        category_breakdown=category_breakdown
    )

@router.get("/monthly",response_model=List[SummaryResponse],status_code=status.HTTP_200_OK)
def overall_monthly(year:Optional[int],db:Session=Depends(get_db), cur_user=Depends(get_current_user)):
    if cur_user.role not in [UserRole.ADMIN,UserRole.ANALYST]:
        raise HTTPException(403,"You are not authorized to view this page")
    query=db.query(
        func.date_trunc("month",Transaction.created_at).label("month"),
        func.sum(case((Transaction.type==transaction_type.INCOME,Transaction.amount),else_=0)).label("income"),
        func.sum(case((Transaction.type==transaction_type.EXPENSES,Transaction.amount),else_=0)).label("expense")
    )
    if year:
        query=query.filter(func.extract("year",Transaction.created_at)==year)
    query=query.group_by(func.date_trunc("month",Transaction.created_at)).order_by(func.date_trunc("month",Transaction.created_at))
    rows=query.all()

    list=[]
    for row in rows:
        month_str=row.month.strftime("%Y-%m")
        income=row.income or 0
        expenses=row.expense or 0
        balance=income-expenses
        list.append({
            "month":month_str,
            "income":income,
            "expenses":expenses,
            "balance":balance,
        }
        )

    return list

@router.get("/recent",response_model=List[TransactionResponse],status_code=status.HTTP_200_OK)
def recent(db:Session=Depends(get_db), cur_user=Depends(get_current_user)):
    transaction=(db.query(Transaction).order_by(Transaction.created_at.desc()).limit(10).all())
    return transaction

@router.get("/categories")
def category_breakdown(db=Depends(get_db), cur_user=Depends(get_current_user)):
    if cur_user.role not in [UserRole.ADMIN,UserRole.ANALYST]:
        raise HTTPException(403,"You are not authorized to view this page")
    total = db.query(func.sum(Transaction.amount).label("total")).one()
    rows=(db.query(
        Transaction.category,
        func.sum(Transaction.amount).label("total_amount"),
        func.count(Transaction.id).label("total_count")
    ).group_by(Transaction.category)
    .order_by(func.sum(Transaction.amount).desc())
    .all()
    )


    breakdown: List[Dict] = []
    for row in rows:
        percentage = (row.total_amount / total* 100) if total > 0 else 0
        breakdown.append({
            "category": row.category,
            "total_amount": row.total_amount,
            "count": row.count,
            "percentage": round(percentage, 2)
        })

    return breakdown







