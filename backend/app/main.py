from fastapi import FastAPI
from .database import engine, Base
from .api import router as api_router

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(api_router, prefix="/api") # You can use /api for APIs

@app.get("/")
async def read_root():
    return {"message": "Welcome to E2E Notepad and Password Manager API"}
