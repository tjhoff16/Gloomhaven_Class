import random

class Modifier_deck(object):
    def __init__(self):
        self.deck=[]
        dist = [0,0,0,0,0,0,1,1,1,1,1,-1,-1,-1,-1,-1,2,-2,-1000,'*2']
        # dist = range(20)
        for ele in dist:
            self.deck.append(Modifier_card(ele))
        self.used=[]

    def draw(self, base_dam):
        random.shuffle(self.deck)
        results = []
        t2=False
        rolling = True
        special_effects = []
        tot_mod = 0
        print ("No Advantage or Disadvantage...")
        while rolling == True:
            ch = self.deck.pop()
            results.append(ch)
            self.used.append(ch)
            rolling = ch.rolling
            print ('rolling', rolling)
        for card in results:
            if type(card.mod) !=type(''):
                tot_mod += card.mod
            else:
                t2=True
            special_effects.append(card.special)
        if t2==True:
            tot_mod = tot_mod*2

        tot_mod += base_dam
        print ("You are doing {} damage".format(tot_mod))
        print ("Your attack has {} special effects:".format(len(special_effects)))
        print ('spec effects:', len(special_effects), special_effects)

    def draw_advantage(self, base_dam):
        random.shuffle(self.deck)
        results, results_2 = [], []
        t2=False
        rolling = True
        special_effects, special_effects_2 = [], []
        tot_mod, tot_mod_2= 0, 0

        print ("Advantage...")
        while rolling == True:
            choice_1 = self.deck.pop()
            self.used.append(choice_1)
            results.append(choice_1)
            rolling = choice_1.rolling
            print ('rolling', rolling)
        rolling = True

        while rolling == True:
            choice_2 = self.deck.pop()
            self.used.append(choice_2)
            results_2.append(choice_2)
            rolling = choice_2.rolling
            print ('rolling', rolling)

        for card in results:
            if type(card.mod) == type(tot_mod_2):
                tot_mod += card.mod
            else:
                t2=True
            special_effects.append(card.special)
        if t2==True:
            tot_mod = tot_mod*2

        t2=False
        for card in results_2:
            if type(card.mod) == type(tot_mod_2):
                tot_mod_2 += card.mod
            else:
                t2=True
            special_effects_2.append(card.special)
        if t2==True:
            tot_mod = tot_mod_2*2

        tot_mod += base_dam
        tot_mod_2 += base_dam

        print ('Stack 1 has {} special effects...'.format(len(special_effects)))
        print ('spec effects', special_effects)
        print ("Stack 1 total damage:", tot_mod)
        print ('Stack 2 has {} special effects...'.format(len(special_effects_2)))
        print ('spec effects', special_effects_2)
        print ("Stack 2 total damage:", tot_mod_2)

    def draw_disadvantage(self, base_dam):
        random.shuffle(self.deck)
        results, results_2 = [], []
        t2=False
        rolling = True
        special_effects, special_effects_2 = [], []
        tot_mod, tot_mod_2= 0, 0
        print ("Disadvantage...")
        while rolling == True:
            choice_1 = self.deck.pop()
            self.used.append(choice_1)
            results.append(choice_1)
            rolling = choice_1.rolling
            print ('rolling', rolling)
        rolling = True
        while rolling == True:
            choice_2 = self.deck.pop()
            self.used.append(choice_2)
            results_2.append(choice_2)
            rolling = choice_2.rolling
            print ('rolling', rolling)

        for card in results:
            if type(card.mod) == type(tot_mod_2):
                tot_mod += card.mod
            else:
                t2=True
            special_effects.append(card.special)
        if t2==True:
            tot_mod = tot_mod*2

        t2=False
        for card in results_2:
            if type(card.mod) == type(tot_mod_2):
                tot_mod += card.mod
            else:
                t2=True
            special_effects_2.append(card.special)

        if t2==True:
            tot_mod = tot_mod_2*2
        tot_mod += base_dam
        tot_mod_2 += base_dam

        print ('Stack 1 has {} special effects...'.format(len(special_effects)))
        print ('spec effects', special_effects)
        print ("Stack 1 total damage:", tot_mod)
        print ('Stack 2 has {} special effects...'.format(len(special_effects_2)))
        print ('spec effects', special_effects_2)
        print ("Stack 2 total damage:", tot_mod_2)

class Modifier_card(object):
    def __init__(self, mod, rolling=False, special=None):
        self.mod = mod
        self.special = special
        self.rolling=False

    def __str__(self):
        return "{} card, which has {} effects".format(self.mod,self.special)
d = Modifier_deck()

print (len(d.deck))

d.draw(1)
d.draw_advantage(1)
d.draw_disadvantage(1)

print (len(d.deck), len(d.used))
