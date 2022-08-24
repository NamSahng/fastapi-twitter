import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import models

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PWD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')

SQLALCHEMY_URL = f"mysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}"
SQLALCHEMY_DATABASE_URL = SQLALCHEMY_URL + f"/{DB_NAME}?charset=utf8mb4"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_recycle=900,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def _database_exist(engine, schema_name):
    query = f"SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{schema_name}'"
    with engine.connect() as conn:
        result_proxy = conn.execute(query)
        result = result_proxy.scalar()
        return bool(result)

def _create_database(engine, schema_name):
    with engine.connect() as conn:
        conn.execute(f"CREATE DATABASE {schema_name} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;")

def init_database(engine=engine, schema_name=DB_NAME):
    print("creation")
    db_engine = create_engine(SQLALCHEMY_URL)

    # create Database
    if not _database_exist(db_engine, schema_name):
        _create_database(db_engine, schema_name)

    # create Tables
    models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
