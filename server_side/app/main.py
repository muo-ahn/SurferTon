# app/main.py

from fastapi import FastAPI
from app.routers import Stream
app = FastAPI()

app.include_router(Stream.router)
