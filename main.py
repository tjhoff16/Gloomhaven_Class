import math
import json

class GH_Class(object):
    def __init__(self, cs):
        print ("Gathering class info...")
        self.items=cs[]
        self.cards=[]
        self.lost_cards=[]
        self.discards=[]
        self.enchancements=[]
        self.equipped={"HEAD": None,"BODY": None,"LEG": None,"ARM": None,"ARM2": None, "POUCH":[]}
        pouch_items = int(math.ceil(cs['level']/2))
        
        self.name = cs['name']
        self.hp = cs['hp_track'][cs['level']-1]
        self.perks=cs['perks']
        self.xp=cs['xp']
        self.level = cs['level']
        self.checks=cs['checks']
        self.gold = cs['gold']

        for card in cs['cards']:
            if card['card_taken'] == "True":
                self.cards.append(Card(card))
        while len(self.cards) > cs['card_limit']:
            print ("You have {} cards".format(len(self.cards)), "choose a card to discard from your starting hand")
            for i,card in enumerate(self.cards):
                print (i, card)
            inp = int(input("Type a card's number to discard from your hand"))
            self.cards.pop(inp)

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
        for enhancement in cs['enchancements']:
            self.enchancements.append(Enhancement(enhancement))
        print ("You are playing a level {} {}. You have {} health, {} gold and {} xp.".format(self.level, self.name, self.gold, self.xp))
        for enhancement in self.enchancements:
            print ("You have the enhancement:", enhancement)


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

class Deck(object):
    def __init__(self):  # Don't need any input to create a deck of cards
        # This working depends on Card class existing above
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)  # appends in a sorted order

    def __str__(self):
        total = []
        for card in self.cards:
            total.append(card.__str__())
        # shows up in whatever order the cards are in
        return "\n".join(total)  # returns a multi-line string listing each card

    def pop_card(self, i=-1):
        return self.cards.pop(i)  # this card is no longer in the deck -- taken off

    def shuffle(self):
        random.shuffle(self.cards)

    def replace_card(self, card):
        card_strs = []  # forming an empty list
        for c in self.cards:  # each card in self.cards (the initial list)
            card_strs.append(c.__str__())  # appends the string that represents
            #that card to the empty list
        if card.__str__() not in card_strs:  # if the string representing this
        #card is not in the list already
            self.cards.append(card)  # append it to the list

    def sort_cards(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def deal_hand(self, hand_size):
        hand_cards = []
        for i in range(hand_size):
            hand_cards.append(self.pop_card(i))
        return hand_cards
