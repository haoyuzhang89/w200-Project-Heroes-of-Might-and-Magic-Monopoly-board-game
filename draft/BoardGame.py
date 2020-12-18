# Class List
class BoardGame:
    """Main part of the board game, store board, players list. Control game step, checking victory and delete failed player"""

    def __init__(self, num_player=4):
        self.heros = []  # list of players
        self.board = []  # board information
        self.size = num_player
        self.round = 1

    def round_check(self):  # hero with no gold, army, castle is lost, print notice, then remnove it from heroes list
        for i in range(self.size):
            if self.heros[i].gold <= 0 and self.heros[i].army == 0 and len(self.heros[i].castle) < 1:
                print("Hero " + self.heros[i].name + " is defeated!\n")
                self.size -= 1
            else:
                continue
        # if there is only one hero left, he is the winner

        if self.size == 1:
            print(" Hero " + self.heros[i].name + " conquered the land!\n")

    def round_step(self):  # board game running for a round

        # Notice of round start, all playr move and inactive with space
        print("Round " + str(self.round) + "\n")
        self.round += 1

        for hero in self.heros:

            print(hero.name + ", it is your turn.\n")
            print("Currently, you have " + str(hero.gold) + " gold, " + str(hero.army) + " army," + str(len(hero.castle)) + " castles.")
            hero.move_forward()

            space = hero.block_check(self.board)

            if type(space) == Castle:
                print("It is a Castle\n")
                hero.act_castle(space, self.heros)
            else:
                print("You are at other type space")

            # Hero collect production from the castles they owned

        for hero in self.heros:
            if not hero.castle is None:
                for castle in hero.castle:
                    hero.gold += castle.production
                    hero.army += castle.production
            else:
                continue

        print("Heros received supply from their castles.\n")