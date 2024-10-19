from fastapi import FastAPI
from models import *
from database import init_db
from routers import api

app = FastAPI()  # This is the "app" that FastAPI expects

app.include_router(api.api_router)

# Call init_db on startup
@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
