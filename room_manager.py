# managers/room_manager.py

import uuid
from typing import List
from room import Room
from player import Player

class RoomManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RoomManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "active_rooms"):
            self.active_rooms: dict[uuid.UUID, Room] = {}

    def create_room(self) -> uuid.UUID:
        room_id = str(uuid.uuid4())
        self.active_rooms[room_id] = Room(room_id)
        return room_id

    def join_room(self, room_id: uuid.UUID, client_id, username: str):

        room = self.active_rooms.get(room_id)
        new_player = Player(client_id=client_id, username=username)
        if room is None:
            raise ValueError(f"error while joining room: room [{room_id}] does not exist")
        
        if room.is_full():
            raise ValueError("Room is full")
        
        if new_player in room.get_players():
            raise ValueError("Player already in room")
        
        room.add_player(new_player)
            
    def get_players(self, room_id):
        room = self.active_rooms.get(room_id)
        if room is not None:
            return room.get_players()
        else:
            raise ValueError(f"No such room [{room_id}]")
        
    def get_players_info(self, room_id):
        room = self.active_rooms.get(room_id)
        if room is not None:
            return [player.get_public_info() for player in room.get_players()]
        else:
            raise ValueError(f"No such room [{room_id}]")
        
    def __getitem__(self, key):
        room =self.active_rooms.get(key)
        if room is None:
            raise KeyError(f"Room [{key}] does not exist")
        return room
        
                
