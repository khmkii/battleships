import string


class Board:

    LETTERS = string.ascii_uppercase

    def __init__(self, x):
        self.dimension = x
        self.coordinates = [(c, str(r)) for c in self.LETTERS[:x] for r in range(1, x + 1)]
        self.dictionary = {cell: '' for cell in self.coordinates}
        self.hits = []
        self.misses = []