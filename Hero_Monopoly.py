import random
import time
import sys
import csv


# Function modules
def hero_search(name, heros):
    """Input hero's name (string), heroes list. output hero(class Hero) owns the name"""

    for hero in heros:
        if hero.name == name:
            return hero
    else:
        return None  # if there is no one matches, return None


def roll_dice(dice_number):
    """Roll dices of dice_number, most 2 times in this game"""
    i = 1
    dice_sum = 0
    input(">>Enter any to rolling dices.")
    print('Rolling dices......')
    time.sleep(0.5)

    while i <= dice_number:
        dice = random.randint(1, 6)
        print('Dice {} is {}.'.format(i, dice))
        dice_sum += dice
        i += 1
    return dice_sum


#################################################################

# Class List

class getoutofloop(Exception):
    """Exception class for jump out of multiple while loops"""
    pass


# Class of Game

class BoardGame:
    """Main part of the board game, store board, players list. Control game step, checking victory and delete failed
    player """

    def __init__(self, num_player=4):
        self.heros = []  # list of players
        self.board = []  # board map information
        self.size = num_player  # num of active players
        self.round = 1  # round no

    def round_check(self):

        """After each round of game, check if hero survive from debt, update the surviving heroes.
        Exit in advance between rounds if need. Check if there is a victory and exit."""

        hero_next_round = []  # heroes survivor list
        if self.size >= 2:  # only check if there are two or more heroes
            for hero in self.heros:
                if hero.gold < 0 and len(hero.castle) > 0:  # hero sell castles for debt
                    hero.pay_debt()  # def Hero.pay_debt in Class Hero

            for hero in self.heros:
                if hero.gold <= 0 and len(hero.castle) < 1:  # hero lose the game when owns no gold, no castle
                    print("Hero " + hero.name + " owns no gold or castles, he is defeated!\n")
                    time.sleep(0.5)
                    self.size -= 1  # update num of active players

                else:
                    hero_next_round.append(hero)  # surviving hero for next round
                    self.heros = hero_next_round

        if self.size == 1:  # if there is only one hero left, he is the winner
            print("Hero " + self.heros[0].name + " conquered the land!!!\n")  # Victory announcement of the winner
            time.sleep(1)
            print("The End.\n")  # end of the game
            time.sleep(0.5)
            while True:
                isexityes = input(">>Please input exit to quit\n")  # ask player if to quit the program
                time.sleep(0.5)
                if isexityes.lower() == "exit":
                    sys.exit()  # exit the program
                else:
                    continue

        else:  # check if players want to end game in advance between rounds
            isexitadyes = input(">>Continue? Enter exit to quit, other key to continue.\n")
            time.sleep(0.5)
            if isexitadyes.lower() == "exit":  # input exit to quit in advance
                sys.exit()  # exit the program

    def round_step(self):

        """Run the board game for one round. Notice of round start, all players move and inactive with space"""

        print("     [\n@XXXX[{::::::::::::::::::::::::::::::::::::>\n     [\n")  # mark for different rounds
        time.sleep(0.5)
        print("Round " + str(self.round) + "\n")  # round number
        time.sleep(1)
        self.round += 1

        for hero in self.heros:  # each hero play one by one

            print(hero.name + ", it is your turn.\n")  # call the hero, notice his term
            time.sleep(0.5)
            print("Currently, you have " + str(hero.gold) + " gold, " + str(hero.army) + " army, " + str(
                len(hero.castle)) + " castles.\n")  # statement of hero status
            print("Your hero status is, Attack -- {} Defense -- {}.\n".format(hero.attack, hero.defense))

            print("Equipment: ", end="")  # statement of hero status
            for equip in hero.equips:
                print(equip.name, end=", ")
            print("\n")
            time.sleep(0.5)
            hero.move_forward()

            space = hero.block_check(
                self.board)  # check the building type where hero locates, def Hero.block_check in Class Hero
            print(space)  # notice of where it is
            time.sleep(0.5)

            if type(space) == Castle:  # Hero acts at Castle
                hero.act_castle(space, self.heros)  # def hero.act_castle in Class Hero

            elif type(space) == Arena:  # Hero acts at Arena
                hero.act_arena()  # def hero.act_arena in Class Hero

            elif type(space) == Monolith:  # Hero acts at Monolith
                hero.act_monolith(space)  # def act_monolith in Class Hero

            elif type(space) == Market:  # Hero acts at Market
                hero.act_market(space)  # def act_market in Class Hero

            print("--------------------------------------------\n")  # mark for end of each hero player
            time.sleep(1)

        for hero in self.heros:  # Hero collect gold and army supply from the castles they owned
            if hero.castle:
                for castle in hero.castle:
                    hero.gold += castle.production
                    hero.army += castle.production
            else:
                continue

        print("Heros received supply from their castles.\n")  # notice of supply
        time.sleep(2)


# Classes of Building

class Building:
    """building on the board, including castles, shop, etc"""

    def __init__(self, name, location):
        self.name = name  # name of building
        self.location = location  # location of building on the board map (0-35)


# Subclasses of Building

class Castle(Building):
    """Building can be purchased, captured, upgraded by Hero, def hero.act_castle in Class Hero"""

    def __init__(self, name, location, price):
        super().__init__(name, location)

        self.level = 1  # maximum level is 5
        self.price = price  # sale price
        self.up_fee = 0.6  # upgrade cost for each time 60% of current price
        self.up_ratio = 2  # production improvement for each upgrade
        self.owner = None  # name of hero owning the castle, None at beginning
        self.army = price  # army defending the  castle
        self.production = int(price / 20)  # supply of gold and army per round

    def __str__(self):  # notice of arrival at the castle, castle stats
        return "Here is a Level " + str(self.level) + " Castle " + self.name + ".\n(Price: " + str(
            self.price) + " Army : " + str(self.army) + " Gold Supply: " + str(
            self.production) + " Army Supply: " + str(self.production) + ")"


class Arena(Building):
    """Building where heroes can be trained, def hero.act_arena in Class Hero"""

    def __init__(self, name, location):
        super().__init__(name, location)

    def __str__(self):
        return "Here is Arena " + self.name + ".\n"  # building welcome word


class Monolith(Building):
    """Building where hero is teleport to self.next_position, def hero.act_monolith in Class Hero """

    def __init__(self, name, location, next_location):
        super().__init__(name, location)
        self.next_location = next_location  # teleport destination

    def __str__(self):  # notice of arrival at the monolith
        return "Here is a Monolith " + self.name + ".\n"


class Market(Building):
    """Building where hero can purchase equipment (Class Equipment), def hero.act_market in Class Hero"""

    def __init__(self, name, location):
        super().__init__(name, location)
        self.equips_stk = []  # equipments in stock at the market

    def __str__(self):  # notice of arrival at the market
        return "Here is " + self.name + " Market.\n"


# Class Item

class Equipment:
    """Equipment stock at the store, be purchased and equipped by hero, def hero.act_market in Class Hero"""

    def __init__(self, name, price, att_add, def_add):
        self.name = name  # name of equipment
        self.price = price  # sale price of equipment
        self.att_add = att_add  # attack enhancement for hero
        self.def_add = def_add  # defense enhancement for hero

    def __str__(self):  # equipment stats shown in the market
        return '{:35s}Attack:{:4d}, Defense:{:4d} ----- Gold {:4d}'.format(self.name, self.att_add, self.def_add,
                                                                           self.price)

########################################################################################

class Hero:
    """Player of the game is a hero. Move and interact with Castle, Market, Monolith, Arena"""

    def __init__(self, name, gold=1500, army=1500):

        self.name = name  # name of hero
        self.location = 0  # location of hero at the board map
        self.gold = gold  # resource for purchase, default 1500
        self.army = army  # resource for capture, training default 1500
        self.castle = []  # castles list that hero owns
        self.equips = []  # equipments list that hero owns
        self.attack = 100  # hero stats for capture battle
        self.defense = 100  # hero stats for capture battle

    def move_forward(self):
        """Movement decided by two dices"""
        forward = roll_dice(2)  # roll two dices once

        self.location += forward  # update position after movement

        if self.location >= 36:  # pass the start after movement, board is of 36 blocks
            self.gold += 200  # pass go collect 200 gold
            self.location = self.location % 36
            print('Collect 200 gold as you pass go.\n')
            time.sleep(0.5)

        print('Hero ' + self.name + ' is marching, arrives Space ' + str(
            self.location) + ' now.\n')  # location update info
        time.sleep(0.5)

    def block_check(self, board):

        """input is hero, and board is list of all the blocks,
           output the type of block"""

        for space in board:
            if self.location == space.location:
                return space  # return the building class where hero is located: Castle, Market, etc
            else:
                continue

    def pay_debt(self):
        """when hero is of debt, sell owning castles until cover the debt or no castles left"""
        while self.gold < 0:  # stop selling castles when debt is covered
            if len(self.castle) > 0:
                castle_debt = self.castle.pop(0)  # sell one castle
                self.gold += castle_debt.price  # pay debt
                castle_debt.owner = None  # castle belongs to None now
                print("{} mortgaged Level {} Castle {} as {} gold for his debt.\n".format(
                    self.name, castle_debt.level, castle_debt.name, castle_debt.price))  # Notice of sale
                time.sleep(0.5)
            else:  # stop when hero owns no castle, fail to pay debt
                print("{} mortgaged all his property, still failed to pay the debt.\n".format(self.name))  # notice
                time.sleep(0.5)
                break

    # (optional )def surrender(self): """Hero choose to surrender, empty all the castle ownership, and quit the game"""

    def act_arena(self):

        """Actions heroes can take at Arena, do some training to enhance attack and defence, decided by dices"""

        while True:
            istrainyes = input(
                ">>Any fighting art training here? Your soldiers will get wounded but you will be stronger? (Y - Yes, "
                "N - No)\n")  # ask if want to train

            if istrainyes.lower() == 'y':  # yes to train
                print("Roll dices to see your training enhancement \n")
                train_enhance = roll_dice(2)  # ehancement of attack and defense
                self.attack += train_enhance
                self.defense += train_enhance
                print()
                print("Roll dices to decide the troop loss.\n")
                army_lost = roll_dice(2)  # cost for training
                army_lost *= train_enhance  # army_lost is dice(2) * dice(2)
                self.army -= army_lost

                print("Your attack, defense increased by " + str(train_enhance) + '.\n')  # notice
                time.sleep(0.5)
                print("At the same time, " + str(army_lost) + ' soldiers injured.\n')  # notice
                time.sleep(0.5)

                if self.army < 0:  # mim army size is 0, hero with less army has training benefit
                    self.army = 0
                break

            elif istrainyes.lower() == 'n':  # no to train
                print("Maybe next time.\n")
                time.sleep(0.5)
                break

            else:  # invalid response
                print("Pardon me.\n")
                time.sleep(0.5)

    def act_monolith(self, monolith):

        """Hero teleports to monolith.next_location
        """

        print("After touching the Monolith, Hero and the troops are teleported by some unknown power...\n")
        time.sleep(0.5)
        if self.location > monolith.next_location:  # if pass the start to go block
            self.gold += 200  # pass go collect 200 gold
            print('Collect 200 gold as you pass go.\n')
        self.location = monolith.next_location  # teleport to the next location
        print("You are at space " + str(self.location) + " now.\n")  # notice of new location
        time.sleep(0.5)

    def act_market(self, market):

        """Hero can purchase equipment from the market.equips_stk
        """
        try:
            while True:
                ispurchaseyes = input(
                    ">>Would you like to buy any equipment(One item limit every visit)? (Y - Yes, N - No)\n")
                time.sleep(0.5)  # check if want to buy

                if ispurchaseyes.lower() == "y":  # yes to buy
                    print("Welcome, here is the sale list today!\n")
                    time.sleep(0.5)

                    for i in range(len(market.equips_stk)):  # print the list of equipments in stock
                        print(i, end="-")
                        print(market.equips_stk[i])
                    print("Q-Quit")
                    time.sleep(0.5)

                    while True:
                        equip_id = input(
                            ">>Which equipment you want to purchase? (Input NO.of the equipment to choose, Q - Quit)\n")
                        time.sleep(0.5)  # ask which equipment to buy
                        if equip_id.lower() == 'q':  # quit the trading
                            raise getoutofloop()  # jump out of two whiles, end act at market

                        elif equip_id.isdigit():  # input a number to choose equipment
                            equip_id = int(equip_id)
                            if not equip_id in range(len(market.equips_stk)):  # not available equipment id
                                print("Pardon me. Please make the available choice.\n")
                                time.sleep(0.5)
                                continue  # continue for re-choose id

                            elif self.gold < market.equips_stk[equip_id].price:  # no enough gold
                                print("You don't have enough gold.Please make the available choice.\n")
                                time.sleep(0.5)
                                continue  # continue for re-choose id

                            elif self.gold >= market.equips_stk[equip_id].price:  # available item, enough gold
                                self.gold -= market.equips_stk[equip_id].price
                                self.attack += market.equips_stk[equip_id].att_add
                                self.defense += market.equips_stk[equip_id].def_add
                                self.equips.append(market.equips_stk.pop(
                                    equip_id))  # equipment add to hero.equips list, pop from the equips_stk list
                                print("You received a new equipment!\n")
                                time.sleep(0.5)
                                raise getoutofloop()  # jump out of two whiles, end act in the market

                        else:  # invalid response to equipment id
                            print("Pardon me. Please make the available choice.\n")
                            continue  # continue for re-choose id

                elif ispurchaseyes.lower() == "n":  # don't want to buy
                    time.sleep(0.5)
                    break  # end act in the market

                else:  # invalid response if want to buy
                    print("Pardon me.\n")
                    time.sleep(0.5)
                    continue  # continue choose if want to buy

        except getoutofloop:  # jump out of two whiles loop
            pass

        print("See you next time!\n")  # end act in the market

    def act_castle(self, castle, heros):

        """Actions heroes can take at a castle, input castle is the castle hero is located, heros is the list of heroes.
        (BoardGame.heros)
        """

        if castle.owner is None:  # castle is of no owner it is available for sale

            while True:

                isbuyyes = input(
                    ">>Would you like to purchase the Castle for " + str(castle.price) + " gold? (Y - Yes, N - No)\n")
                # check if want to buy

                if isbuyyes.lower() == "y":  # yes to buy

                    if self.gold >= castle.price:  # enough gold
                        self.gold -= castle.price
                        castle.owner = self.name  # update castle owner name
                        self.castle.append(castle)  # add to hero.castle list
                        print("Your territory just expanded!\n")
                        time.sleep(0.5)
                        break  # end act at the castle

                    else:  # not enough gold
                        print("You don't have enough gold! Purchase failed.\n")
                        time.sleep(0.5)
                        break  # end act at the castle

                elif isbuyyes.lower() == "n":  # no to buy
                    print("You and your soldiers stationed outsides the castle for one night.\n")
                    time.sleep(0.5)
                    break  # end act at the castle

                else:  # invalid response to if want to buy
                    print("Pardon me.\n")
                    time.sleep(0.5)
                    continue  # continue for re-choose if want to buy

        elif castle.owner == self.name:  # Heroes can upgrade the castle that belongs to himself.

            if castle.level == 5:  # max level is 5
                print(" Your highness, the castle has been upgraded to the top level!\n")
                time.sleep(1)

            else:
                while True:

                    level_up_fee = int(castle.up_fee * castle.price)

                    islevelyes = input(
                        ">>Would you like to upgrade the Castle for " + str(
                            level_up_fee) + " gold? (Y - Yes, N - No)\n")  # check if to upgrade
                    time.sleep(0.5)

                    if islevelyes.lower() == "y":  # yes to upgrade

                        if self.gold >= level_up_fee:  # enough gold
                            self.gold -= level_up_fee  # charge fee
                            castle.level += 1  # upgrade level
                            castle.army *= castle.up_ratio
                            castle.production *= castle.up_ratio
                            castle.price *= castle.up_ratio

                            print("Your castle has reached level " + str(castle.level) + " !\n")
                            time.sleep(0.5)
                            break  # end act in the castle

                        else:  # not enough gold
                            print("You don't have enough gold! Upgrade failed.\n")
                            time.sleep(0.5)
                            break  # end act in the castle

                    elif islevelyes.lower() == "n":  # no to upgrade
                        print("Wish you bring some reinforce next time.\n")
                        time.sleep(0.5)
                        break  # end act in the castle

                    else:  # invalid response if want to upgrade
                        print("Pardon me.\n")
                        time.sleep(0.5)
                        continue  # continue re-choose if want to upgrade

        else:  # Heros can try to capture the castle that belongs to others.
            while True:
                isattackyes = input(
                    ">>This is a castle belongs to enemy, " + castle.owner + ". Capture it? (Y - Yes, N - No)\n{You "
                                                                             "will lose half of your gold (at least "
                                                                             "half the castle price) and all "
                                                                             "your army if you lose.\n Or you can pay "
                                                                             "half the castle price to pass "
                                                                             "safely.}\n")
                # check if want to capture

                if isattackyes.lower() == "y":  # yes to capture
                    print("Battle Starts!!!\n")
                    time.sleep(1)

                    hero_power = self.army * self.attack * 0.01 / (1 + castle.level * 0.25)  # hero power during battle
                    castle_power = castle.army * 10 * castle.level / (self.defense * 0.01)  # castle power during battle

                    if hero_power == castle_power:  # it is a tie, hero lost all the army
                        self.army = 0
                        print("The battle is over.We didn't make it... fought until the final soldier.\n")
                        time.sleep(0.5)
                        break  # end act in the castle

                    elif hero_power < castle_power:  # hero lost, lost all his army, half gold or half castle price
                        self.army = 0
                        winner = hero_search(castle.owner, heros)  # winner is owner of the castle,
                        indemnity = max(int(0.5 * self.gold), int(0.5 * castle.price))
                        # indemnity is half of hero's gold, at least more than half of the castle price

                        winner.gold += indemnity  # winner receives the gold
                        self.gold -= indemnity  # hero pays the gold
                        print(
                            'The enemy is too strong.Our troops are defeated. We paid {} gold as indemnity.\n'.format(
                                indemnity))
                        time.sleep(0.5)
                        break  # end act in the castle

                    else:  # hero win
                        army_lost = int(self.army * castle_power / hero_power)  # army cost in the battle
                        self.army -= army_lost
                        print(str(army_lost) + " soldiers fought till their death.\n")

                        loser = hero_search(castle.owner, heros)  # castle owner is the loser
                        loser.castle.remove(castle)  # loser lost the ownership of castle

                        self.castle.append(castle)  # hero get the castle
                        castle.owner = self.name
                        print("Victory! We conquered another castle, my lord!\n")
                        time.sleep(0.5)
                        break  # end act in the castle

                elif isattackyes.lower() == "n":  # no to capture
                    pass_fee = int(0.5 * castle.price)  # pay half the castle price for pass fee
                    self.gold -= pass_fee
                    pass_receiver = hero_search(castle.owner, heros)  # castle owner collect pass_fee
                    pass_receiver.gold += pass_fee
                    print("After paid {} gold, your troop sneaked out of the enemy's territory safely.\n".format(
                        pass_fee))
                    time.sleep(0.5)
                    break  # end act in the castle

                else:  # invalid response to if want to capture
                    print("Pardon me.\n")
                    time.sleep(0.5)
                    continue  # continue for re-choose if want to capture


####################################################################
# Initialize and Run the Game
print("Welcome to Heroes of Might & Magic Monopoly.\n")
time.sleep(0.5)

while True:  # decide players number
    player_num = input(">>How many players(Heroes) will play the game? (2-4 is recommended)\n")  # ask players number
    time.sleep(0.5)

    if player_num.isdigit():
        player_num = int(player_num)
        if player_num < 2:  # 1 player mode is not supported
            print("At least 2 players are required.\n")
            time.sleep(0.5)
            continue
        elif player_num > 6:  # more than 6 players are not recommended
            print("Too many players will affect the playing experience.\n")
            time.sleep(0.5)
            continue
        else:
            break
    else:
        print("This is not number.\n")
        continue

newgame = BoardGame(player_num)  # initial newgame class BoardGame

# initial work for players
namelist = []  # waiting list for heroes names to avoid repeat name
for i in range(player_num):
    while True:
        hero_name = input(">>Play {}, enter your hero's name,\n".format(i + 1))
        time.sleep(0.5)
        if hero_name == "":  # blank name is invalid
            print("Blank name is not accepted.\n")
            time.sleep(0.5)
            continue
        elif hero_name in namelist:  # hero can't have the same name
            print("Other already has the same name.\n")
            time.sleep(0.5)
        else:  # valid name input
            newgame.heros.append(Hero(hero_name))  # add hero to BoardGame
            namelist.append(hero_name)
            break

weapon_csv_read = open('weapon.csv', 'rt')  # load weapon list from weapon.csv file
csvin = csv.reader(weapon_csv_read)
weapon_equips_stk = []
for row in csvin:
    name, price, attack, defense = row[0], int(row[1]), int(row[2]), int(row[3])
    weapon_equips_stk.append(Equipment(name, price, attack, defense))
weapon_csv_read.close()

helmet_csv_read = open('helmet.csv', 'rt')  # load helmet list from helmet.csv file
csvin = csv.reader(helmet_csv_read)
helmet_equips_stk = []
for row in csvin:
    name, price, attack, defense = row[0], int(row[1]), int(row[2]), int(row[3])
    helmet_equips_stk.append(Equipment(name, price, attack, defense))
helmet_csv_read.close()

shield_csv_read = open('shield.csv', 'rt')  # load shield list from armor.csv file
csvin = csv.reader(shield_csv_read)
shield_equips_stk = []
for row in csvin:
    name, price, attack, defense = row[0], int(row[1]), int(row[2]), int(row[3])
    shield_equips_stk.append(Equipment(name, price, attack, defense))
shield_csv_read.close()

armor_csv_read = open('armor.csv', 'rt')  # load armor list from weapon.csv file
csvin = csv.reader(armor_csv_read)
armor_equips_stk = []
for row in csvin:
    name, price, attack, defense = row[0], int(row[1]), int(row[2]), int(row[3])
    armor_equips_stk.append(Equipment(name, price, attack, defense))
armor_csv_read.close()

map_csv_read = open('map.csv', 'rt')  # load map from map.csv file
csvin = csv.reader(map_csv_read)

for row in csvin:
    if row[0] == "Castle":  # castle blocks
        name, loc, price = row[1], int(row[2]), int(row[3])
        newgame.board.append(Castle(name, loc, price))  # add all the 36 blocks

    elif row[0] == "Market":  # market blocks
        name, loc = row[1], int(row[2])
        market = Market(name, loc)

        if name == "Weapon":  # weapon market
            market.equips_stk = weapon_equips_stk

        elif name == "Helmet":  # helmet market
            market.equips_stk = helmet_equips_stk

        elif name == "Shield":  # shield market
            market.equips_stk = shield_equips_stk

        elif name == "Armor":  # armor market
            market.equips_stk = armor_equips_stk

        newgame.board.append(market)

    elif row[0] == "Arena":  # arena blocks
        name, loc = row[1], int(row[2])
        newgame.board.append(Arena(name, loc))

    else:  # monolith blocks
        name, loc, next_loc = row[1], int(row[2]), int(row[3])
        newgame.board.append(Monolith(name, loc, next_loc))

map_csv_read.close()

# play the game

while True:  # play until sys.exit()
    newgame.round_step()  # run one round of the board game
    newgame.round_check()  # check after each round
