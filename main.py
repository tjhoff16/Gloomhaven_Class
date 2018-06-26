import math
import json
import random
import * from mod_deck

class GH_Class(object):
    def __init__(self, cs):
        print ("Initializing class...")
        self.items=[]
        self.cards=[]
        self.lost_cards=[]
        self.discards=[]
        self.enchancements=[]
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

        print ("Gathering cards...")
        for card in cs['cards']:
            if card['card_taken'] == "True":
                self.cards.append(Card(card))
        while len(self.cards) > cs['card_limit']:
            print ("You have {} cards".format(len(self.cards)), "choose a card to discard from your starting hand")
            for i,card in enumerate(self.cards):
                print (i, card)
            inp = int(input("Type a card's number to discard from your hand"))
            self.cards.pop(inp)

        print ("Gathering items...")
        for item in cs['items']:
            self.items.append(Item(item))
        for i,item in enumerate(self.items):
            print (i, item)
            item_equip = input("Would you like to equip this item? (y/n): ")
            if item_equip == 'y':
                if self.equipped[item.part] == None:
                    self.equipped[item.part] = item
                elif item.part != "POUCH":
                    print ("This slot has the already equipped item:", self.equipped[item.part])
                    part_input = input("Are you sure you would like to replace this item? (y/n)")
                    if part_input == 'y':
                        self.equipped[item.part] = item
                elif item.part == "POUCH" and len(self.equipped[item.part]) >= pouch_items:
                    for i,item in enumerate(self.equipped[item.part]):
                        print (i, item)
                    pouch_input = int(input("Which pouch item would you like to replace? (type a number): "))
                    self.equipped[item.part][pouch_input] = item
                elif item.part == "POUCH":
                    self.equipped[item.part].append(item)

        print ("Gathering enchancements...")
        for enhancement in cs['enchancements']:
            self.enchancements.append(Enhancement(enhancement))

        print ("Showing current class state...")
        print ("You are playing a level {} {}. You have {} health, {} gold and {} xp.".format(self.level, self.name, self.gold, self.xp))
        for enhancement in self.enchancements:
            print ("You have the enhancement:", enhancement)
        for k,v in self.equipped.items():
            print ("You have {} equipped in your {} slot".format(v, k))

    def current_cards(self):
        print ("You have the following cards in your hand...")
        for card in self.cards:
            print (card)

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
        for i,card in enumerate(self.cards):
            print(i, card)
        card_choice_1 = input("Choose your first card (input a number): ")
        card_choice_2 = input("Choose your second card (input a number): ")
        card_choices = [self.cards.pop(card_choice_1), self.cards.pop(card_choice_2)]
        card_init = input("Which card is your initiative card? (type 1 or 2)")
        print ("Your initiative is:", card_choices[card_init-1].initiative)
        for card in card_choices:
            print ("Your card is:", card)
            card_lost = input("Is this card a lost card? (y/n) ")
            if card_lost == 'y':
                self.lost_cards.append(card)

    def change_hp(self, dam, cards=False):
        if cards = True:
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

    def add_xp(self, xp):
        self.xp += xp
        print ("You now have {} xp".format(self.xp))

    def add_gold(self, gold):
        self.gold += gold
        print ("You now have {} gold".format(self.gold))

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
        return "{} with upper half: {}, lower half {}, and initiative {}".format(self.name, self.upper, self.lower, self.initiative)

class Item(object):
    def __init__(self, item_json):
        self.name = item_json['item_name']
        self.text = item_json['item_text']
        self.cost = item_json['item_cost']
        self.part = item_json['item_part']
        self.equipped = False

    def __str__(self):
        return "This is a {} with {} effect which costs {} and can be equipped on {}".format(self.name, self.text, self.cost, self.part)
