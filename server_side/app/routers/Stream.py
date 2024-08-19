# app/routers/Stream.py

from fastapi import APIRouter
from app.models.StreamRequest import StreamRequest
from fastapi.responses import StreamingResponse
from app.langchain import send_message

router = APIRouter()

@router.post("/stream")
def stream(body: StreamRequest):
    return StreamingResponse(send_message(body.message), media_type="text/event-stream")