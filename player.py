from typing import List
from deck import Card
import copy

class Player:

    def __init__(self, client_id) -> None:
        self.client_id = client_id
        self.cards = List[Card]

    def add_cards(self, cards: List[Card]):
        self.cards += cards

    def remove_card(self, card: Card):
        try:
            self.cards.remove(card)
        except ValueError as e:
            raise ValueError("Card not in hand")
    def reset_hand(self):
        self.cards = []

    def play_hand(self, cards_played: List[Card]):
                
        current_player_hand = self.cards.copy()
        # check if no value error
        try: 
            for card in cards_played:
                current_player_hand.remove(card)
        except Exception:
            raise ValueError("Some cards not in player hand hand")
        self.cards = current_player_hand

    def get_cards_in_hand(self) -> List[Card]:
        return copy.deepcopy(self.cards)
    
    def nb_cards_in_hand(self) -> int:
        return len(self.cards)
    
    def get_status(self):
        return {"cards": [str(card) for card in self.get_cards_in_hand()]}
    
    def get_best_card(self) -> Card:
        return max(self.cards)
    
    def get_worst_card(self):
        return min(self.cards)

    def __eq__(self, other):
        return self.client_id == other.client_id