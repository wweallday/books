from fastapi import FastAPI
from models import *
from routers import api

app = FastAPI()  # This is the "app" that FastAPI expects

app.include_router(api.api_router)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}
