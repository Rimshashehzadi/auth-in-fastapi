# from sqlmodel import SQLModel, Field, create_engine
# from sqlalchemy.ext.declarative import DeclarativeMeta

# DATABASE_URL = "postgresql://neondb_owner:8EG0IaWfuTJM@ep-cool-butterfly-a5jzey8j-pooler.us-east-2.aws.neon.tech/neondb?sslmode=require"
# engine = create_engine(DATABASE_URL)

# class User(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     email: str = Field(unique=True, index=True)
#     hashed_password: str
#     otp: str = Field(default=None)
#     is_verified: bool = Field(default=False)

# # Create the database tables
# SQLModel.metadata.create_all(engine)
