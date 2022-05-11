from os import name, system

from colorama import Fore, Style, init

from card import Card
from deck import Deck
from message import Message
from player import AIPlayer, HumanPlayer


class Game:
    def __init__(self, num_human_players=1, debug=False):
        # Initialize colorama to enable styled terminal output on Windows
        init()
        self.num_human_players = num_human_players
        self.players = []
        for i in range(4):
            if i < num_human_players:
                self.players.append(HumanPlayer(i))
            else:
                self.players.append(AIPlayer(i, verbose=debug))
        self.debug = debug
        self.messages = [Message()]
        self.draw = Deck()
        self.discard = Deck([])
        self.player_up = 0
        self.secret = False

    # Clear the screen with the appropriate terminal command for the system
    def clear(self):
        # Don't clear the screen in debug mode. This helps with debugging because it enables scrollback to see snapshots of game state change
        if not self.debug:
            if name == 'nt':
                system('cls')
            else:
                system('clear')

    # Renders a list of Message objects inside in a nice little box
    def render_ui_messages(self, messages, render_strs=[''] * 9, width=80, margin_left=10):
        render_strs = [render_str + ' ' * margin_left for render_str in render_strs]
        render_strs[0] += '╓' + '─' * width + '╖'
        for i, message in enumerate(messages, start=1):
            render_strs[i] += '║ ' + message.ljust(width) + ' ║'
        for i in range(len(messages) + 1, 8):
            render_strs[i] += '║' + ' ' * width + '║'
        render_strs[8] += '╙' + '─' * width + '╜'
        return render_strs

    # Render a player's hand with cards if they're up and *'s if they're not
    def render_ui_hand(self, player, render_strs=[''] * 5, width=25, margin_left=10):
        padded_hand = []
        hand = sorted([card for card in self.players[player].hand], key=lambda x: x.num_rank)
        if len(hand) > 12:
            half_cards = int(len(hand) / 2)
        else:
            half_cards = len(hand)
        if half_cards > 12:
            half_cards = 12
        render_strs[0] += ' ' * margin_left + '╓' + '─' * width + '╖'
        # Show the hand if the current player up is human, or if it's player 1's hand in a 1-player game, or in debug mode
        if (player == self.player_up and not self.secret) or \
            (player == 0 and self.num_human_players == 1) or self.debug:
            render_strs[1] += ' ' * margin_left + '║' + \
                'Your hand:'.center(width) + '║'
            padded_hand.append(Message(''.join(str(card) for card in hand[:half_cards])))
            padded_hand.append(Message(''.join(str(card) for card in hand[half_cards:24])))
        # Show asterisks for each card in the hand if it belongs to an opponent
        else:
            render_strs[1] += ' ' * margin_left + '║' + \
                f'Player {player + 1}\'s hand:'.center(width) + '║'
            padded_hand.append(Message('* ' * len(hand[:half_cards])))
            padded_hand.append(Message('* ' * len(hand[half_cards:24])))

        render_strs[2] += ' ' * margin_left + '║' + \
            padded_hand[0].center(width) + '║'
        render_strs[3] += ' ' * margin_left + '║' + \
            padded_hand[1].center(width) + '║'
        render_strs[4] += ' ' * margin_left + '╙' + '─' * width + '╜'
        return render_strs

    # Render the draw and the discard piles
    def render_ui_piles(self, margin_left=5):
        render_strs = [' ' * margin_left] * 9
        render_strs[0] += '╓─────────────╖'
        render_strs[1] += '║ Dicard Pile ║'
        render_strs[2] += '║' + \
            Message(str(self.discard.cards[0])).center(13) + '║'
        render_strs[3] += '╙─────────────╜'
        render_strs[4] += '               '
        render_strs[5] += '╓─────────────╖'
        render_strs[6] += '║  Draw Pile  ║'
        render_strs[7] += '║' + \
            Message(' (' + str(len(self.draw)) + ' cards)').center(13) + '║'
        render_strs[8] += '╙─────────────╜'
        return render_strs

    # Can be used directly or passed as a callback to player objects so they can write to the UI
    def set_message(self, *messages, **kwargs):
        # If the replace_line argument is passed, use it
        try:
            if kwargs['replace_line']:
                replace_line = kwargs['replace_line']
            else:
                replace_line = -1
        # If the kwarg wasn't included, make it -1 to ignore
        except Exception:
            replace_line = -1
        messages_list = list(Message(message) for message in messages)
        if replace_line > -1:
            while len(self.messages) <= replace_line:
                self.messages.append(Message(''))
            self.messages[replace_line] = messages_list[0]
        else:
            self.messages = messages_list
        self.draw_game()

    # Draw the visual elements
    def draw_game(self):
        self.clear()
        # Helper method to print out a list of strings
        def render(render_strs):
            for render_str in render_strs:
                print(render_str)

        # Draw titlebar
        print(' ' * 40, '╓───────────────────────────────────────────────────────╖')
        print(' ' * 40, f'║                  {Style.BRIGHT}{Fore.GREEN}¡Los {Fore.LIGHTRED_EX}Ochos {Fore.WHITE}Locos!{Style.RESET_ALL}                    ║')
        print(' ' * 40, '╙───────────────────────────────────────────────────────╜')

        # Render the players' hands
        render_strs = [''] * 5
        render_strs = self.render_ui_hand(0, render_strs, margin_left=0)
        for player in range(1,4):
            render_strs = self.render_ui_hand(player, render_strs)
        render(render_strs)
        print()

        # Render the card piles and the gameplay messages side by side
        render(self.render_ui_messages(self.messages, self.render_ui_piles(), 103, 10))
        print()

        if self.debug:
            print('========================================================================')
            print('DRAW:')
            print(''.join(str(card) for card in self.draw.cards))
            print('DISCARD:')
            print(''.join(str(card) for card in self.discard.cards))
            for i in range(4):
                print('PLAYER', i + 1, 'HAND:')
                print(''.join(str(card) for card in self.players[i].hand))
    

    # Callback for the players to claim victory
    def player_victory(self, player_num):
        self.secret = True
        self.set_message(f'{Style.BRIGHT}Player {player_num + 1} wins!!!{Style.RESET_ALL}')
        input()
        exit()

    # Deal hands to players
    def deal_hands(self):
        self.draw.shuffle()
        hands = self.draw.deal_hands()
        for i, hand in enumerate(hands):
            self.players[i].hand = hand

    # Increment/rollover the player_up variable and prevent peeking betwixt human players
    def next_player(self):
        last_player_up = self.player_up
        self.player_up += 1
        if self.player_up == 4:
            self.player_up = 0
        if self.num_human_players > 1 and self.players[self.player_up].is_human:
            self.secret = True
            self.set_message(*[f'Player {min(last_player_up + 1, self.num_human_players)}, quit peeking!',
                                f'Player {self.player_up + 1}, you\'re up!',
                                'Press enter when ready...'])
            input()
            self.secret = False

    # Core game loop
    def play(self):
        # Start a game by dealing the hands and placing one card face-up in the discard pile
        self.deal_hands()
        self.discard.add_card(self.draw.draw_card())
        # Keep going until a player runs out of cards
        while all(len(player.hand) > 0 for player in self.players):
            # Check if player can play
            if self.players[self.player_up].can_play(self.discard.cards[0]):
                self.set_message(f'{Style.BRIGHT}Player {self.player_up + 1}, you\'re up!{Style.RESET_ALL}',
                                    'Choose a card to play. You can use the numbers 2-10, as well as letters A, J, Q, and K.',
                                    f'You can include the first letter of the suit: {Card.SPADES}, {Card.HEARTS}, {Card.CLUBS}, or {Card.DIAMONDS}.',
                                    '',
                                    f'Playable cards: ' + ''.join(str(card) for card in self.players[self.player_up].playable_cards(self.discard.cards[0])))
                self.discard.add_card(self.players[self.player_up].play_card(self.set_message, self.discard.cards[0]))
                if not self.players[self.player_up].is_human:
                    self.secret = True
                    self.set_message(f'Player {self.player_up + 1} plays {str(self.discard.cards[0])}.',
                                        'Press enter to continue...')
                    input()
                    self.secret = False
                # ¡¡¡Los ochos son muy locos!!!
                if self.discard.cards[0].num_rank == 8:
                    self.discard.cards[0].suit = self.players[self.player_up].choose_suit(self.set_message)
                    self.secret = True
                    self.set_message(f'Player {self.player_up + 1} chooses {self.discard.cards[0].get_suit()} as the new suit!',
                                        'Press enter to continue...')
                    self.secret = False
                    input()
            # If the player can't play, then draw until they can
            else:
                if self.players[self.player_up].is_human:
                    self.set_message(f'{Style.BRIGHT}No cards can play.{Style.RESET_ALL} Press enter to draw.')
                    input()
                cards_drawn = 0
                while True:
                    # Make sure there are cards available to draw
                    if len(self.draw.cards) > 0:
                        new_card = self.draw.draw_card()
                        cards_drawn += 1
                        if new_card.plays_on(self.discard.cards[0]):
                            self.discard.add_card(new_card)
                            self.secret = True
                            if cards_drawn > 1:
                                card_or_cards = 'cards'
                            else:
                                card_or_cards = 'card'
                            self.set_message(f'Player {self.player_up + 1} draws a total of {cards_drawn} {card_or_cards} and plays a {str(new_card)}.',
                                                'Press enter to continue...')
                            input()
                            if self.discard.cards[0].num_rank == 8:
                                self.discard.cards[0].suit = self.players[self.player_up].choose_suit(self.set_message)
                                self.secret = True
                                self.set_message(f'Player {self.player_up + 1} chooses {self.discard.cards[0].get_suit()} as the new suit!',
                                                    'Press enter to continue...')
                                self.secret = False
                                input()
                            self.secret = False
                            break
                        else:
                            self.players[self.player_up].hand.append(new_card)
                            if self.players[self.player_up].is_human:
                                self.set_message(f'You draw {str(new_card)}. Press enter to draw again.')
                                input()

                    else:
                        # Shuffle the discard pile (sans the top card) and turn it into the draw pile if the draw pile is empty
                        if not self.players[self.player_up].is_human:
                            self.secret = True
                        self.set_message('Shuffling deck. Press enter to continue...')
                        input()
                        self.secret = False
                        self.draw = Deck(self.discard.cards[1:])
                        self.draw.shuffle()
                        self.discard.cards = [self.discard.cards[0]]
            # Rotate to the next player
            self.next_player()
            
        # Looks like somebody won!
        self.player_victory(self.player_up - 1)
            