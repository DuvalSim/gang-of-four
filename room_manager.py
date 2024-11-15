# managers/room_manager.py

from typing import List
from room import Room
from player import Player
from socket_manager import SocketManager
from nanoid import generate
from utils.InvalidRequestException import InvalidRequestException

socket_manager = SocketManager()

class RoomManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(RoomManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "active_rooms"):
            self.active_rooms: dict[str, Room] = {}

    def __generate_id(self) -> str:
        new_id = generate(size=10)
        while new_id in self.active_rooms.keys():
            new_id = new_id = generate(size=10)
        
        return new_id
    
    def create_room(self) -> str:
        room_id = self.__generate_id()
        self.active_rooms[room_id] = Room(room_id)
        return room_id

    def join_room(self, room_id: str, socket_id, client_id, username: str):

        room = self.active_rooms.get(room_id)
        new_player = Player(client_id=client_id, username=username)
        if room is None:
            raise InvalidRequestException(f"error while joining room: room [{room_id}] does not exist")
        
        if room.is_full():
            raise InvalidRequestException("Room is full")
        
        if new_player in room.get_players():
            raise InvalidRequestException("Player already in room")
        
        if socket_manager.get_user_room_id(user_id=client_id) is not None:
            raise InvalidRequestException("Player already in a room")
        
        if room.current_game is not None:
            raise InvalidRequestException("Cannot join while a game is played")
        
        room.add_player(new_player)

        socket_manager.add_user(user_id=client_id, socket_id=socket_id, room_id=room_id)

    
    def leave_room(self, room_id: str, user_id):
        room = self.active_rooms.get(room_id)
        if room is None:
            raise InvalidRequestException(f"error while leaving room: room [{room_id}] does not exist")
        
        if user_id not in room.players.keys():
            raise InvalidRequestException("Player not in room")
        
        room.remove_player(user_id)
        socket_manager.remove_user(user_id=user_id)

        if len(room.get_players()) == 0:
            self.remove_room(room_id)
    
    def get_room(self, room_id: str) -> Room | None:
        return self.active_rooms.get(room_id, None)

    def get_room_from_user(self, user_id) -> str:
        return socket_manager.get_user_room_id(user_id=user_id)
    
    def remove_room(self, room_id):

        for player in self.active_rooms[room_id].get_players():
            socket_manager.remove_user(player.client_id)

        del self.active_rooms[room_id]

    def leave_room(self, room_id, user_id):
        current_room = self.active_rooms[room_id]
        current_room.remove_player(user_id)
        socket_manager.remove_user(user_id)
        if len(current_room.get_players()) == 0:
            self.remove_room(room_id)

    def set_inactive_user(self, user_id):
        room_id = self.get_room_from_user(user_id)
        if room_id and user_id :
            self.active_rooms[room_id].get_player(user_id).set_active(False)
            if not any([player.is_active for player in self.active_rooms[room_id].get_players()]):
                self.remove_room(room_id)                

    def on_user_disconnect(self, user_id, room_id):
        current_room = self.active_rooms[room_id]
        if current_room and current_room.current_game:
            self.set_inactive_user(user_id)
        elif current_room:
            self.leave_room(room_id, user_id)  
            
    def get_players(self, room_id):
        room = self.active_rooms.get(room_id)
        if room is not None:
            return room.get_players()
        else:
            raise InvalidRequestException(f"No such room [{room_id}]")
        
    def get_players_info(self, room_id):
        room = self.active_rooms.get(room_id)
        if room is not None:
            return [player.get_public_info() for player in room.get_players()]
        else:
            raise InvalidRequestException(f"No such room [{room_id}]")
        
    def __getitem__(self, key):
        room =self.active_rooms.get(key)
        if room is None:
            raise KeyError(f"Room [{key}] does not exist")
        return room
        
                
