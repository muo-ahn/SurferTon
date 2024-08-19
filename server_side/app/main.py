# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import routes

app = FastAPI()

# Configure CORS
origins = [
    "http://localhost:3000",  # Your client URL
    "http://127.0.0.1:3000",  # Also include localhost with IP
    # Add other origins if needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)
