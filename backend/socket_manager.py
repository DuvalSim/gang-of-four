
from player import Player
from typing import List

class SocketManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SocketManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "userSocketMapping"):
            self.userSocketMapping = {}
            self.userRoomMapping = {}

    def add_user(self, user_id, socket_id, room_id: str):
        self.userSocketMapping[user_id] = socket_id
        self.userRoomMapping[user_id] = room_id

    def remove_user(self, user_id):
        del self.userRoomMapping[user_id]
        del self.userSocketMapping[user_id]
        
    def get_user_room_id(self, user_id):
        return self.userRoomMapping.get(user_id, None)
    
    def get_user_socket_id(self, user_id):
        return self.userSocketMapping.get(user_id, None)
    
    def get_user_from_socket(self, socket_id):
        for user_id, sid in self.userSocketMapping.items():
            if sid == socket_id:
                return user_id
        else:
            return None
        
    def update_user_socket(self, user_id, socket_id):
        self.userSocketMapping[user_id] = socket_id

