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
    print("--- CURRENT ENUM VALUES IN DATABASE ---")
    
    # Debug user_roles_enum
    result = conn.execute(text(
        "SELECT enumlabel FROM pg_enum e JOIN pg_type t ON e.enumtypid = t.oid "
        "WHERE t.typname = 'user_roles_enum'"
    ))
    roles = [row[0] for row in result]
    print(f"user_roles_enum values: {roles}")

    # Debug transaction_type_enum
    result = conn.execute(text(
        "SELECT enumlabel FROM pg_enum e JOIN pg_type t ON e.enumtypid = t.oid "
        "WHERE t.typname = 'transaction_type_enum'"
    ))
    tx_types = [row[0] for row in result]
    print(f"transaction_type_enum values: {tx_types}")

    print("--- END ENUM VALUES ---")

    # If the database has NO values for the enum for some reason, maybe the type got messed up?
    # Or if they are Title Case ('Admin', 'Analyst', 'Viewer') let's fix them.
    for role in roles:
        if role != role.lower():
            print(f"Found non-lowercase role: {role}, renaming to {role.lower()}")
            try:
                conn.execute(text(f"ALTER TYPE user_roles_enum RENAME VALUE '{role}' TO '{role.lower()}'"))
                conn.commit()
            except Exception as e:
                print(f"Failed to rename {role}: {e}")

    for tx in tx_types:
        if tx != tx.lower():
            lower_tx = tx.lower()
            if lower_tx == 'expenses':
                lower_tx = 'expense'
            if lower_tx != tx:
                print(f"Found non-lowercase tx type: {tx}, renaming to {lower_tx}")
                try:
                    conn.execute(text(f"ALTER TYPE transaction_type_enum RENAME VALUE '{tx}' TO '{lower_tx}'"))
                    conn.commit()
                except Exception as e:
                    print(f"Failed to rename {tx}: {e}")

    print("Enum fix complete.")
