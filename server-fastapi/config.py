
import os
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv('DB_HOST')
user_name = os.getenv('DB_USER')
user_pwd = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_DATABASE')
db_port = os.getenv('DB_PORT')

DATABASE = f"mysql://{user_name}:{user_pwd}@{db_host}:{db_port}/{db_name}?charset=utf8"
