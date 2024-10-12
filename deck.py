from typing import List
from enum import Enum, IntEnum
import random

from collections import Counter

class Suits(IntEnum):
        
        Green = 0,
        Yellow = 1,
        Red = 2,
        Multicolor = 3

        def __str__(self):
            return self.name
        
class HandType(IntEnum):
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

    @staticmethod
    def build_from_str(card_str :str):
        suit_dict = {"G": Suits.Green, "Y": Suits.Yellow, "R": Suits.Red, "M": Suits.Multicolor}
        rank, suit = card_str.split("-")
        suit = suit_dict[suit]
        return Card(rank, suit)
    
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
        return (rank_a_idx < rank_b_idx) or ((rank_a_idx == rank_b_idx) and (self.suit < other.suit))
    
    def __le__(self, other) -> bool:
        return self.__lt__(other) or self.__eq__(other)
        
    
    def __str__(self) -> str:
        return f"{self.rank}-{str(self.suit)[0]}"
    
    def __repr__(self) -> str:
        return f"{self.rank}-{str(self.suit)[0]}"

class Deck:


    def __init__(self) -> None:
        self.suits = [Suits.Red,Suits.Yellow, Suits.Green]
        self.ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        self.special_cards = [('1', Suits.Multicolor), ('Phoenix', Suits.Green),
                              ('Phoenix', Suits.Yellow), ('Dragon', Suits.Red)]
        
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

    @staticmethod
    def build_from_str(card_str_list: List[str]):
        result_card_list : List[Card] = []
        for card_str in card_str_list:
            result_card_list.append(Card.build_from_str(card_str))

        return Hand(result_card_list)
    
    def __init__(self, cards: List[Card]):
        
        self.cards = sorted(cards)
        self.has_poulet = any(card.is_poulet for card in self.cards)
        self.ranks = [card.rank for card in self.cards]
        self.suits = [card.suit for card in self.cards]

        self.hand_type = self.calculate_hand_type()

        if self.hand_type is None:
            raise ValueError("Not a valid hand")
        
    def contains(self, card: Card):
        return card in self.cards

    def get_hand_size(self) -> int:
        return len(self.cards)
    
    def get_card_list(self) -> List[Card]:
        return self.cards.copy()
    
    def get_str_card_list(self):
        return [str(card) for card in self.cards]

    def check_valid_five_combination(self):
        
        if self.has_poulet:
            return False
        else:
            return len(self.cards) == 5
        
    def is_flush(self):
        """Check if all cards have the same suit."""
        suits = self.suits.copy()
        # multicolor works as any color
        if Suits.Multicolor in suits:
            suits.remove(Suits.Multicolor)

        return (len(set(suits)) == 1) and self.check_valid_five_combination()

    def is_straight(self):
        """Check if the cards form a sequence."""
        if not self.check_valid_five_combination():
            return False
        int_ranks = [int(rank) for rank in self.ranks]
        return (int_ranks == list(range(int_ranks[0], int_ranks[0] + 5)))

    def is_gank_of_x(self):
        """Check if there are four cards of the same rank."""
        return (len(self.cards) >= 4 and len(set(self.ranks)) == 1)
    

    def is_full_house(self):
        """Check for a full house (three of a kind and a pair)."""
        if not len(self.cards) == 5:
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

    def calculate_hand_type(self) -> HandType:
        if self.is_gank_of_x():
            return HandType.GANG_OF_X
        
        if self.is_flush() and self.is_straight():
            return HandType.STRAIGHT_FLUSH
        
        if self.is_full_house():
            return HandType.FULL_HOUSE
        
        if self.is_flush():
            return HandType.FLUSH

        if self.is_straight():
            return HandType.STRAIGHT

        if self.is_three_of_a_kind():
            return HandType.THREE_OF_A_KIND
    
        if self.is_two_pair():
            return HandType.TWO_PAIRS
    
        if self.is_one_pair():
            return HandType.PAIR

        if self.is_high_card():
            return HandType.HIGH_CARD
        
        return None
    
    def __eq__(self, other):
        """Equality comparison between two hands."""
        return self.cards == other.cards

    def __lt__(self, other: object):
        """Less than comparison between two hands."""
        if type(other) != Hand:
            raise ValueError(f"Cannot compare Hand and [{type(other)}]")
     
        if (self.get_hand_size() != other.get_hand_size()) and not (HandType.GANG_OF_X in [self.hand_type, other.hand_type]):
            raise ValueError(f"Cannot compare hands of different lenghts")

        
        if self.hand_type < other.hand_type:
            return True
        
        elif self.hand_type == other.hand_type:

            if self.hand_type == HandType.GANG_OF_X:
                if self.get_hand_size() != other.get_hand_size():
                    # Gang of 5 < Gang of 6 
                    return self.get_hand_size() < other.get_hand_size()
                else:
                    # Check rank of cards
                    return self.cards[0] < other.cards[0]
                
            # Hands have same number of cards
            for self_card, other_card in zip(*map(reversed, (self.cards, other.cards))):
                if self_card != other_card:
                    return (self_card < other_card)
            
            # All cards are equal
        return False
    
    def __le__(self, other):
        return (self.__lt__(other) or self.__eq__(other))
