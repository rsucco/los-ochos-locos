from card import Card
import random


class Deck:
    def __init__(self, cards=None):
        if cards is not None:
            self.cards = cards
        else:
            # Instantiate a standard 52-card deck
            self.cards = []
            for num_rank in range(1, 14):
                for suit in ['c', 's', 'h', 'd']:
                    card = Card(num_rank, suit)
                    self.cards.append(card)

    def __len__(self):
        return len(self.cards)

    # Shuffle the deck
    def shuffle(self):
        random.shuffle(self.cards)

    # Deal four hands with seven cards each
    def deal_hands(self):
        hands = [self.cards[0:28:4], self.cards[1:28:4], self.cards[2:28:4], self.cards[3:28:4]]
        self.cards = self.cards[28:]
        return hands

    # Take a card from the top of a pile (pop from the stack)
    def draw_card(self):
        return self.cards.pop(0)

    # Add a card to the top of a pile (push to the stack)
    def add_card(self, card):
        self.cards.insert(0, card)