import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Use AUTOCOMMIT isolation level for ALTER TYPE commands
engine = create_engine(DATABASE_URL)

def run_fix():
    with engine.connect() as conn:
        # PostgreSQL doesn't allow ALTER TYPE inside transactions for adding values
        # We use execution_options to set AUTOCOMMIT for this connection
        conn = conn.execution_options(isolation_level="AUTOCOMMIT")
        
        print("--- FIXING ENUMS ---")
        
        # 1. Ensure user_roles_enum has all values
        for role in ['admin', 'analyst', 'viewer']:
            try:
                # Add value if it doesn't exist
                conn.execute(text(f"ALTER TYPE user_roles_enum ADD VALUE IF NOT EXISTS '{role}'"))
                print(f"Ensured role '{role}' exists.")
            except Exception as e:
                print(f"Skipped adding role {role}: {e}")

        # 2. Ensure transaction_type_enum has all values
        for tx_type in ['income', 'expense']:
            try:
                conn.execute(text(f"ALTER TYPE transaction_type_enum ADD VALUE IF NOT EXISTS '{tx_type}'"))
                print(f"Ensured tx type '{tx_type}' exists.")
            except Exception as e:
                print(f"Skipped adding tx type {tx_type}: {e}")

        print("Enum fix complete.")

if __name__ == "__main__":
    run_fix()
