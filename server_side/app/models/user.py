# app/models/user.py

from pydantic import BaseModel
from typing import List

class User(BaseModel):
    user_id: int
    name: str
    age: int
    gender: str
    tags: List[str]