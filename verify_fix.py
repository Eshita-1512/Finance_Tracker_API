
from app.models import User, UserRole, transaction_type
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import base

# Test in-memory sqlite to verify the model and enum behavior
engine = create_engine("sqlite:///:memory:")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base.metadata.create_all(bind=engine)

def test_user_creation():
    db = SessionLocal()
    try:
        new_user = User(
            username="testuser",
            email="test@example.com",
            hashed_password="hash",
            role=UserRole.viewer
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"Role value: {new_user.role.value}")
        print(f"Role string: {str(new_user.role)}")
        assert new_user.role == "viewer"
        
        new_transaction = UserRole.admin
        print(f"Admin enum: {new_transaction}")
        print(f"Admin value: {new_transaction.value}")
        assert new_transaction == "admin"

        
        print("Model verification successful!")
    except Exception as e:
        import traceback
        print(f"Model verification failed: {type(e).__name__}: {e}")
        traceback.print_exc()

    finally:
        db.close()

if __name__ == "__main__":
    test_user_creation()
