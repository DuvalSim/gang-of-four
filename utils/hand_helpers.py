from itertools import combinations
from collections.abc import Iterable
from collections import Counter
from deck import Hand, Card, Suits, HandType
from typing import List

def get_pairs(card_list: Iterable[Card]) -> set[Hand]:
    pairs = set()
    value_counter = Counter(card.get_rank_value() for card in card_list)
    for value, count in value_counter.items():
        if count >= 2:
            relevent_cards = [card for card in card_list if card.get_rank_value() == value]
            pairs.update(Hand(comb) for comb in combinations(relevent_cards, 2))
    return pairs

def get_three_of_a_kinds(card_list : Iterable[Card]) -> set[Hand]:
    triplets = set()
    value_counter = Counter(card.get_rank_value() for card in card_list)
    for value, count in value_counter.items():
        if count >= 3:
            relevent_cards = [card for card in card_list if card.get_rank_value() == value]
            triplets.update(Hand(comb) for comb in combinations(relevent_cards, 3))
    return triplets

def get_gang_of_x(card_list: Iterable[Card]) -> set[Hand]:
    gang_of_x_list = set()
    value_counter = Counter(card.get_rank_value() for card in card_list)
    for value, count in value_counter.items():
        if count >=4:
            relevent_cards = [card for card in card_list if card.get_rank_value() == value]
            for x in range(4, count + 1):
                gang_of_x_list.update(Hand(comb) for comb in combinations(relevent_cards, x))

    return gang_of_x_list

def get_two_pairs(card_list : Iterable[Card]) -> set[Hand]:
    pairs = get_pairs(card_list)

    two_pairs = set()
    pairs = [pair.get_card_list() for pair in pairs]
    for first_pair_idx in range(len(pairs) -1):
        for second_pair_idx in range(first_pair_idx, len(pairs)):
            first_pair = pairs[first_pair_idx]
            second_pair = pairs[second_pair_idx]
            if first_pair[0].get_rank_value() != second_pair[0].get_rank_value():
                two_pairs.update([Hand(first_pair + second_pair)])
    return two_pairs

def get_full_houses(card_list: Iterable[Card]) -> set[Hand]:
    # value_counter = Counter(card.get_rank_value() for card in card_list)
    pairs = get_pairs(card_list)
    three_of_a_kinds = get_three_of_a_kinds(card_list)    

    full_house_list = set()
    for pair in pairs:
        pair = pair.get_card_list()
        for three_of_a_kind in three_of_a_kinds:
            three_of_a_kind = three_of_a_kind.get_card_list()
            if pair[0].get_rank_value() != three_of_a_kind[0].get_rank_value():
                full_house_list.update([Hand(pair + three_of_a_kind)])

    return full_house_list

def get_flushes(card_list: Iterable[Card]) -> set[Hand]:
    flushes = set()
    card_list = [card for card in card_list if not card.is_poulet]
    suit_counter = Counter(card.suit for card in card_list)
    for suit, count in suit_counter.items():
        if (count + suit_counter[Suits.Multicolor] >=5):
            relevent_cards = (card for card in card_list if card.suit in (suit, Suits.Multicolor))
            flushes.update(Hand(comb) for comb in combinations(relevent_cards, 5))
    return flushes


def get_straights(card_list: Iterable[Card]) -> set[Hand]:

    card_list = [card for card in card_list if not card.is_poulet]
    value_counter = Counter(card.get_rank_value() for card in card_list)
    values = sorted(value_counter.keys())

    straight_set = set()
    
    for key_idx in range(len(values) -4):
        start_value = values[key_idx]
        end_value = values[key_idx + 4]

        if  start_value == end_value - 4:
            # There is a straight
            new_straights = [[]]
                
            for rank_value in range(start_value, end_value + 1):
                
                rank_cards = list(set(card for card in card_list if card.get_rank_value() == rank_value))

                nb_cards_to_add = len(rank_cards)
                # Add nb_new_cards - 1 list to to the list of straights to cover all possibilities
                new_straights = [straight.copy() for straight in new_straights for _ in range(nb_cards_to_add)]

                for straight_idx in range(len(new_straights)):

                    card_to_add = rank_cards[straight_idx % (nb_cards_to_add) if (nb_cards_to_add >= 1) else 0]

                    new_straights[straight_idx].append(card_to_add)


            straight_set.update(Hand(straight) for straight in new_straights)
    
    return straight_set


def get_playable_combinations(card_list : Iterable[Card], last_hand:Hand) -> List[Hand]:
    possible_combinations: set[Hand] = set() # Set of Hands objects
    
    # SINGLE CARD
    if last_hand is None or last_hand.hand_type == HandType.HIGH_CARD:
        possible_combinations.update([Hand([card]) for card in card_list])
    
    if last_hand is None or last_hand.hand_type == HandType.PAIR:
        possible_combinations.update(get_pairs(card_list))

    if last_hand is None or last_hand.hand_type == HandType.THREE_OF_A_KIND:
        possible_combinations.update(get_three_of_a_kinds(card_list))
    
    # Gang Of Fours:
    possible_combinations.update(get_gang_of_x(card_list))
    
    # Two pairs
    if last_hand is None or (last_hand.hand_type == HandType.TWO_PAIRS):
        possible_combinations.update(get_two_pairs(card_list))

    if last_hand is None or (last_hand.hand_type in (HandType.FLUSH, HandType.STRAIGHT, HandType.FULL_HOUSE)):
        possible_combinations.update(get_full_houses(card_list))

    # Flushes (includes straight flushes)
    if last_hand is None or (last_hand.hand_type in (HandType.FLUSH, HandType.STRAIGHT, HandType.FULL_HOUSE, HandType.STRAIGHT_FLUSH)):
        possible_combinations.update(get_flushes(card_list))

    # Straight (straight flushes already included)
    if last_hand is None or (last_hand.hand_type == HandType.STRAIGHT):
        straight_set = get_straights(card_list)
        possible_combinations.update(straight_set)
        
    
    return [hand for hand in possible_combinations if hand.valid_to_play(last_hand)]

def argsort_cards(card_list: List[Card], sort_method: str) -> List[int]:
    if sort_method == "rank":
        sorted_order = sorted(range(len(card_list)), key=card_list.__getitem__)
    else:
        # By color first then rank
        sorted_order = sorted(range(len(card_list)), key=lambda i : (card_list[i].suit, card_list[i].get_rank_value()))

    return sorted_order