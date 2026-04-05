from app.database import Session
from app.models import User, Transaction, UserRole, transaction_type
from app.auth import hash_password
from datetime import datetime, timedelta, timezone

db = Session()

try:
    print("Seeding database")
    admin_pw = hash_password("admin123")
    analyst_pw = hash_password("analyst123")
    viewer_pw = hash_password("viewer123")

    users = [
        User(username="admin_user", email="admin@test.com", hashed_password=admin_pw, role=UserRole.ADMIN),
        User(username="analyst_user", email="analyst@test.com", hashed_password=analyst_pw, role=UserRole.ANALYST),
        User(username="viewer_user", email="viewer@test.com", hashed_password=viewer_pw, role=UserRole.VIEWER),
    ]

    existing_admin = db.query(User).filter(User.email == "admin@test.com").first()
    if not existing_admin:
        db.add_all(users)
        db.commit()

    admin = db.query(User).filter(User.role == UserRole.ADMIN).first()

    now = datetime.now(timezone.utc)
    
    transactions = [
        Transaction(user_id=admin.id, amount=50000, type=transaction_type.INCOME, category="salary", created_at=now - timedelta(days=40), notes="Previous Salary"),
        Transaction(user_id=admin.id, amount=12000, type=transaction_type.EXPENSES, category="rent", created_at=now - timedelta(days=35), notes="Rent"),
        Transaction(user_id=admin.id, amount=1500, type=transaction_type.EXPENSES, category="groceries", created_at=now - timedelta(days=30), notes="Groceries"),
        Transaction(user_id=admin.id, amount=3000, type=transaction_type.EXPENSES, category="travel", created_at=now - timedelta(days=28), notes="Train ticket"),
        Transaction(user_id=admin.id, amount=50000, type=transaction_type.INCOME, category="salary", created_at=now - timedelta(days=10), notes="Salary"),
        Transaction(user_id=admin.id, amount=800, type=transaction_type.EXPENSES, category="utilities", created_at=now - timedelta(days=9), notes="Internet"),
        Transaction(user_id=admin.id, amount=12000, type=transaction_type.EXPENSES, category="rent", created_at=now - timedelta(days=8), notes="Rent"),
        Transaction(user_id=admin.id, amount=2000, type=transaction_type.EXPENSES, category="food", created_at=now - timedelta(days=5), notes="Dining out"),
        Transaction(user_id=admin.id, amount=120, type=transaction_type.EXPENSES, category="subscriptions", created_at=now - timedelta(days=2), notes="Netflix"),
        Transaction(user_id=admin.id, amount=450, type=transaction_type.EXPENSES, category="food", created_at=now - timedelta(days=1), notes="Coffee"),
        Transaction(user_id=admin.id, amount=25000, type=transaction_type.INCOME, category="freelance", created_at=now - timedelta(days=45), notes="Client project"),
        Transaction(user_id=admin.id, amount=3000, type=transaction_type.EXPENSES, category="shopping", created_at=now - timedelta(days=42), notes="Clothes"),
        Transaction(user_id=admin.id, amount=150, type=transaction_type.EXPENSES, category="utilities", created_at=now - timedelta(days=22), notes="Water bill"),
        Transaction(user_id=admin.id, amount=900, type=transaction_type.EXPENSES, category="health", created_at=now - timedelta(days=15), notes="Pharmacy"),
        Transaction(user_id=admin.id, amount=400, type=transaction_type.EXPENSES, category="entertainment", created_at=now - timedelta(days=12), notes="Movies"),
    ]

    has_txs = db.query(Transaction).filter(Transaction.user_id == admin.id).first()
    if not has_txs:
        db.add_all(transactions)
        db.commit()

    print("Seeded successfully!")
except Exception as e:
    print(f"Error seeding: {e}")
finally:
    db.close()
