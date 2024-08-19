# app/routers/routes.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from app.models.user import User
import math
from typing import Dict, List

router = APIRouter()

users = [
    User(user_id=1, name="Alice", age=25, gender="female", tags=["developer", "gamer"]),
    User(user_id=2, name="Bob", age=24, gender="male", tags=["designer", "blogger", "movies"]),
    User(user_id=3, name="Charlie", age=22, gender="male", tags=["student", "musician"]),
    User(user_id=4, name="Diana", age=23, gender="female", tags=["artist"]),
    User(user_id=5, name="Eve", age=21, gender="female", tags=["engineer", "painter"]),
    User(user_id=6, name="Frank", age=20, gender="male", tags=["teacher", "writer"]),
    User(user_id=7, name="Grace", age=24, gender="female", tags=["gamer"]),
    User(user_id=8, name="Hank", age=25, gender="male", tags=["developer", "musician"]),
    User(user_id=9, name="Ivy", age=22, gender="female", tags=["photographer"]),
    User(user_id=10, name="Jack", age=23, gender="male", tags=["student", "artist", "gamer"]),
    User(user_id=11, name="Kara", age=20, gender="female", tags=["musician", "writer"]),
    User(user_id=12, name="Leo", age=19, gender="male", tags=["engineer", "student"]),
    User(user_id=13, name="Mona", age=21, gender="female", tags=["gamer", "movies"]),
    User(user_id=14, name="Nina", age=18, gender="female", tags=["artist", "travel"]),
    User(user_id=15, name="Oscar", age=22, gender="male", tags=["designer", "photographer"]),
    User(user_id=16, name="Paul", age=25, gender="male", tags=["teacher", "sports"]),
    User(user_id=17, name="Quinn", age=24, gender="female", tags=["painter", "movies"]),
    User(user_id=18, name="Rose", age=23, gender="female", tags=["student", "gamer"]),
    User(user_id=19, name="Sam", age=21, gender="male", tags=["musician", "coding"]),
    User(user_id=20, name="Tina", age=20, gender="female", tags=["writer", "travel"]),
    User(user_id=21, name="Uma", age=19, gender="female", tags=["photographer", "music"]),
    User(user_id=22, name="Victor", age=22, gender="male", tags=["gamer"]),
    User(user_id=23, name="Wendy", age=24, gender="female", tags=["painter"]),
    User(user_id=24, name="Xander", age=18, gender="male", tags=["student", "sports"]),
    User(user_id=25, name="Yara", age=25, gender="female", tags=["artist"]),
    User(user_id=26, name="Zane", age=23, gender="male", tags=["designer", "gamer"]),
    User(user_id=27, name="Amy", age=24, gender="female", tags=["engineer", "movies"]),
    User(user_id=28, name="Ben", age=21, gender="male", tags=["musician", "sports"]),
    User(user_id=29, name="Cara", age=22, gender="female", tags=["photographer"]),
    User(user_id=30, name="Dave", age=25, gender="male", tags=["writer", "movies"]),
    User(user_id=31, name="Ella", age=20, gender="female", tags=["painter", "travel"]),
    User(user_id=32, name="Finn", age=19, gender="male", tags=["student", "gamer"]),
    User(user_id=33, name="Gina", age=18, gender="female", tags=["artist", "music"]),
    User(user_id=34, name="Hugo", age=21, gender="male", tags=["engineer"]),
    User(user_id=35, name="Iris", age=22, gender="female", tags=["musician"]),
    User(user_id=36, name="Jake", age=23, gender="male", tags=["designer", "sports"]),
    User(user_id=37, name="Lara", age=24, gender="female", tags=["writer", "photographer"]),
    User(user_id=38, name="Mark", age=25, gender="male", tags=["gamer", "movies"]),
    User(user_id=39, name="Nora", age=20, gender="female", tags=["painter"]),
    User(user_id=40, name="Owen", age=19, gender="male", tags=["student", "musician"]),
    User(user_id=41, name="Pia", age=18, gender="female", tags=["photographer"]),
    User(user_id=42, name="Rick", age=21, gender="male", tags=["sports"]),
    User(user_id=43, name="Sara", age=22, gender="female", tags=["gamer"]),
    User(user_id=44, name="Tom", age=23, gender="male", tags=["designer"]),
    User(user_id=45, name="Vera", age=24, gender="female", tags=["artist", "movies"]),
    User(user_id=46, name="Will", age=25, gender="male", tags=["writer", "music"]),
    User(user_id=47, name="Zoe", age=19, gender="female", tags=["student", "painter"]),
    User(user_id=48, name="Aaron", age=20, gender="male", tags=["photographer", "gamer"]),
    User(user_id=49, name="Beth", age=21, gender="female", tags=["musician", "travel"]),
    User(user_id=50, name="Chris", age=22, gender="male", tags=["designer", "writer"]),
]

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

def get_user(user_id: int):
    user = next((u for u in users if u.user_id == user_id), None)
    if user:
        return user.name
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.websocket("/ws/chat/{chat_id}/{user_id}")
async def chat_websocket(websocket: WebSocket, chat_id: str, user_id: int):
    await manager.connect(chat_id, user_id, websocket)
    user = get_user(user_id=user_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"{user}: {data}", chat_id)
    except WebSocketDisconnect:
        manager.disconnect(chat_id, user_id)
        await manager.broadcast(f"{user} left the chat", chat_id)

# match algorithm
def calculate_age_similarity(age1: int, age2: int) -> float:
    max_age_diff = 6  # Increasing the range to allow for more variation in age similarity
    age_diff = abs(age1 - age2)
    
    if age_diff > max_age_diff:
        return 0.0  # No similarity if age difference is too large
    
    return math.exp(-0.5 * (age_diff / max_age_diff))

def calculate_tag_similarity(tags1: List[str], tags2: List[str]) -> float:
    set1 = set(tags1)
    set2 = set(tags2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    
    if not union:
        return 0.0
    
    intersection_score = len(intersection) / len(union)
    
    # Give extra points for each matching tag
    bonus = 0.1 * len(intersection)
    
    return min(intersection_score + bonus, 1.0)

def calculate_match_score(user1: User, user2: User) -> float:
    weights = {
        "age": 0.3,
        "tags": 0.7
    }

    age_score = calculate_age_similarity(user1.age, user2.age)
    tag_score = calculate_tag_similarity(user1.tags, user2.tags)

    total_score = (
        weights["age"] * age_score +
        weights["tags"] * tag_score
    )

    return round(total_score * 100, 2)

def find_best_matches(user: User, users: List[User], top_n: int = 3) -> List[Dict[str, any]]:
    scores = []
    for u in users:
        if u.user_id != user.user_id:
            score = calculate_match_score(user, u)
            scores.append({"user": u, "score": score})
    scores.sort(key=lambda x: x["score"], reverse=True)
    return scores[:top_n]

@router.get("/match/{user_id}")
def get_matches(user_id: int, top_n: int = len(users) - 1):
    user = next((u for u in users if u.user_id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    matches = find_best_matches(user, users, top_n)
    return {
        "matches": matches,
        "username": user.name
        }