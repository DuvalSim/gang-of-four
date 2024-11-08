
from typing import List
from player import Player
from deck import Deck, Card, Suits, Hand, HandType
from operator import itemgetter

import copy
from enum import StrEnum


class Game:

    class GameStatus(StrEnum):
        Playing = 'Playing'
        InterRound = 'InterRound',
        GameEnd = 'End'
    

    def __init__(self, players : List[Player], max_score = 50) -> None:
        if len(players) < 2 or len(players) > 4:
            raise ValueError(f"Need to be 3 or 4 players to play the game")
        
        
        self.max_score = max_score

        self.players_dict = {player.client_id: player for player in players}
        self.scores = {player.client_id: 0 for player in players}
        self.play_order_player_id_list = [player.client_id for player in players]

        self.nb_cards_to_deal = 16

        self.winner = None
        
        self.nb_players = len(players)
        self.current_round = 1
        self.consecutive_pass = 0
        self.previous_hand = None

        self.last_round_looser = None
        self.last_round_winner = None

        self.looser_to_winner_card = None
        self.winner_to_looser_card = None

        self.play_with_one_mult = False

        # 1 is counter clockwise, -1 is clockwise
        self.order_of_play = 1  
    
        # Prepare new round:
        self.deck = Deck()  # Recreate and shuffle the deck
        self.shuffle_deck()
        for player in players:
            player.reset_hand()
        
        self.deal_cards()

        # Get starting player:
        for idx, player_id in enumerate(self.play_order_player_id_list):
            if Card("1", Suits.Multicolor) in self.players_dict[player_id].get_cards_in_hand():
                self.set_current_player(idx)
                self.play_with_one_mult = True
                
                break
        else:
            self.set_current_player(0) 

        self.game_status = self.GameStatus.Playing

        # TODO: make sure first hand has 1 mult in hand

    def is_restartable(self) -> bool:
        return self.game_status == self.GameStatus.GameEnd

    def set_current_player(self, new_idx: int):
        self.current_turn_player_idx = new_idx

    def get_current_player(self):
        return self.players_dict[self.play_order_player_id_list[self.current_turn_player_idx]]

    def next_turn(self):

        current_player = self.get_current_player()

        # Change current turn if necessary
        if self.consecutive_pass == (self.nb_players - 1):
            self.next_cycle()
        
        # Next round
        elif current_player.nb_cards_in_hand() == 0:
            self.next_round()
        else:
            # Keep on playing
            self.set_current_player((self.current_turn_player_idx + self.order_of_play) % self.nb_players)

    def next_cycle(self):
        self.set_current_player((self.current_turn_player_idx + self.order_of_play) % self.nb_players)
        self.previous_hand = None
        self.consecutive_pass = 0

    @staticmethod
    def get_player_round_score(player: Player):
        nb_cards_remaining = len(player.get_cards_in_hand())

        if nb_cards_remaining <= 7:
            return nb_cards_remaining
        elif nb_cards_remaining <= 10:
            return nb_cards_remaining * 2
        elif nb_cards_remaining <= 13:
            return nb_cards_remaining * 3
        elif nb_cards_remaining <= 15:
            return nb_cards_remaining * 4
        else:
            return 80

    def next_round(self):

        # Update scores
        self.last_round_winner = None
        self.last_round_looser = None

        round_scores = {}

        for player in self.players_dict.values():
            player_score = Game.get_player_round_score(player)
            round_scores[player.client_id] = player_score
            self.scores[player.client_id] += player_score

        # Uupdate round winner and looser
        player_id_sorted_by_score = sorted(round_scores, key=round_scores.get)
        worst_score = round_scores[player_id_sorted_by_score[-1]]

        # Winner is unique (has 0 cards left)
        self.last_round_winner = self.players_dict[player_id_sorted_by_score[0]]

        # Can have multiple players with same round score
        round_looser_id_list = [player_id for player_id, player_score in round_scores.items() if (worst_score == player_score)]

        if len(round_looser_id_list) > 1:
            # Choose worse player in game score
            worst_overall_score = self.scores[max(round_looser_id_list, key= lambda player_id: self.scores[player_id])]

            round_looser_id_list = [player_id for player_id in round_looser_id_list if (worst_overall_score == self.scores[player_id])]

            if len(round_looser_id_list) > 1:
                # If still players with same overall score:
                # closest player to the winner in counter clockwise order

                winner_idx = self.play_order_player_id_list.index(self.last_round_winner.client_id)
                round_looser_distance_to_winner = [((self.play_order_player_id_list.index(player_id)-winner_idx) % self.nb_players, player_id) for player_id in round_looser_id_list]
                round_looser_id_list = [min(round_looser_distance_to_winner, key= itemgetter(0))[1]]

        self.last_round_looser = self.players_dict[round_looser_id_list[0]]

        if any([(score >= self.max_score) for score in self.scores.values()]):
            self.end_game()
            return

        # Reset the game for a new round.
        self.current_round += 1
        self.order_of_play *= -1
        self.deck = Deck()  # Recreate and shuffle the deck
        self.shuffle_deck()

        for player in self.players_dict.values():
            player.reset_hand()

        self.deal_cards()

        # Card (Remove) card exchange
        self.looser_to_winner_card = self.last_round_looser.get_best_card()
        self.last_round_looser.remove_card(self.looser_to_winner_card)
        self.last_round_winner.add_cards([self.looser_to_winner_card])
        
        # Prepare new cycle:
        next_player_to_start_idx = self.play_order_player_id_list.index(self.last_round_winner.client_id)
        self.set_current_player(next_player_to_start_idx)
        
        self.consecutive_pass = 0

        self.game_status = self.GameStatus.InterRound

    def complete_card_exchanges(self, client_id,  winner_to_looser_card : Card):

        if self.game_status != self.GameStatus.InterRound:
            raise ValueError("Not right moment")

        if client_id != self.last_round_winner.client_id:
            raise ValueError("Card not coming from last round winner")
        
        self.last_round_winner.remove_card(winner_to_looser_card)
        self.last_round_looser.add_cards([winner_to_looser_card])

        self.winner_to_looser_card = winner_to_looser_card

        self.previous_hand = None

        self.game_status = self.GameStatus.Playing

    def end_game(self):

        self.game_winners = []
        min_value = self.max_score
        for k, v in self.scores.items():
            if v == min_value:
                self.game_winners.append(k)
            elif v < min_value:
                self.game_winners = [k]

        self.game_status = self.GameStatus.GameEnd

    def shuffle_deck(self):
        """Shuffle the deck of cards."""
        self.deck.shuffle()

    def deal_cards(self):
        """Deal cards to all players."""
        card_per_player = self.nb_cards_to_deal
        for player in self.players_dict.values():
            player.add_cards(self.deck.deal_card(card_per_player))

    # def counter_last_card(self, client_id):

    # def call_last_card(self, client_id):
        
    #     if len(self.players_dict[client_id].get_cards_in_hand()) > 1:
    #         raise ValueError("Cannot call last card when more than 1 card in hand")
        
    #     current_player = self.get_current_player()
        
    #     if client_id != current_player.client_id:
    #         raise ValueError("Not current player's turn")
        
    #     self.


    def play_turn(self, client_id , hand_played: Hand = None, pass_turn: bool = False ):

        if self.game_status != self.GameStatus.Playing:
            raise ValueError("Not play phase")

        current_player = self.get_current_player()
        
        if client_id != current_player.client_id:
            raise ValueError("Not current player's turn")
        
        # pass
        if pass_turn:
            if self.previous_hand is None:
                raise ValueError("Cannot pass this turn")            
            self.consecutive_pass += 1

        else:
            if hand_played is None:
                raise ValueError("Cannot play null hand")
            
            if self.play_with_one_mult:
                # This hands has to be played with 1 mult
                if not hand_played.contains(Card("1", Suits.Multicolor)):
                    raise ValueError("First hand of the game has to contain Multicolored 1")
                self.play_with_one_mult = False
            
            # Check valid combination
            if self.previous_hand is not None:

                valid_hand = (hand_played.hand_type == HandType.GANG_OF_X) or (hand_played.get_hand_size() == self.previous_hand.get_hand_size()) 
                if not valid_hand:
                    raise ValueError(f"Hand is not of correct type - Need {self.previous_hand.get_hand_size()} cards")
                if hand_played <= self.previous_hand:
                    raise ValueError("Hand is not stronger that previous one")
            
            current_player.play_hand(cards_played=hand_played.get_card_list())
            self.previous_hand = hand_played

            self.consecutive_pass = 0

        self.next_turn()

    def get_status(self) -> dict:
        
        status_dict = {
            "game_is_on": (self.game_status != self.GameStatus.GameEnd),
            
            "player_to_play": self.get_current_player().client_id,
            "current_round": self.current_round,
            "play_direction": "clockwise" if (self.order_of_play == 1) else "counter_clockwise",
            "players_info": {
                player.client_id: { "nb_cards": player.nb_cards_in_hand(),
                                   "score": self.scores[player.client_id] } 
                for player in self.players_dict.values()
            },            
            "previous_hand": self.previous_hand.get_str_card_list() if self.previous_hand is not None else None, 
        }

        if self.game_status == self.GameStatus.InterRound:
            status_dict["inter_round_info"] = {
                "last_winner" : self.last_round_winner.client_id,
                "last_looser" : self.last_round_looser.client_id,
                "looser_to_winner_card" : str(self.looser_to_winner_card)
            }

        if self.game_status == self.GameStatus.GameEnd:
            status_dict["game_winners"] = self.game_winners

        return status_dict
    
    def get_winner_to_looser_card(self):
        return self.winner_to_looser_card
    
    def get_card_exchange_info(self):
        return {
            "last_winner" : self.last_round_winner.client_id,
            "last_looser" : self.last_round_looser.client_id,
            "looser_to_winner_card" : str(self.looser_to_winner_card),
            "winner_to_looser_card" : str(self.winner_to_looser_card)
        }
  
    def __str__(self):
        return f"Game with {len(self.players_dict)} players, Round: {self.current_round} - Scores: {self.scores}"