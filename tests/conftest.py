import os

# Fake/test environment variables
os.environ["BOT_TOKEN"] = "fake-token"
os.environ["DATABASE_URL"] = "postgresql://user:password@localhost:5432/test_db"
os.environ["MONGO_URI"] = "mongodb://localhost:27017"
os.environ["MONGO_DB_NAME"] = "test_db"
