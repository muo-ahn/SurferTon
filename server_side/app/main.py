from fastapi import FastAPI
from app.routers import items

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to my FastAPI project!"}

app.include_router(items.router)
