from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql://neondb_owner:8EG0IaWfuTJM@ep-cool-butterfly-a5jzey8j-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"  # or your database URL

engine = create_engine(DATABASE_URL)

def get_db() -> Session: # type: ignore
    with Session(engine) as session:
        yield session
