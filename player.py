from card import Card
from colorama import Style


# Base Player class
class Player:
    def __init__(self, player_num):
        self.player_num = player_num
        self.hand = []

    def can_play(self, other_card):
        return any(card.plays_on(other_card) for card in self.hand)

    def playable_cards(self, other_card):
        return sorted([card for card in self.hand if card.plays_on(other_card)], key=lambda x: x.num_rank)

# Class for human player
class HumanPlayer(Player):
    def __init__(self, player_num):
        super().__init__(player_num)
        self.is_human = True

    # Parse input to determine play choice
    # Returns the Card object in question and removes it from its hand
    def play_card(self, set_message, card_up):
        # Filtering constants
        VALID_CHARS = ['2', '3', '4', '5', '6', '7',
                    '8', '9', 't', 'j', 'q', 'k', 'a', 'h', 's', 'd', 'c']
        SUIT_CHARS = ['s', 'h', 'c', 'd']

        # Get numerical rank of text input so we can create a Card object
        def get_num_rank(rank):
            if rank == 'a':
                return 1
            elif rank == 't':
                return 10
            elif rank == 'j':
                return 11
            elif rank == 'q':
                return 12
            elif rank == 'k':
                return 13
            else:
                return int(rank)

        # If a char is a valid suit, return it. Otherwise, return the default suit value of '0'
        def get_suit(check_suit):
            if check_suit in SUIT_CHARS:
                return check_suit
            else:
                return '0'

        # Get the card
        while True:
            num_rank = 0
            suit = '0'
            try:
                # Convert 10's to t's, 1's to a's, and uppercase to lowercase. Anything valid will be matched to VALID_CHARS
                discard_input = [char for char in input().lower().replace('10', 't').replace('1', 'a')
                                if char in VALID_CHARS]
                num_rank = get_num_rank(discard_input[0])
                suit = get_suit(discard_input[-1])
                for card in self.playable_cards(card_up):
                    # Rank needs to match. Suit only needs to match if specified
                    if num_rank == card.num_rank and (suit == '0' or suit == card.suit):
                        self.hand.remove(card)
                        return card
                # Card wasn't in playable_cards, do error handling
                for card in self.hand:
                    # If the card is in the hand but not playable, say so
                    if num_rank == card.num_rank and (suit == '0' or suit == card.suit):
                        raise ValueError(' is not playable.')
                    # If the card is fundamentally a lie, say so
                    else:
                        raise ValueError(' does not exist in hand.')
            # Handle the player typing in a card that doesn't exist or can't be played
            except ValueError as ve:
                set_message(str(Card(num_rank, suit)) + str(ve), replace_line=6)
            # Handle the player not typing in anything useful at all
            except IndexError:
                set_message('You must enter a card to play.', replace_line=6)        

    def choose_suit(self, set_message):
        while True:
            try:
                set_message(f'Select a new suit: {Card.SPADES}, {Card.HEARTS}, {Card.CLUBS}, or {Card.DIAMONDS}.')
                suit_input = input().lower()[0]
                if suit_input in ['c', 'd', 'h', 's']:
                    return suit_input
                else:
                    raise Exception
            except Exception:
                set_message(f'{Style.BRIGHT}Invalid input.{Style.RESET_ALL} Enter one of the following: c, d, h, or s.', replace_line=1)
            

# Class for AI player
class AIPlayer(Player):
    def __init__(self, player_num, **kwargs):
        super().__init__(player_num)
        self.verbose = kwargs['verbose']
        self.known_cards = []
        self.is_human = False

    def print_message(self, *message):
        if self.verbose:
            print(*message)

    def play_card(self, set_message, card_up):
        playable_cards = self.playable_cards(card_up)
        if len(playable_cards) > 1:
            # Try to avoid wasting an 8 if possible
            for card in playable_cards:
                if card.num_rank != 8:
                    self.hand.remove(card)
                    return card
        # If there's only one option (or all options or 8's), take it
        self.hand.remove(playable_cards[0])
        return playable_cards[0]

    def choose_suit(self, set_message):
        suit_counts = {'c': 0, 'd': 0, 'h': 0, 's': 0}
        for card in self.hand:
            suit_counts[card.suit] += 1
        return max(suit_counts, key=suit_counts.get)