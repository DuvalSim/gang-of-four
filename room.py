from deck import Card
from player import Player
from typing import List

from game import Game

class Room:

    MAX_PLAYERS = 4

    def __init__(self, room_id) -> None:
        self.room_id = room_id
        self.players = {}
        self.current_game = None

    def add_player(self, player : Player) -> None:
        if len(self.players) < Room.MAX_PLAYERS:
            self.players[player.client_id] = player

    def is_full(self) -> bool:
        return len(self.players) == Room.MAX_PLAYERS
    
    def get_players(self) -> List[Player]:
        return list(self.players.values())
    
    def start_game(self):
        if not self.is_full():
            raise ValueError("Not enought player to start")
        
        self.current_game = Game(list(self.players.values()))

    def get_player(self, client_id):
        player = self.players.get(client_id)
        if player is None:
            raise ValueError(f"Client [{client_id}] not in room")

        return player

    # def play_turn(self, client_id, card_list: List[Card]):
    #     if self.current_game is None:
    #         raise ValueError("No game in progress")
        
    #     player = self.get_player(client_id=client_id)
        
    #     self.current_game.play_turn(player, card_list)


    def get_status(self):
        
        is_game_in_progress = (self.current_game is not None)        
        status = {"game_in_progres" : is_game_in_progress}
                
        if is_game_in_progress:
            status["game_info"] = self.current_game.get_status()

        return status
            

       