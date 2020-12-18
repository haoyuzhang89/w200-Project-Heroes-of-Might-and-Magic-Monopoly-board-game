# '''Function modules'''

def hero_search(name, heros):
    """Input hero's name (string), heros list. output hero(class Hero) owns the name"""

    for hero in heros:
        if hero.name == name:
            return hero
            break
    else:
        return None  # if there is no one matches, return None
