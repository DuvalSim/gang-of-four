from typing import List
from deck import Card
import copy

class Player:

    def __init__(self, client_id, username = None) -> None:
        self.client_id = client_id
        self.username = username
        self.cards : List[Card] = []
        self.score_history: dict[int] = {}
        self.score = 0
        self.is_active = True

    def get_user_id(self) -> str:
        return self.client_id

    def score_round(self, round:int, score: int):
        self.score_history[round] = score
        self.score += score

    def get_score(self) -> int:
        return self.score
    
    def get_score_history(self) -> dict[int]:
        return self.score_history

    def set_active(self, is_active):
        self.is_active = is_active

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
            raise ValueError("Some cards not in player hand")
        self.cards = current_player_hand

    def get_cards_in_hand(self) -> List[Card]:
        return copy.deepcopy(self.cards)
    
    def nb_cards_in_hand(self) -> int:
        return len(self.cards)
    
    def sort_cards(self, sort_method: str) -> List[int]:
        """Sort player cards according to sort method and returns the sorted order

        Args:
            sort_method (rank | color) 

        Returns:
            List[int]: argsort result
        """
        if sort_method == "rank":
            sorted_order = sorted(range(len(self.cards)), key=self.cards.__getitem__)
        else:
            # By color first then rank
            sorted_order = sorted(range(len(self.cards)), key=lambda i : (self.cards[i].suit, self.cards[i].get_rank_value() ))

        self.cards = [self.cards[i] for i in sorted_order]

        return sorted_order
    
    def get_status(self):
        return {"cards": [str(card) for card in self.get_cards_in_hand()]}
    
    def get_public_info(self):
        return {"user_id": self.client_id, "username": self.username, "active":self.is_active}
    
    def get_best_card(self) -> Card:
        return max(self.cards)
    
    def get_worst_card(self):
        return min(self.cards)

    def __eq__(self, other):
        return self.client_id == other.client_id