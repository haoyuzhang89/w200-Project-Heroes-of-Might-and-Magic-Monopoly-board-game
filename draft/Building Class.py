class Building:
    """building on the board, including castles, shop, etc"""

    def __init__(self, name, location):
        self.name = name
        self.location = location


class Castle(Building):

    def __init__(self, name, location, price):
        super().__init__(name, location)

        self.level = 1  # maximum level is 5
        self.price = price
        self.up_fee = int(price * 0.6)  # upgrade cost for each time
        self.up_ratio = 2  # production improvement for each upgrade
        self.owner = None  # None at begining
        self.army = price
        self.production = int(price / 20)  # production of gold and army per day