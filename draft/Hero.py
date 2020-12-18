import random

class Hero:
    """Player is a hero."""
    def __init__(self, name):
        self.name = name
        self.location = 0
        self.gold = 1500  # 1500
        self.army = 1500  # 1500
        self.castle = []
        self.equips = []
        self.attack = 100
        self.defense = 100

    def move_forward(self):
        """Movement decided by two dices"""
        dice_1 = random.randint(1, 6)
        dice_2 = random.randint(1, 6)  # roll two dices once
        forward = dice_1 + dice_2
        print('Rolling dices......Dice 1 is ' + str(dice_1) + ', Dice 2 is ' + str(dice_2) + '.')

        self.location += forward  # update position after movement

        if self.location >= 40:
            self.gold += 200  # pass go collect 200 gold
            print('Collect 200 gold as you pass go.\n')
        self.location = self.location % 40  # board is of 40 blocks

        print('Hero ' + self.name + ' is marching, arrives Space ' + str(
            self.location) + ' now.\n')  # location update info

    def block_check(self, board):

        """input is hero, and board is list of all the blocks,
           output the type of block"""

        for space in board:
            if self.location == space.location:
                building = space
                break
            else:
                continue

        return building  # return the building where hero is located: castle, shop, etc

    def act_castle(self, castle, heros):

         """Actions heroes can take at a castleinput castle are castle hero is located, heros is list of heroes.(BoardGame.heros)"""

        if castle.owner is None:  # castle is of no owner it is available for sale

            while True:

                isbuyyes = input(
                    "Would you like to purchase the Castle for " + str(castle.price) + " gold? (Y - Yes, N - No)\n")

                if isbuyyes.lower() == "y":  # want to buy

                    if self.gold >= castle.price:  # enough gold
                        self.gold -= castle.price
                        castle.owner = self.name
                        self.castle.append(castle)
                        print("Your territory just expanded!\n")
                        break

                    else:
                        print("You don't have enough gold! Purchase failed.\n")
                        break

                elif isbuyyes.lower() == "n":  # don't want to buy
                    print("You and your soldiers stationed outsides the castle for one night.\n")
                    break

                else:
                    print("Pardon me.\n")
                    continue

        elif castle.owner == self.name:  # Heroes can upgrade the castle that belongs to himself.

            if castle.level == 5:
                print(" Your highness, the castle has been upgraded to the top level!\n")

            else:
                while True:

                    islevelyes = input(
                        "Would you like to upgrade the Castle for " + str(castle.up_fee) + " gold? (Y - Yes, N - No)\n")

                    if islevelyes.lower() == "y":  # want to upgrade

                        if self.gold >= castle.up_fee:  # enough gold
                            self.gold -= castle.up_fee  # charge
                            castle.level += 1  # upgrade level
                            castle.army *= castle.up_ratio
                            castle.production *= castle.up_ratio

                            print("Your castle has reached level " + str(castle.level) + " !\n")
                            break

                        else:  # not enough gold
                            print("You don't have enough gold! Upgrade failed.\n")
                            break

                    elif islevelyes.lower() == "n":  # don't want to upgrade
                        print("Wish you bring some reinforce next time.\n")
                        break

                    else:
                        print("Pardon me.\n")
                        continue

        else:  # Heros can try to capture the castle that belongs to others.
            while True:
                isattackyes = input(
                    "This is a castle belongs to enemy. Caputre it? (Y - Yes, N - No)\n")

                if isattackyes.lower() == "y":  # want to attack
                    print("Battle Starts!!!\n")

                    hero_power = self.army * (1 + self.attack) / (1 + castle.level * 20)  # hero power
                    castle_power = castle.army * 10 * castle.level / (self.defense / 100)  # castle power during battle

                    if hero_power == castle_power:  # it is a tie, hero lost all the army
                        self.army = 0
                        print("The battle is over.We didn't make it... fought until the final soldier.\n")
                        break

                    elif hero_power < castle_power:  # hero lost
                        self.army = 0
                        winner = hero_search(castle.owner, heros)  # winner is owner of the castle,
                        winner.gold += castle.price  # winner get the gold
                        winner.gold = int(winner.gold)

                        self.gold -= castle.price  # pay gold castle price to the owner of castle
                        self.gold = int(self.gold)
                        print("The enemy is too strong.Our troops are defeated. We paid some gold as indemnity.\n")
                        break

                    else:  # hero win
                        army_lost = int(self.army * castle_power / hero_power)
                        self.army -= army_lost
                        castle.owner = self.name
                        self.castle.append(castle)  # hero get the castle

                        loser = hero_search(castle.owner, heros)  # castle owner is the loser
                        loser.castle.remove(castle)  # loser lost the owner
                        print("Victory! We caputred another castle, my lord!\n")
                        break

                elif isattackyes.lower() == "n":  # no attack, just pass
                    print("You troop sneaked out of the enemy's terrtory safely.\n")
                    break
                else:
                    print("Pardon me.\n")
                    continue

