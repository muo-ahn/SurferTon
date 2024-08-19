# app/models/__init__.py

from app.models.user import User

# Define a list of dummy users
dummy_users = [
    User(user_id=1, name="Alice", age=25, gender="female", tags=["developer", "gamer"]),
    User(user_id=2, name="Bob", age=30, gender="male", tags=["designer", "blogger"]),
    User(user_id=3, name="Charlie", age=22, gender="male", tags=["student", "musician"]),
    User(user_id=4, name="Diana", age=28, gender="female", tags=["artist", "photographer"]),
]