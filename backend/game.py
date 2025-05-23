
from typing import List
from player import Player
from deck import Deck, Card, Suits, Hand, HandType
from operator import itemgetter
from utils.InvalidRequestException import InvalidRequestException

from copy import deepcopy

from utils.hand_helpers import get_playable_combinations, argsort_cards

import copy
from enum import StrEnum


class Game:

    class GameStatus(StrEnum):
        Playing = 'Playing'
        InterRound = 'InterRound',
        GameEnd = 'End'
    

    def __init__(self, players : List[Player], max_score = 50) -> None:
        if len(players) < 2 or len(players) > 4:
            raise InvalidRequestException(f"Need to be 3 or 4 players to play the game")
        
        
        self.max_score = max_score

        self.players_dict = {player.client_id: player for player in players}
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

        # handle last_card
        self.safe_players = []
        self.blocked_players = []

    def get_active_players_id(self) -> List[str]:
        return [player.get_user_id() for player in self.players_dict.values() if player.is_active]

    def remove_player(self, user_id):
  
        current_player_id = self.get_current_player().client_id
        if user_id != current_player_id:
            self.play_order_player_id_list.remove(user_id)
        else:
            next_player_id = self.play_order_player_id_list[self.get_next_player_idx()]
            self.play_order_player_id_list.remove(user_id)
            self.current_turn_player_idx = self.play_order_player_id_list.index(next_player_id)
        
        

    def _get_nb_playing_players(self)-> int:
        return len(self.play_order_player_id_list)

    def is_restartable(self) -> bool:
        return self.game_status == self.GameStatus.GameEnd

    def set_current_player(self, new_idx: int):
        self.current_turn_player_idx = new_idx

    def get_current_player(self):
        return self.players_dict[self.play_order_player_id_list[self.current_turn_player_idx]]

    def next_turn(self):

        current_player = self.get_current_player()

        # Change current turn if necessary
        if self.consecutive_pass == (self._get_nb_playing_players() - 1):
            self.next_cycle()
        
        # Next round
        elif current_player.nb_cards_in_hand() == 0:
            self.next_round()
        else:
            # Keep on playing
            self.set_current_player(self.get_next_player_idx())

    def get_next_player_idx(self):
        next_player_idx = (self.current_turn_player_idx + self.order_of_play) % self._get_nb_playing_players()
            
        return next_player_idx

    def next_cycle(self):
        self.set_current_player(self.get_next_player_idx())
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
        current_scores = {}

        for player in self.players_dict.values():
            player_score = Game.get_player_round_score(player)
            player.score_round(self.current_round, player_score)
            round_scores[player.client_id] = player_score
            current_scores[player.client_id] = player.get_score()

        # Uupdate round winner and looser
        player_id_sorted_by_score = sorted(round_scores, key=round_scores.get)
        worst_score = round_scores[player_id_sorted_by_score[-1]]

        # Winner is unique (has 0 cards left)
        self.last_round_winner = self.players_dict[player_id_sorted_by_score[0]]

        # Can have multiple players with same round score
        round_looser_id_list = [player_id for player_id, player_score in round_scores.items() if (worst_score == player_score)]

        if len(round_looser_id_list) > 1:
            # Choose worse player in game score
            worst_overall_score = current_scores[max(round_looser_id_list, key= lambda player_id: current_scores[player_id])]

            round_looser_id_list = [player_id for player_id in round_looser_id_list if (worst_overall_score == current_scores[player_id])]

            if len(round_looser_id_list) > 1:
                # If still players with same overall score:
                # closest player to the winner in counter clockwise order

                winner_idx = self.play_order_player_id_list.index(self.last_round_winner.client_id)
                round_looser_distance_to_winner = [((self.play_order_player_id_list.index(player_id)-winner_idx) % self.nb_players, player_id) for player_id in round_looser_id_list]
                round_looser_id_list = [min(round_looser_distance_to_winner, key= itemgetter(0))[1]]

        self.last_round_looser = self.players_dict[round_looser_id_list[0]]

        if any([(score >= self.max_score) for score in current_scores.values()]):
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

        # reset players in play
        self.play_order_player_id_list = self.get_active_players_id()
        self.blocked_players = []
        self.safe_players = []

        # Check in case winner left after winning
        if self.last_round_winner.client_id in self.play_order_player_id_list:
            next_player_to_start_idx =  self.play_order_player_id_list.index(self.last_round_winner.client_id)
        else:
            next_player_to_start_idx = 0

        self.set_current_player(next_player_to_start_idx)
        
        self.consecutive_pass = 0

        self.game_status = self.GameStatus.InterRound

    def complete_card_exchanges(self, client_id,  winner_to_looser_card : Card):

        if self.game_status != self.GameStatus.InterRound:
            raise InvalidRequestException("Not right moment")

        if client_id != self.last_round_winner.client_id:
            raise InvalidRequestException("Card not coming from last round winner")
        
        self.last_round_winner.remove_card(winner_to_looser_card)
        self.last_round_looser.add_cards([winner_to_looser_card])

        self.winner_to_looser_card = winner_to_looser_card

        self.previous_hand = None

        self.game_status = self.GameStatus.Playing

    def end_game(self):

        self.game_winners = []
        min_value = self.max_score
        for player in self.players_dict.values():

            if player.get_score() == min_value:
                self.game_winners.append(player.get_user_id())
            elif player.get_score() < min_value:
                self.game_winners = [player.get_user_id()]
                min_value = player.get_score()

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

    def call_last_card(self, client_id):
        
        if len(self.players_dict[client_id].get_cards_in_hand()) > 1:
            raise InvalidRequestException("More than 1 card left")
                
        # if client_id != current_player.client_id:
        #     raise InvalidRequestException("Wait for your turn")
        
        if client_id not in self.play_order_player_id_list:
            raise InvalidRequestException("Already blocked -- Too late now")
        elif client_id in self.safe_players:
            raise InvalidRequestException("Already safe")

        self.safe_players.append(client_id)

    def counter_last_card(self, caller_id) -> List[str]:
        """Counter players that have only one card left

        Returns:
            List[str]: List of players that have been countered
        """

        if caller_id not in self.players_dict:
            raise InvalidRequestException("Player does not exist")

        one_card_players = [ player.client_id for player in self.players_dict.values() 
                            if (len(player.get_cards_in_hand()) == 1) and 
                                (player.client_id not in (self.safe_players)) and
                                 (player.client_id in self.play_order_player_id_list)]
        
        if len(one_card_players) < 1 :
            raise InvalidRequestException("No counter to make")
        
        for player_id in one_card_players:
            self.play_order_player_id_list.remove(player_id)
            self.blocked_players.append(player_id)

        if len(self.play_order_player_id_list) == 0:
            # make caller win (can only be one winner)
            self.players_dict[caller_id].cards = []
            self.next_round()
        elif len(self.play_order_player_id_list) == 1:
            self.players_dict[self.play_order_player_id_list[0]].cards = []
            self.next_round()
        else:
            # Still enough players to play:
            if self.get_current_player().client_id in self.blocked_players:
                self.next_turn()

        return one_card_players


    def play_turn(self, client_id , hand_played: Hand = None, pass_turn: bool = False ):

        if self.game_status != self.GameStatus.Playing:
            raise InvalidRequestException("Not play phase")

        current_player = self.get_current_player()
        
        if client_id != current_player.client_id:
            raise InvalidRequestException("Not current player's turn")
        
        next_player = self.players_dict[self.play_order_player_id_list[self.get_next_player_idx()]]
        # pass
        if pass_turn:
            if self.previous_hand is None:
                raise InvalidRequestException("Cannot pass this turn")

            # Last player has only one card left -- Cannot pass 
            if (len(next_player.get_cards_in_hand()) == 1) and (self.previous_hand.hand_type == HandType.HIGH_CARD):
                playable_combs = get_playable_combinations(current_player.get_cards_in_hand(), self.previous_hand)
                if len([comb for comb in playable_combs if comb.hand_type == HandType.HIGH_CARD]) > 0:
                    raise InvalidRequestException("Next player has only one card left: You have to play your best card")

            self.consecutive_pass += 1

        else:
            if hand_played is None:
                raise InvalidRequestException("Cannot play null hand")
            
            if self.play_with_one_mult:
                # This hands has to be played with 1 mult
                if not hand_played.contains(Card("1", Suits.Multicolor)):
                    raise InvalidRequestException("First hand of the game has to contain Multicolored 1")
                self.play_with_one_mult = False


            # Check that next player has more than one card:
            if len(hand_played.get_card_list()) == 1 and (len(next_player.get_cards_in_hand()) == 1):
                # Check if player can play more than one card
                playable_combs = get_playable_combinations(current_player.get_cards_in_hand(), self.previous_hand)
                
                if len(playable_combs) > 0:
                    playable_combs = sorted(playable_combs, key=lambda x: (x.hand_type, x))
                    if self.previous_hand is None:
                        #Player can play anything
                        if playable_combs[-1] != hand_played:
                            # print("Could play:", playable_combs[-1])
                            raise InvalidRequestException("You have to play multiple cards or your best card")        
                    else:
                        best_hand = max(hand for hand in playable_combs if hand.hand_type == HandType.HIGH_CARD)
                        if hand_played != best_hand:
                            # print("Could play:", best_hand)
                            raise InvalidRequestException("You have to play multiple cards or your best card")
            
            # Check that combination can be played
            if self.previous_hand is not None:

                valid_hand = (hand_played.hand_type == HandType.GANG_OF_X) or (hand_played.get_hand_size() == self.previous_hand.get_hand_size()) 
                if not valid_hand:
                    raise InvalidRequestException(f"Hand is not of correct type - Need {self.previous_hand.get_hand_size()} cards")
                if hand_played <= self.previous_hand:
                    raise InvalidRequestException("Hand is not stronger that previous one")
                
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
                player.client_id: {"nb_cards": player.nb_cards_in_hand(),
                                   "score": player.get_score(),
                                    "blocked": (player.client_id in self.blocked_players),
                                    "safe": (player.client_id in self.safe_players) } 
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
            status_dict["score_history"] = {
                player.client_id: player.get_score_history() for player in self.players_dict.values()
            }

        if self.game_status == self.GameStatus.GameEnd:
            status_dict["game_winners"] = self.game_winners
            status_dict["score_history"] = {
                player.client_id: player.get_score_history() for player in self.players_dict.values()
            }

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
        return f"Game with {len(self.players_dict)} players, Round: {self.current_round}"