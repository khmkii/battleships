from board import Board
from ship import Ship


class Player:
    def __init__(self, name, x, fleet):
        self.name = name
        self.board = Board(x)
        self.ships = [Ship(*f, set(), False) for f in fleet]
        self.sunk = set()

    def add_ship(self, locus, orientation, ship_to_place):
        x, y = locus
        placement = {locus}
        clashes = []
        if orientation == 'h':
            for count in range(ship_to_place.length - 1):
                col_index = self.board.LETTERS.find(x) + 1 + count
                try:
                    cell = (self.board.LETTERS[col_index], y)
                    placement.add(cell)
                except IndexError:
                    message = "Ship placement is partially outside board range"
                    return None, message
            if placement < set(self.board.coordinates):
                for ship in self.ships:
                    if bool(placement & ship.location):
                        clashes.append(list(placement & ship.location))
                    else:
                        continue
                if not clashes:
                    ship_to_place.location = placement
                    for cell in placement:
                        self.board.dictionary[cell] = ship_to_place.symbol
                    message = "Success"
                    return placement, message
                else:
                    message = "There is a problem with placing the ship there, overlaps other ships"
                    return clashes, message
            else:
                message = "Ship placement is partially outside board range"
                return None, message
        elif orientation == 'v':
            for count in range(ship_to_place.length - 1):
                cell = (x, str(int(y) + 1 + count))
                placement.add(cell)
            if placement < set(self.board.coordinates):
                for ship in self.ships:
                    if bool(placement & ship.location):
                        clashes.append(ship.location)
                    else:
                        continue
                if not clashes:
                    ship_to_place.location = placement
                    for cell in placement:
                        self.board.dictionary[cell] = ship_to_place.symbol
                    message = "Success"
                    return placement, message
                else:
                    message = "There is a problem with placing the ship there"
                    return clashes, message
            else:
                message = "Ship placement is partially outside board range"
                return None, message

    def take_incoming(self, target):
        if self.board.dictionary[target] in [x.symbol for x in self.ships]:
            self.board.dictionary[target] = 'X'
            self.board.hits.append(target)
            return print('You scored a hit')
        else:
            self.board.dictionary[target] = 'M'
            self.board.misses.append(target)
            return print('You missed')

    def sink_or_swim(self):
        current_sunk = {x for x in self.sunk}
        for ship in self.ships:
            if ship.symbol not in self.board.dictionary.values():
                ship.sunk = True
                for loc in ship.location:
                    self.board.dictionary[loc] = '*'
                self.sunk.add(ship)
        if bool(self.sunk - current_sunk):
            sunk_ship = (self.sunk - current_sunk).pop()
            return print('You sunk the {}'.format(sunk_ship.name))