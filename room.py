from deck import Card
from player import Player
from typing import List
from socket_manager import SocketManager

from game import Game

socket_manager = SocketManager()

class Room:

    MAX_PLAYERS = 4

    def __init__(self, room_id) -> None:
        self.room_id = room_id
        self.players = {}
        self.current_game = None
        self.room_manager_user_id = None

    def add_player(self, player : Player) -> None:
        if len(self.players) < Room.MAX_PLAYERS:
            self.players[player.client_id] = player

        if self.room_manager_user_id is None:
            self.room_manager_user_id = player.client_id

    def remove_player(self, client_id) -> None:
        del self.players[client_id]
        if len(self.players) > 0:
            self.room_manager_user_id = list(self.players)[0]
        else:
            self.room_manager_user_id = None

    def is_full(self) -> bool:
        return len(self.players) == Room.MAX_PLAYERS
    
    def get_players(self) -> List[Player]:
        return list(self.players.values())
    
    def start_game(self, user_id):
        # TODO
        # if not self.is_full():
        #     raise ValueError("Not enought player to start")
        if Player(user_id) not in self.get_players():
            raise ValueError("WTF get out of there")

        if self.current_game is None or self.current_game.is_restartable():
            self.current_game = Game(list(self.players.values()))
        else:
            raise ValueError("Game already on")
        
    def get_player(self, client_id) -> Player:
        player = self.players.get(client_id)
        if player is None:
            raise ValueError(f"Client [{client_id}] not in room")

        return player

    # def play_turn(self, client_id, card_list: List[Card]):
    #     if self.current_game is None:
    #         raise ValueError("No game in progress")
        
    #     player = self.get_player(client_id=client_id)
        
    #     self.current_game.play_turn(player, card_list)

    def get_room_info(self):
        return {
            "room_id": self.room_id,
            "users": [player.get_public_info() for player in self.get_players()],
            "leader": self.room_manager_user_id
        }


    def get_status(self):
        
        is_game_in_progress = (self.current_game is not None)        
        status = {"game_in_progres" : is_game_in_progress}
                
        if is_game_in_progress:
            status["game_info"] = self.current_game.get_status()

        return status
            

       