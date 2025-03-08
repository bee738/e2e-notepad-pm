import os

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@db:5432/e2e_notepad_db") # 'db' is the service name in docker-compose
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-for-jwt-replace-in-production") # Change this in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
