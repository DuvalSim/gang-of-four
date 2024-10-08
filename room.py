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
        
        self.current_game = Game(self.players)

    def check_valid_player(self, client_id):
        if self.players.get(client_id) is None:
            raise ValueError(f"Client [{client_id}] not in room")

    def play_turn(self, client_id, card_list: List[Card]):
        if self.current_game is None:
            raise ValueError("No game in progress")
        
        player = self.players.get(client_id)
        if player is None:
            raise ValueError("")
        
        self.current_game.play_turn():


    def get_status(self):
        return self.current_game.get_status()

       