import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker

#DATABASE_URL = "postgresql://postgres:rootadmin@localhost:5435/fastapi_blog_db"
DATABASE_URL = "postgresql+psycopg://postgres:rootadmin@localhost:5435/fastapi_blog_db"

#Create Database Engine
engine = create_engine(DATABASE_URL)

# Setup Session Schema
SessionLocal = sessionmaker(bind=engine)

#For Model
Base = declarative_base()