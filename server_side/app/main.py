# app/main.py

from fastapi import FastAPI
from app.routers import routes

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to the 1:1 chat app"}

app.include_router(routes.router)
