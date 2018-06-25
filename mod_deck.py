import random

class Modifier_deck(object):
    def __init__(self):
        self.deck=[]
        dist = [0,0,0,0,0,0,1,1,1,1,1,-1,-1,-1,-1,-1,2,-2,-1000,'*2']
        for ele in dist:
            self.deck.append(Modifier_card(ele))
        self.used=[]

    def draw(self, base_dam, adv=False, disadv=False):
        res=[]
        used = []
        # adv, disadv = False, False
        random.shuffle(self.deck)
        t2=False
        rolling = True
        special_effects = []
        if adv and disadv == False:
            while rolling == True:
                ch = self.deck.pop()
                res.append(ch)
                used.append(ch)
                rolling = ch.rolling
                print ('rolling', rolling)
            tot_mod = base_dam
            for card in res:
                if type(card.mod) !=type(''):
                    tot_mod += card.mod
                else:
                    t2=True
                special_effects.append(card.special)
            if t2==True:
                tot_mod = tot_mod*2

        elif adv == True:
            while rolling == True:
                ch1 = self.deck.pop()
                used.append(ch1)
                if ch1.mod > ch2.mod:
                    res.append(ch1)
                rolling = ch.rolling
                print ('rolling', rolling)
            while rolling == True:
                ch1 = self.deck.pop()
                used.append(ch1)
                if ch1.mod > ch2.mod:
                    res.append(ch1)
                rolling = ch.rolling
                print ('rolling', rolling)

            tot_mod = base_dam
            for card in res:
                if type(card.mod) !=type(''):
                    tot_mod += card.mod
                else:
                    t2=True
                special_effects.append(card.special)
            if t2==True:
                tot_mod = tot_mod*2

        elif disadv == True:
            while rolling == True:
                ch = self.deck.pop()
                res.append(ch)
                used.append(ch)
                rolling = ch.rolling
                print ('rolling', rolling)
            tot_mod = base_dam
            for card in res:
                if type(card.mod) !=type(''):
                    tot_mod += card.mod
                else:
                    t2=True
                special_effects.append(card.special)
            if t2==True:
                tot_mod = tot_mod*2

        print ('spec effects', len(special_effects), special_effects)
        if len(special_effects) == 1:
            print ('tot_mod', tot_mod)
            return tot_mod
        else:
            print ('tot_mod', tot_mod)
            return tot_mod, ' '.join(special_effects)

class Modifier_card(object):
    def __init__(self, mod, rolling=False):
        self.mod = mod
        self.special = None
        self.rolling=False
    def __str__(self):
        return "{} card, which has {} effects".format(self.mod,self.special)
d = Modifier_deck()

for card in d.deck:
    print (card)

res = d.draw(1)
print (res)
