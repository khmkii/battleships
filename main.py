import player
import game
import os
import platform


def validate_cell_input2(player_input, target_board):
    try:
        selection = player_input.strip().upper()
        selection_cell = selection[0], selection[1:]
        if selection_cell in target_board.coordinates:
            cmessage = 'Coordinate Ok'
            return selection_cell, cmessage
        else:
            letter_list = [x for x in target_board.LETTERS]
            cmessage = ''
            if selection_cell[0] not in letter_list:
                cmessage += 'First part of the coordinate must' \
                            ' be a letter from {} followed by a number '.format(''.join(letter_list))
            elif selection_cell[1] not in range(1, target_board.dimension + 1):
                cmessage += 'Second part of the coordinate needs' \
                            ' to be a number from 1 to {}'.format(target_board.dimension)
            return None, cmessage
    except IndexError:
        return None, "It seems you entered nothing, try again"


def validate_orientation(player_input):
    player_input = player_input.strip().lower()
    if player_input in 'hv':
        omessage = 'Orientation Ok'
        return player_input, omessage
    else:
        omessage = "Orientation must be 'h' for horizontal, or 'v' for vertical"
        return None, omessage


def print_pl_board(print_object):
    action_row = '{:^3}' + '|{:^3}' * print_object.dimension + '|'
    base_row = '{:^4}' + '{:^4}' * print_object.dimension
    for i in reversed(range(1, print_object.dimension + 1)):
        cells = sorted([(key[0], value) for key, value in print_object.dictionary.items() if
                        key[1] == str(i)], key=lambda x: x[0])
        print(action_row.format(i, *[x[1] for x in cells]))
    print(base_row.format('', *[str(letter) for letter in print_object.LETTERS[:print_object.dimension]]))


def print_op_board(print_obj, player_obj):
    action_row = '{:^3}' + '|{:^3}' * print_obj.dimension + '|'
    base_row = '{:^4}' + '{:^4}' * print_obj.dimension
    ship_symbols = [boat.symbol for boat in player_obj.ships]
    for i in reversed(range(1, print_obj.dimension + 1)):
        cell_tuples = sorted(
            [(key[0], value) for key, value in print_obj.dictionary.items() if
                key[1] == str(i)], key=lambda x: x[0]
        )
        cells = [' ' if x[1] in ship_symbols else x[1] for x in cell_tuples]
        print(action_row.format(i, *cells))
    print(base_row.format('', *[str(letter) for letter in print_obj.LETTERS[:print_obj.dimension]]))


def quit_programme():
    os._exit(1)


def clear_tscreen():
    if 'Windows' in platform.architecture()[1]:
        os.system('cls')
    else:
        os.system('clear')


if __name__ == '__main__':

    while True:
        start = input('Welcome, do you want to start a game of Battleships? '
                      'enter Y to start, Q to quit, or H to read the instructions\n> ').strip().lower()
        if start == 'q':
            quit_programme()
        elif start == 'y':
            print("Ok, lets start the game")
            break
        elif start == 'h':
            print(game.instructions)
        else:
            print('I will take that as a yes, let\'s start the game')
            break

    while True:
        grid_size = input("What size board do you want to play on, enter '5' for the minimum 5 x 5"
                      "\nor 26 for the maximum 26 x 26 board, or any number in between\n> ").strip()
        try:
            grid_size = int(grid_size)
        except ValueError:
            print("I need a number from 5 to 26")
            continue
        if grid_size not in [x for x in range(5, 27)]:
            print("I need a number; either 5, 26 or anything in between")
            continue
        break

    player_one = player.Player(input("Enter player one's name > "), grid_size, game.fleet)

    player_two = player.Player(input("Enter player two's name > "), grid_size, game.fleet)

    print("It's time for {} to place their ships".format(player_one.name))
    input("Make sure {} has the computer, press any key to continue".format(player_one.name))

    for ship_to_anchor in player_one.ships:
        while True:
            anchor = input("{}, Give me a coordinate,"
                           " for example 'A1', "
                           "to anchor your {} > ".format(player_one.name, ship_to_anchor.name))
            anchor, message = validate_cell_input2(anchor, player_one.board)
            if anchor is None:
                print(message)
                continue
            print(message)
            mooring = input('Do you want the ship to lie (H)orizontally, or (V)ertically? > ')
            mooring, message = validate_orientation(mooring)
            if mooring is None:
                print(message)
                continue
            result, comment = player_one.add_ship(anchor, mooring, ship_to_anchor)
            if comment == 'Success':
                print(message + ', ' + comment + ' ship placed at {}'.format(*result))
                print_pl_board(player_one.board)
                break
            elif result is None:
                print(comment)
                continue
            else:
                print('else entered')
                print(comment + ' at {}'.format(result))
                continue

    print("It's time for {} to place their ships".format(player_two.name))
    print('{} press any key and hand the computer to {}'.format(player_one.name, player_two.name))
    input()
    clear_tscreen()

    for ship_to_anchor in player_two.ships:
        while True:
            anchor = input("{}, give me a coordinate, "
                           "for example 'A1', "
                           "to anchor your {} > ".format(player_two.name, ship_to_anchor.name))
            anchor, message = validate_cell_input2(anchor, player_two.board)
            if anchor is None:
                print(message)
                continue
            print(message)
            mooring = input('Do you want the ship to lie (H)orizontally, or (V)ertically? > ')
            mooring, message = validate_orientation(mooring)
            if mooring is None:
                print(message)
                continue
            result, comment = player_two.add_ship(anchor, mooring, ship_to_anchor)
            if comment == 'Success':
                print(message + ', ' + comment + ' ship placed at {}'.format(*result))
                print_pl_board(player_two.board)
                break
            elif result is None:
                print(comment)
                continue
            else:
                print('else entered')
                print(comment + ' at {}'.format(result))
                continue

    input('{}, press any key and hand the computer back to {}, '
          'it\'s time to start the battle'.format(player_two.name, player_one.name))
    clear_tscreen()

    winner = None
    loser = None

    while True:
        while True:
            input('{} press any key when ready'.format(player_one.name))
            print_pl_board(player_one.board)
            input('Review your board, '
                  'and then press any key when ready to see your opponents board'
                  ' and plan your attack')
            print_op_board(player_two.board, player_two)
            player_one_shot = input("{} Where do you want to fire?".format(player_one.name))
            player_one_shot, message = validate_cell_input2(player_one_shot, player_two.board)
            if player_one_shot is None:
                print(message)
                continue
            elif player_one_shot in player_two.board.hits:
                print('You have already fired and hit something there')
                continue
            elif player_one_shot in player_two.board.misses:
                print('You have already fired and missed there')
                continue
            else:
                print(message)
                player_two.take_incoming(player_one_shot)
                player_two.sink_or_swim()
                break
        if False not in [s.sunk for s in player_two.ships]:
            winner = player_one.name
            loser = player_two.name
            break
        input('{} press any key then hand the computer to {}'.format(player_one.name, player_two.name))
        clear_tscreen()
        while True:
            input('{} press any key when ready'.format(player_two.name))
            print_pl_board(player_two.board)
            input('Review your board, '
                  'and then press any key when ready to see your opponents board'
                  ' and plan your attack')
            print_op_board(player_one.board, player_one)
            player_two_shot = input("{} Where do you want to fire?".format(player_two.name))
            player_two_shot, message = validate_cell_input2(player_two_shot, player_one.board)
            if player_two_shot is None:
                print(message)
                continue
            elif player_two_shot in player_one.board.hits:
                print('You have already fired and hit something there')
                continue
            elif player_two_shot in player_one.board.misses:
                print('You have already fired and missed there')
                continue
            else:
                print(message)
                player_one.take_incoming(player_two_shot)
                player_one.sink_or_swim()
                break
        if False not in [s.sunk for s in player_one.ships]:
            winner = player_two.name
            loser = player_one.name
            break
        input('{} press any key then hand the computer to {}'.format(player_two.name, player_one.name))
        clear_tscreen()

    print("The battle has been won")
    print("{} has sunk {}'s fleet".format(winner, loser))
    print("{}'s accuracy was {:.2f}".format(player_one.name,
            len(player_one.board.hits) / (len(player_one.board.hits) + len(player_one.board.misses)))
          )
    print("{}'s accuracy was {:.2f}".format(player_two.name,
            len(player_two.board.hits) / (len(player_two.board.hits) + len(player_two.board.misses)))
          )

    input("Press any key to see the each players boards")
    print(player_one.name)
    print_pl_board(player_one.board)
    print(player_two.name)
    print_pl_board(player_two.board)
