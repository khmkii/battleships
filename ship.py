class Ship:

    def __init__(self, name, length, symbol, location=set(), sunk=False):
        self.name = name
        self.length = length
        self.symbol = symbol
        self.location = location
        self.sunk = sunk
