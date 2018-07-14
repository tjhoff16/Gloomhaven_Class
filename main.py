import math
import json
import random
from mod_deck import *
import sys

class GH_Class(object):
    def __init__(self, cs):
        print ("Initializing class...")
        self.items,self.cards,self.lost_cards,self.discards,self.enchancements=[],[],[],[],[]
        self.equipped={"HEAD": None,"BODY": None,"LEG": None,"ARM": None,"ARM2": None, "POUCH":[]}
        pouch_items = int(math.ceil(cs['level']/2))

        print ("Gathering class info...")
        self.name = cs['name']
        self.hp = cs['hp_track'][cs['level']-1]
        self.perks=cs['perks']
        self.xp=cs['xp']
        self.level = cs['level']
        self.checks=cs['checks']
        self.gold = cs['gold']
        self.modifier_deck = Modifier_deck(cs['mod_deck_distribution'])

        print ("Gathering cards...")
        for card in cs['cards']:
            if card['card_taken'] == True:
                self.cards.append(Card(card))
        while len(self.cards) > cs['card_limit']:
            print ("You have {} cards".format(len(self.cards)), "choose a card to discard from your starting hand")
            for i,card in enumerate(self.cards):
                print (i, card)
            inp = int(input("Type a card's number to discard from your hand"))
            self.cards.pop(inp)

        # print ("Gathering items...")
        # for item in cs['items']:
        #     self.items.append(Item(item))
        # for item in self.items:
        #     print (item)
        #     item_equip = input("Would you like to equip this item? (y/n): ")
        #     if item_equip == 'y':
        #         if self.equipped[item.part] == None:
        #             self.equipped[item.part] = item
        #         elif item.part != "POUCH":
        #             print ("This slot has the already equipped item:", self.equipped[item.part])
        #             part_input = input("Are you sure you would like to replace this item? (y/n)")
        #             if part_input == 'y':
        #                 self.equipped[item.part] = item
        #         elif item.part == "POUCH" and len(self.equipped[item.part]) >= pouch_items:
        #             for i,item in enumerate(self.equipped[item.part]):
        #                 print (i, item)
        #             pouch_input = int(input("Which pouch item would you like to replace? (type a number): "))
        #             self.equipped[item.part][pouch_input] = item
        #         elif item.part == "POUCH":
        #             self.equipped[item.part].append(item)

        print ("Gathering enchancements...")
        for enhancement in cs['enchancements']:
            self.enchancements.append(Enhancement(enhancement))

        print ("Showing current class state...\n\n")
        print ("You are playing a level {} {}. You have {} health, {} gold and {} xp.".format(self.level, self.name, self.hp, self.gold, self.xp))
        for enhancement in self.enchancements:
            print ("You have the enhancement:", enhancement)
        for k,v in self.equipped.items():
            if len(k) < 2:
                print ("You have {} equipped in your {} slot".format(v, k))

    def current_cards(self):
        print ("You have the following cards in your hand...\n\n")
        for i,card in enumerate(self.cards):
            print (card)
            print ("\n")

    def current_discards(self):
        print ("You have the following discards...")
        for card in self.discards:
            print (card)

    def current_lost_cards(self):
        print ("You have the following discards...")
        for card in self.lost_cards:
            print (card)

    def long_rest(self):
        print ("Long Resting...")
        for i,card in enumerate(self.discards):
            print (i,card)
        inp = int(input("Type a card's number to lose it from your discards"))
        self.lost_cards.append(self.discards.pop(inp))
        self.cards = self.cards + self.discards
        self.hp += 2

    def short_rest(self):
        print ("Short Resting...")
        random.shuffle(self.discards)
        self.lost_cards.append(self.discards.pop())
        self.cards = self.cards + self.discards

    def play_cards(self):
        print ("Playing cards...")
        self.current_cards()
        card_choice_1 = int(input("Choose your first card (input a number): "))
        card_choice_2 = int(input("Choose your second card (input a number): "))
        card_choices = [self.cards.pop(card_choice_1), self.cards.pop(card_choice_2)]
        card_init = int(input("Which card is your initiative card? (type 1 or 2)"))
        print ("Your initiative is:", card_choices[card_init-1].initiative)
        for card in card_choices:
            print ("Your card is:", card)
            card_attack = int(input("How many attacks does this card have? (Input number)"))
            attacks = 0
            while attacks < card_attack:
                damage = int(input("What is the base damage of this attack? (input number)"))
                check_adv_disadv = int(input ("Does this attack have advantage(1) or disadvantage(2)?"))
                if check_adv_disadv == 1:
                    self.modifier_deck.draw_advantage(damage)
                elif check_adv_disadv == 2:
                    self.modifier_deck.draw_disadvantage(damage)
                else:
                    self.modifier_deck.draw(damage)

                attacks += 1
                print ("This was attack number:", attacks)
            card_lost = input("Is this card a lost card? (y/n) ")
            if card_lost == 'y':
                self.lost_cards.append(card)

    def change_hp(self, dam, cards=False):
        if cards == True:
            if len(self.cards) > 0:
                print ("You have the following cards in your hand...")
                for i,card in enumerate(self.cards):
                    print (i,card)

            elif len(self.discards) >= 2:
                random.shuffle(self.discards)
                self.lost_cards.append(self.discards.pop())
                self.lost_cards.append(self.discards.pop())
        else:
            self.hp += dam
            print ("You now have {} hp".format(self.hp))

    def change_xp(self, xp):
        self.xp += xp
        print ("You now have {} xp".format(self.xp))

    def change_gold(self, gold):
        self.gold += gold
        print ("You now have {} gold".format(self.gold))

    def reshuffle(self):
        self.modifier_deck.reshuffle()

class Enhancement(object):
    def __init__(self, en_json):
        self.e_card_name = en_json['e_card_name']
        self.e_card_half = en_json["e_card_half"]
        self.e_specifics = en_json["e_specifics"]

    def __str__(self):
        return "This is an enhancement on the {} half of the card {} with the effect {}".format(self.e_card_half, self.e_card_name, self.e_specifics)

class Card(object):
    def __init__(self, card_json):
        self.name=card_json['card_name']
        self.initiative=card_json['initiative']
        self.upper=card_json['upper_text']
        self.lower=card_json['lower_text']

    def __str__(self):
        return "{} with upper half:\n\n{},\n\nlower half\n\n{},\n\nand initiative {}".format(self.name, self.upper, self.lower, self.initiative)

class Item(object):
    def __init__(self, item_json):
        self.name = item_json['item_name']
        self.text = item_json['item_text']
        self.cost = item_json['item_cost']
        self.part = item_json['item_part']
        self.equipped = False

    def __str__(self):
        return "This is a {} with {} effect which costs {} gold and can be equipped on {}".format(self.name, self.text, self.cost, self.part)

# def set_in_cache(CACHE, gh_class):
#     cached_class = CACHE['classes'][gh_class]
#     # if gh_class.xp < cached_class['xp']:
#     cached_class['xp'] = gh_class.xp
#     cached_class['level'] = gh_class.level
#     cached_class['checks'] = gh_class.checks
#     cached_class['gold'] = gh_class.gold
#     cached_class['perks'] = gh_class.perks

    # with open(command, 'w') as cache_file:

if __name__ == '__main__':
    # command = None
    # command = sys.argv[1]
    command = "class_cache.json"
    class_CACHE = None
    if class_CACHE == None:
        with open(command, 'r') as cache_file:
            class_CACHE = json.loads(cache_file.read())

    print ("The following classes are available to choose from...")
    for clss in class_CACHE['classes'].keys():
        print (clss)
    class_choice_inp = input ("Which class would you like? ")
    current_class= GH_Class(class_CACHE['classes'][class_choice_inp])
    action = None
    actions = ["play cards", "long rest", "short rest", "change hp", "change xp", "change gold", "reshuffle modifier deck", "see current cards", "see current discards", "see current lost cards"]
    while action != "done":
        print ("What would you like to do:")
        for i,action in enumerate(actions):
            print (i,action)
        action = int(input("Your action is: "))
        print (actions[i])
        if action == 0:
            current_class.play_cards()
        elif action == 1:
            current_class.long_rest()
        elif action == 2:
            current_class.short_rest()
        elif action == 3:
            lose_cards = False
            dam_amt = input("How much damage/healing are you taking?")
            losing_cards = input ("Would you like to lose cards instead of taking damage? (y/n)")
            if losing_cards == 'y':
                lose_cards = True
            current_class.change_hp(dam_amt, lose_cards)
        elif action == 4:
            xp_input = input ("How much xp are you gaining or losing?")
            current_class.change_xp(xp_input)
        elif action == 5:
            gold_input = input("How much gold are you gaining or losing?")
            current_class.change_gold(gold_input)
        elif action == 6:
            current_class.reshuffle()
        elif action == 7:
            current_class.current_cards()
        elif action == 8:
            current_class.current_discards()
        elif action == 9:
            current_class.current_lost_cards()
        # elif action == "done":
        #     done_input = ("Are you sure you want to quit? (y/n)")
        #     if done_input == 'y':
        #
        #     else:
        #         action=None
