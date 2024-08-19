# app/routers/routes.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from typing import Dict

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, Dict[int, WebSocket]] = {}

    async def connect(self, chat_id: str, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if chat_id not in self.active_connections:
            self.active_connections[chat_id] = {}
        self.active_connections[chat_id][user_id] = websocket

    def disconnect(self, chat_id: str, user_id: int):
        if chat_id in self.active_connections:
            del self.active_connections[chat_id][user_id]
            if not self.active_connections[chat_id]:
                del self.active_connections[chat_id]

    async def send_personal_message(self, message: str, chat_id: str, user_id: int):
        if chat_id in self.active_connections and user_id in self.active_connections[chat_id]:
            websocket = self.active_connections[chat_id][user_id]
            await websocket.send_text(message)
        else:
            raise HTTPException(status_code=404, detail="User not connected")

    async def broadcast(self, message: str, chat_id: str):
        if chat_id in self.active_connections:
            for user_id, connection in self.active_connections[chat_id].items():
                await connection.send_text(message)

manager = ConnectionManager()

@router.websocket("/ws/chat/{chat_id}/{user_id}")
async def chat_websocket(websocket: WebSocket, chat_id: str, user_id: int):
    await manager.connect(chat_id, user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"User {user_id}: {data}", chat_id)
    except WebSocketDisconnect:
        manager.disconnect(chat_id, user_id)
        await manager.broadcast(f"User {user_id} left the chat", chat_id)
