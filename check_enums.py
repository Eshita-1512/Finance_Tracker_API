
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

with engine.connect() as connection:
    result = connection.execute(text("SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE pg_type.typname = 'user_roles_enum';"))
    print("Enum values for user_roles_enum:")
    for row in result:
        print(row[0])

    result = connection.execute(text("SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE pg_type.typname = 'transaction_type_enum';"))
    print("\nEnum values for transaction_type_enum:")
    for row in result:
        print(row[0])
