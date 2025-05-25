# flake8: noqa

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from motor.motor_asyncio import AsyncIOMotorClient
from config import config




# === SQLAlchemy (PostgresQL) setup ===
engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


# === MongoDB setup ===
mongo_client = AsyncIOMotorClient(config.MONGO_URI)
config.logger.debug(f"Connected to MongoDB at {config.MONGO_URI} and {config.MONGO_DB_NAME}")
db = mongo_client[config.MONGO_DB_NAME]
categories_collection = db["user_categories"]
