import random
import numpy as np
import itertools as it
from collections import Counter

allvalues = list(range(6,15))
allfaces = ['6','7','8','9','T','J','Q','K','A']
allsuits = ['C','D','H','S']
msuit = None

# class Game():
#     def __init__(self):
#         self.values = list(range(6,15))
#         self.suits = ['C','D','H','S']
#         self.msuit = ''







class Card():
    def __init__(self,suit=None,value=None,string=None):
        if string is not None:
            self.suit = string[-1]
            self.value = allfaces.index(string[0]) + 6
        elif suit is not None and value is not None:
            self.suit = suit
            self.value = value
        else:
            raise Error("invalid constructor arguments for Card.")


    def __eq__(self,other):
        return self.suit == other.suit and self.value == other.value

    def __hash__(self):
        return hash(str(self))

    def __str__(self):
        face = allfaces[self.value - 6]
        return face + self.suit

    def __repr__(self):
        return str(self)

    def __lt__(self,other):
        master = self.suit == msuit
        if self.suit == msuit:
            if other.suit == msuit:
                return self.value < other.value
            else:
                return False
        else:
            if other.suit == msuit:
                return True
            else:
                return self.value < other.value


    def __gt__(self,other):
        master = self.suit == msuit
        if self.suit == msuit:
            if other.suit == msuit:
                return self.value > other.value
            else:
                return True
        else:
            if other.suit == msuit:
                return False
            else:
                return self.value > other.value

    def istrump(self):
        return self.suit == msuit


    def beats(self,card):
        if self.suit == card.suit:
            return self > card
        elif self.istrump():
            return self > card
        else:
            return False



class Deck():
    def __init__(self):
        global msuit
        self.cards = [Card(suit,value) for suit,value in it.product(allsuits,allvalues)]
        self.cards = random.sample(self.cards,len(self.cards))
        self.msuit = self.cards[-1].suit
        msuit = self.msuit
        self.bitapile = []


    def __str__(self):
        return str(self.cards)

    def draw(self):
        return self.cards.pop()



def dump_func(func):
    def echo_func(*func_args, **func_kwargs):
        if func_kwargs:
            print('{}({},{})'.format(func.__name__,func_args,func_kwargs))
        else:
            print('{}({})'.format(func.__name__,func_args))

        return func(*func_args, **func_kwargs)
    return echo_func

class Player():
    playernum = 0
    def __init__(self,deck):
        self.hand = [deck.draw() for _ in range(6)]
        self.yard = {}
        self.playernum = Player.playernum
        Player.playernum += 1

    def __str__(self):
        return "P" + str(self.playernum)

    def __repr__(self):
        return str(self)

    @dump_func
    def initial_attack(self,defender):

        # check if we have two or more of the same card. If so, just play those two.those
        values = Counter([card.value for card in self.hand])
        value,count = values.most_common()[0]
        if count >= 2:
            cards = [card for card in self.hand if card.value == value]
            self.place_attack_cards_down(cards,defender)
            return len(cards)
        else:
            card = min(self.hand)
            self.place_attack_cards_down([card],defender)
            return 1

    @dump_func
    def addon_attack(self,defender):
        yardfaces = set(card.value for card in it.chain.from_iterable(defender.yard.items()))
        handfaces = set(card.value for card in self.hand)
        playablefaces = handfaces.intersection(yardfaces)
        playcardlimit = len(defender.hand)

        candidates = [card for card in self.hand if card.value in playablefaces]
        num = len(candidates) if len(candidates) < playcardlimit else playcardlimit
        options = list(it.combinations(candidates,num))

        option = random.choice(options)
        self.place_attack_cards_down(option,defender)

    @dump_func
    def place_attack_cards_down(self,cards,defender):
        for card in cards:
            self.hand.remove(card)
            defender.yard[card] = None

    @dump_func
    def take_cards(self):
        for card,beatcard in self.yard.items():
            self.hand.append(card)
            if beatcard is not None:
                self.hand.append(beatcard)

        self.yard = {}


    @dump_func
    def choose_option(self,options):
        option = min(
            options,
            key=lambda x: sum([card.value for card in self.hand if card not in x])
        )
        return option

    @dump_func
    def defend(self):

        candidates = {card:[] for card,beatcard in self.yard.items() if beatcard is None}

        for card1 in candidates:
            for card2 in self.hand:
                if card2.beats(card1):
                    candidates[card1].append(card2)


        options = [s for s in (it.product(*candidates.values())) if len(set(s)) == len(s)]


        option = self.choose_option(options)



        # if we choose to take
        if option == False:
            return False

        for cardtobeat,beatingcard in zip(candidates.keys(),option):
            self.yard[cardtobeat] = beatingcard
            self.hand.remove(beatingcard)

        return True











        
        




# Game object can possess these properties/attributes:
#   Master Suit
#   Deck
#   Players and their hands
#   Turn
#   Perfect knowledge of what has been played/who took what
#   Probabilities for different cards



deck = Deck()
players = [Player(deck) for _ in range(3)]

force_hands = [
    ["QH", "8C", "6H", "8H", "7C", "8S"], 
    ["TD", "9S", "AH", "QC", "KS", "KC"], 
    ["JS", "9H", "AS", "TC", "7H", "8D"]
]

for player,hand in zip(players,force_hands):
    player.hand = [Card(string=card) for card in hand]

msuit = "H"


print("Master Suit: {}".format(msuit))


turn = 0
attacker = players[turn]
defender = players[(turn+1) % len(players)]

limit = len(defender.hand)
limit -= attacker.initial_attack(defender)




while(True):

    bita=True
    skipped = False


    defended = defender.defend()
    if (not defended):
        skipped = True
        defender.take_cards()
        break



    else:
        morecards = False
        for player in players:
            if player != defender:
                numcards = player.addon_attack(defender)
                if numcards:
                    morecards = True
                    limit -= numcards

        if not morecards:
            bita = True


    if (bita):
        break

