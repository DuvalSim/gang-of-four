
from typing import List
from player import Player
from deck import Deck, Card, Suits, Hand, CombinationType

import copy


class Game:

    def __init__(self, players : List[Player]) -> None:
        if len(players) != 4:
            raise ValueError("Need 4 players to start game")
        self.players = players
        self.current_round = 0
        self.scores = {player.client_id: 0 for player in self.players}
        self.current_turn_player_idx = 0

        self.start_new_round()
        self.new_cycle()

    def new_cycle(self):
        self.previous_hand = None
        self.consecutive_pass = 0

    def score_round(self):
        for player in self.players:
            self.scores[player.client_id] += player.nb_cards_in_hand()

    def start_new_round(self):
        """Reset the game for a new round."""
        self.current_round += 1
        self.deck = Deck()  # Recreate and shuffle the deck
        self.shuffle_deck()
        for player in self.players:
            player.reset_hand()

        self.deal_cards()

    def shuffle_deck(self):
        """Shuffle the deck of cards."""
        self.deck.shuffle()

    def deal_cards(self):
        """Deal cards to all players."""
        card_per_player = self.deck.nb_cards() // 4
        for player in self.players:
            player.add_cards(self.deck.deal_card(card_per_player))

    def play_turn(self, client_id , hand_played: Hand = None, pass_turn: bool = False ):

        client_idx = self.players.index(Player(client_id)) 
        
        if client_idx != self.current_turn_player_idx:
            raise ValueError("Not current player's turn")
        current_player = self.players[client_idx]  
        
        # pass
        if pass_turn:
            if self.previous_hand is None:
                raise ValueError("Cannot pass this turn")            
            self.consecutive_pass += 1

        else:
            if hand_played is None:
                raise ValueError("Cannot play null hand")
            
            # Check valid combination
            if self.previous_hand is not None:
                valid_hand = (hand_played.combination == CombinationType.GANG_OF_X) or (hand_played.get_hand_size() == self.previous_hand.get_hand_size()) 
                if not valid_hand:
                    raise ValueError(f"Hand is not of correct type - Need {self.previous_hand.get_hand_size()} cards")
                if hand_played <= self.previous_hand:
                    raise ValueError("Hand is not stronger that previous one")
            
            current_player.play_hand(cards_played=hand_played.get_card_list())
            self.previous_hand = hand_played

        # Change current turn if necessary
        if self.consecutive_pass == 3:
            self.new_cycle()
            self.current_turn_player_idx = (self.current_turn_player_idx + 1) % 4  
        
        # Next round
        elif current_player.nb_cards_in_hand == 0:
            self.score_round()
            self.start_new_round()
        else:
            # Keep on playing
            self.current_turn_player_idx = (self.current_turn_player_idx + 1) % 4  
            

    def get_player_status(self, client_id):
        client_idx = self.players.index(Player(client_id)) 
        
        if client_idx != self.current_turn_player_idx:
            raise ValueError("Not current player's turn")
        current_player = self.players[client_idx]  


    def get_status(self):
        return {
            "player_to_play": self.players[self.current_turn_player_idx].client_id,
            "current_round": self.current_round,
            "players_info": {
                player.client_id: { "nb_cards": player.nb_cards_in_hand(),
                                   "score": self.scores[player.client_id] } 
                for player in self.players
            },
            "previous_hand": self.previous_hand.get_str_card_list() if self.previous_hand is not None else None
        }
            
            
    

    def __str__(self):
        return f"Game with {len(self.players)} players, Round: {self.current_round} - Scores: {self.scores}"