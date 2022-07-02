import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

dotenv.load_dotenv()

db_host = os.getenv('DB_HOST')
user_name = os.getenv('DB_USER')
user_pwd = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_DATABASE')
db_port = os.getenv('DB_PORT')

SQLALCHEMY_DATABASE_URL = f"mysql://{user_name}:{user_pwd}@{db_host}:{db_port}/{db_name}?charset=utf8"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_recycle=900,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
