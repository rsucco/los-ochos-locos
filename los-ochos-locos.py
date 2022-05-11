#!/usr/bin/env python3

import sys
import argparse
from game import Game
from pyfiglet import Figlet
from colorama import Style, Fore
from os import name, system


def print_welcome():
    if name == 'nt':
        system('cls')
    else:
        system('clear')
    f = Figlet(font='alligator', width=120)
    print(Style.BRIGHT + Fore.LIGHTRED_EX +
          '\n' + '-' * 110 + '\n' + Style.RESET_ALL)
    print(f'{Style.BRIGHT}{Fore.GREEN}{f.renderText("      L   O S")}{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.LIGHTRED_EX}{f.renderText("            O C H O S")}{Style.RESET_ALL}')
    print(f'{Style.BRIGHT}{Fore.WHITE}{f.renderText("                     L     O C O S")}{Style.RESET_ALL}')
    print(Style.BRIGHT + Fore.LIGHTGREEN_EX +
          '\n' + '-' * 110 + '\n' + Style.RESET_ALL)


def main():
    # Check for command-line arguments
    parser = argparse.ArgumentParser(
        description='Play a game of crazy eights.')
    parser.add_argument('-p', '--players', nargs='?', default=-1, type=int,
                        choices=range(1,5), metavar='1-4', help='Set number of human players')
    parser.add_argument('-D', '--debug', action='store_true',
                        help='Run in debug mode')
    parser.add_argument('--test', action='store_true',
                        help='Jump straight to current test')
    args = parser.parse_args(sys.argv[1:])

    print_welcome()

    # Set number of players
    try:
        # Check if the user passed a valid number of players via command line, and use it if so
        if args.players in range(1, 5):
            num_players = args.players
        else:
            num_players = input(
                'Enter 1-4 for number of human players (default 1):')
            num_players = int(num_players[0])
            # If the user gave invalid input or no input, use the default
            if num_players not in range(1, 5):
                num_players = 1
    # Either the user pressed enter for the default, or they can't even be trusted to type in an integer and probably don't have any friends, so just do a 1-player game
    except Exception:
        num_players = 1

    game = Game(num_players, args.debug)
    game.play()


if __name__ == '__main__':
    main()
