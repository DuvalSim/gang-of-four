from typing import List
from deck import Card
import copy

class Player:

    def __init__(self, client_id) -> None:
        self.client_id = client_id
        self.cards = List[Card]

    def add_cards(self, cards: List[Card]):
        self.cards += cards

    def reset_hand(self):
        self.cards = []

    def play_hand(self, hand_played: List[Card]):
        if any([card not in self.cards for card in hand_played]):
            raise ValueError("Some cards not in hand")
        
        current_player_hand = self.cards.copy()

        # check if no value error
        for card in hand_played:
            current_player_hand.remove(card)

        self.cards = current_player_hand

    def get_cards_in_hand(self) -> List[Card]:
        return copy.deepcopy(self.cards)
    
    def nb_cards_in_hand(self) -> int:
        return len(self.cards)

    def __eq__(self, other):
        return self.client_id == other.client_id