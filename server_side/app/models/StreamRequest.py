# app/models/StreamRequest.py

from pydantic import BaseModel

class StreamRequest(BaseModel):
    message: str