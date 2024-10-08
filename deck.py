from typing import List
from enum import Enum
import random

from collections import Counter

class Suits(Enum):
        
        Green = 0,
        Yellow = 1,
        Red = 2,
        Multicolor = 3

        def __str__(self):
            return self.name
        
class CombinationType(Enum):
    HIGH_CARD = 0
    PAIR = 1
    TWO_PAIRS = 2
    THREE_OF_A_KIND = 3
    STRAIGHT = 3
    FLUSH = 4
    FULL_HOUSE = 5
    STRAIGHT_FLUSH = 6
    GANG_OF_X = 7

 
SUITS = [Suits.Red,Suits.Yellow, Suits.Green]

class Card:

    ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 'Phoenix', 'Dragon']

    def __init__(self, rank: str, suit: Suits) -> None:

        if rank not in Card.ranks:
            raise ValueError(f"No such rank [{rank}]")
        if suit == Suits.Multicolor and rank != "1":
            raise ValueError(f"Card [{rank}] cannot be multicolor")
        if rank == 'Phoenix' and suit not in (Suits.Green, Suits.Yellow):
            raise ValueError(f"Phoenix can only be yellow or green")
        
        self.rank = rank
        self.suit = suit
        self.is_poulet = self.rank in ("Phoenix", 'Dragon')


    def __eq__(self, value: object) -> bool:
        return (self.rank == value.rank) and (self.suit == value.suit)
    
    def __lt__(self, other:object) -> bool:
        rank_a_idx = Card.ranks.index(self.rank)
        rank_b_idx = Card.ranks.index(other.rank)
        return (rank_a_idx < rank_b_idx) or ((rank_b_idx == rank_b_idx) and (self.suit < other.suit))
        
    
    def __str__(self) -> str:
        return f"{self.rank}-{str(self.suit)[0]}"

class Deck:


    def __init__(self) -> None:
        self.suits = [Suits.RED,Suits.YELLOW, Suits.GREEN]
        self.ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.special_cards = [('1', Suits.MULTI), ('Phoenix', Suits.GREEN),
                              ('Phoenix', Suits.YELLOW), ('Dragon', Suits.RED)]
        
        self.deck = self.__create_deck()

    def __create_deck(self) -> List[Card]:
        """Create a complete deck"""
        card_list = [Card(rank=rank, suit=suit) for suit in self.suits for rank in self.ranks]
        card_list += [Card(rank=rank, suit=suit) for suit in self.suits for rank in self.ranks]
        card_list += [Card(rank=rank, suit=suit) for rank,suit in self.special_cards]

        return card_list
    
    def shuffle(self):        
        random.shuffle(self.deck)

    def nb_cards(self):
        return len(self.deck)
    
    def deal_card(self, nb_card:int) -> List[Card]:
        if nb_card > self.nb_cards():
            raise ValueError("Not enought cards remaining")
        return [self.deck.pop() for _ in range(nb_card)]
    
class Hand:
    # rank_order = '12345678910PhoenixDragon'
    rank_order = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", 'Phoenix', 'Dragon']

    def __init__(self, cards: List[Card]):
        self.cards = sorted(cards)
        self.has_poulet = any(card.is_poulet for card in self.cards)
        self.ranks = [card.rank for card in self.cards]
        self.suits = [card.suit for card in self.cards]

        self.combination = self.check_valid_combination()

        if self.combination is None:
            raise ValueError("Not a valid hand")


    def check_valid_five_combination(self):
        if any([card.is_poulet() for card in self.cards]):
            return False
        else:
            return len(self.cards) == 5
        
    def is_flush(self):
        """Check if all cards have the same suit."""
        suits = self.suits.copy()
        # multicolor works as any color
        suits.remove(Suits.Multicolor)

        return (len(set(suits)) == 1) and self.check_valid_five_combination()

    def is_straight(self):
        """Check if the cards form a sequence."""
        if not self.check_valid_five_combination():
            return False
        int_ranks = [int(rank) for rank in self.ranks]
        return (int_ranks == list(range(int_ranks[0], int_ranks[0] + 4)))

    def is_gank_of_x(self):
        """Check if there are four cards of the same rank."""
        return (len(self.cards) >= 4 and len(set(self.ranks)) == 1)
    

    def is_full_house(self):
        """Check for a full house (three of a kind and a pair)."""
        if not self.check_valid_five_combination:
            return False
        
        rank_counts = Counter(self.ranks)
        return sorted(rank_counts.values()) == [2, 3]

    def is_three_of_a_kind(self):
        """Check if there are three cards of the same rank."""
        
        rank_counts = Counter(self.ranks)
        return list(rank_counts.values()) == [3]

    def is_two_pair(self):
        """Check if there are two pairs."""

        rank_counts = Counter(self.ranks)
        return list(rank_counts.values()) == [2,2]

    def is_one_pair(self):
        """Check if there is one pair."""
        rank_counts = Counter(self.ranks)
        return list(rank_counts.values()) == [2]
    
    def is_high_card(self):
        return len(self.cards) == 1

    def check_valid_combination(self) -> CombinationType:
        if self.is_gank_of_x():
            return CombinationType.GANG_OF_X
        
        if self.is_flush() and self.is_straight():
            return CombinationType.STRAIGHT_FLUSH
        
        if self.is_full_house():
            return CombinationType.FULL_HOUSE
        
        if self.is_flush():
            return CombinationType.FLUSH

        if self.is_straight():
            return CombinationType.STRAIGHT

        if self.is_three_of_a_kind():
            return CombinationType.THREE_OF_A_KIND
    
        if self.is_two_pair():
            return CombinationType.TWO_PAIRS
    
        if self.is_one_pair():
            return CombinationType.PAIR

        if self.is_high_card():
            return CombinationType.HIGH_CARD
        
        return None
    
    def __eq__(self, other):
        """Equality comparison between two hands."""
        # gang of four 
        if self.combination == other.combination:
            if self.combination == CombinationType.GANG_OF_X:
                return self.ranks == other.ranks
            
            if self.is_straight():
                return (self.suits[0] == other.suits[0])
        else:
            return False
        return self._combination_rank() == other._combination_rank() and self.cards == other.cards

    def __lt__(self, other):
        """Less than comparison between two hands."""
        if self._combination_rank() != other._combination_rank():
            return self._combination_rank() < other._combination_rank()
        # If the combination ranks are equal, compare individual cards
        for self_card, other_card in zip(reversed(self.cards), reversed(other.cards)):
            if self_card != other_card:
                return self_card < other_card
        return False
    
    
