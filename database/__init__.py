# flake8: noqa

from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from config import config




# === SQLAlchemy (PostgresQL) setup ===
engine = config.get_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# === MongoDB setup ===
mongo_client = config.get_mongo_client()
config.logger.debug(f"Connected to MongoDB")
db = mongo_client[config.get_mongo_db_name()]
categories_collection = db["user_categories"]
