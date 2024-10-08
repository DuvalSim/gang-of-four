
from typing import List
from player import Player
from deck import Deck, Card, Suits

import copy


class Game:

    def __init__(self, players : List[Player]) -> None:
        if len(players) != 4:
            raise ValueError("Need 4 players to start game")
        self.players = players
        self.current_round = 0
        self.scores = {player.client_id: 0 for player in self.players}
        self.new_round()

    def new_round(self):
        """Reset the game for a new round."""
        self.current_round += 1
        self.deck = Deck()  # Recreate and shuffle the deck
        self.shuffle_deck()
        for player in self.players:
            player.reset_hand()

        self.current_turn_player_idx = 0

        self.deal_cards()

    def shuffle_deck(self):
        """Shuffle the deck of cards."""
        self.deck.shuffle()

    def deal_cards(self):
        """Deal cards to all players."""
        card_per_player = self.deck.nb_cards() // 4
        for player in self.players:
            player.add_cards(self.deck.deal_card(card_per_player))

    def play_turn(self, client_id , hand_played: List[Card]):

        client_idx = self.players.index(Player(client_id)) 
        # Check turn
        if client_idx != self.current_turn_player_idx:
            raise ValueError("Not current player's turn")
        
        # Check valid combination

        
        # play cards
        current_player = self.players[client_idx]        
        current_player.play_hand(hand_played=hand_played)

        # Change current turn
        self.current_turn_player_idx = (self.current_turn_player_idx + 1) % 4

    def get_status(self):
        return {
            "player_to_play": self.players[self.current_turn_player_idx].client_id,
            "current_round": self.current_round,
            "players_info": {
                player.client_id: { "nb_cards": player.nb_cards_in_hand(),
                                   "score": self.scores[player.client_id] } 
                for player in self.players
            }
        }
            
            
    

    def __str__(self):
        return f"Game with {len(self.players)} players, Round: {self.current_round} - Scores: {self.scores}"