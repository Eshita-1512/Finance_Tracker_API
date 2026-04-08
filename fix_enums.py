"""Fix enum values in PostgreSQL to be lowercase.
Handles the case where enums were created with UPPERCASE member names
but the application now expects lowercase values.
"""
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"))

with engine.connect() as conn:
    # Fix user_roles_enum: rename uppercase to lowercase if they exist
    result = conn.execute(text(
        "SELECT enumlabel FROM pg_enum e JOIN pg_type t ON e.enumtypid = t.oid "
        "WHERE t.typname = 'user_roles_enum' AND e.enumlabel = 'ADMIN'"
    ))
    if result.fetchone():
        print("Found uppercase user_roles_enum values, renaming to lowercase...")
        conn.execute(text("ALTER TYPE user_roles_enum RENAME VALUE 'ADMIN' TO 'admin'"))
        conn.execute(text("ALTER TYPE user_roles_enum RENAME VALUE 'ANALYST' TO 'analyst'"))
        conn.execute(text("ALTER TYPE user_roles_enum RENAME VALUE 'VIEWER' TO 'viewer'"))
        conn.commit()
        print("user_roles_enum fixed.")
    else:
        print("user_roles_enum already has lowercase values.")

    # Fix transaction_type_enum: rename uppercase to lowercase if they exist
    result = conn.execute(text(
        "SELECT enumlabel FROM pg_enum e JOIN pg_type t ON e.enumtypid = t.oid "
        "WHERE t.typname = 'transaction_type_enum' AND e.enumlabel = 'INCOME'"
    ))
    if result.fetchone():
        print("Found uppercase transaction_type_enum values, renaming to lowercase...")
        conn.execute(text("ALTER TYPE transaction_type_enum RENAME VALUE 'INCOME' TO 'income'"))
        # Handle both EXPENSES and EXPENSE
        try:
            conn.execute(text("ALTER TYPE transaction_type_enum RENAME VALUE 'EXPENSES' TO 'expense'"))
        except Exception:
            try:
                conn.execute(text("ALTER TYPE transaction_type_enum RENAME VALUE 'EXPENSE' TO 'expense'"))
            except Exception:
                pass
        conn.commit()
        print("transaction_type_enum fixed.")
    else:
        print("transaction_type_enum already has lowercase values.")

    print("Enum fix complete.")
