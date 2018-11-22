import random
import numpy as np
import itertools as it
import colorama
from collections import Counter
from card import *
from utils import *

allvalues = list(range(6,15))
allsuits = ['C','D','H','S']
allfaces = ['6','7','8','9','T','J','Q','K','A']

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
        return colorama.Fore.GREEN + face + self.suit + colorama.Fore.RESET

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

    def __repr__(self):
        return str(self)

    def draw(self):
        return self.cards.pop()



# def dump_func(func):
#     def echo_func(*func_args, **func_kwargs):
#         if func_kwargs:
#             print('{}({},{})'.format(func.__name__,func_args,func_kwargs))
#         else:
#             print('{}({})'.format(func.__name__,func_args))

#         return func(*func_args, **func_kwargs)
#     return echo_func

@decorate_class_functions(debug_func)
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

    def draw_cards(self,deck):
        num_to_draw = 6 - len(self.hand)
        if num_to_draw > 0:
            try:
                for _ in range(num_to_draw):
                    self.hand.append(deck.draw())
                return False
            except:
                return True
        else:
            return False


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

    def addon_attack(self,defender):
        yardfaces = set(card.value for card in it.chain.from_iterable(defender.yard.items()) if card is not None)
        handfaces = set(card.value for card in self.hand)
        playablefaces = handfaces.intersection(yardfaces)
        playcardlimit = len(defender.hand)

        candidates = [card for card in self.hand if card.value in playablefaces]
        num = len(candidates) if len(candidates) < playcardlimit else playcardlimit
        options = list(it.combinations(candidates,num))

        if len(options) == 0:
            return 0
        else:
            option = random.choice(options)
            self.place_attack_cards_down(option,defender)
            return len(option)

    def place_attack_cards_down(self,cards,defender):
        for card in cards:
            self.hand.remove(card)
            defender.yard[card] = None


    def place_defending_cards_down(self,option):
        cardstobeat = [card for card,beatcard in self.yard.items()if beatcard is None]
        for cardtobeat,beatingcard in zip(cardstobeat,option):
            self.yard[cardtobeat] = beatingcard
            self.hand.remove(beatingcard)

    def take_cards(self):
        for card,beatcard in self.yard.items():
            self.hand.append(card)
            if beatcard is not None:
                self.hand.append(beatcard)

        self.yard = {}


    def transfer_to_bita(self,deck):
        for card in it.chain.from_iterable(self.yard.items()):
            deck.bitapile.append(card)
        self.yard = {}


    def choose_option(self,options):
        option = min(
            options,
            key=lambda x: sum([card.value for card in self.hand if card not in x])
        )
        return option

    def generate_playable_options(self):
        candidates = {card:[] for card,beatcard in self.yard.items() if beatcard is None}

        for card1 in candidates:
            for card2 in self.hand:
                if card2.beats(card1):
                    candidates[card1].append(card2)


        options = [s for s in (it.product(*candidates.values())) if len(set(s)) == len(s)]

        return options




    def defend(self):


        options = self.generate_playable_options()

        # if there are no options of how to beat, then you must take
        if len(options) == 0:
            self.take_cards()
            return False

        option = self.choose_option(options)
        
        # if the best option (despite there being a playable card) is to take
        if option == False:
            self.take_cards()
            return False

        self.place_defending_cards_down(option)

        return True










def check_winner(player):
    global turn
    global game_over
    if len(player.hand) == 0 and len(deck.cards) == 0:
        winners.append(player)
        print("{} is the {} place winner.".format(player,placestr(len(winners))))
        players.remove(player)
        turn -= 1

        if len(players) == 1:
            game_over = True

        return True
    else:
        return False


        
        




# Game object can possess these properties/attributes:
#   Master Suit
#   Deck
#   Players and their hands
#   Turn
#   Perfect knowledge of what has been played/who took what
#   Probabilities for different cards

randomseed = random.randint(0,100)
print(randomseed)
# random.seed(62)


deck = Deck()
players = [Player(deck) for _ in range(3)]

# force_hands = [
#     ["QH", "8C", "6H", "8H", "7C", "8S"], 
#     ["TD", "9S", "AH", "QC", "KS", "KC"], 
#     ["JS", "9H", "AS", "TC", "7H", "8D"]
# ]

# for player,hand in zip(players,force_hands):
#     player.hand = [Card(string=card) for card in hand]

# msuit = "H"


print("Master Suit: {}".format(msuit))
for player in players:
    print("{}: {}".format(player,player.hand)) 
print('\n\n') 





#set up the round
game_over = False
turn = 0
current_round = 0
skipped = False
deck_empty = False
winners = []

while(True):
    if game_over:
        print("Winners: {}".format(winners))
        print("Durak: {}".format(players[0]))
        break
    print("\n\n\n==== ROUND {} ====".format(current_round))

    for player in players:
        print("{}: {}".format(player,player.hand))

    if skipped:
        turn += 1

    attacker = players[turn % len(players)]
    defender = players[(turn+1) % len(players)]

    turn += 1
    current_round += 1

    print("attacker: {}, defender: {}".format(attacker,defender))

    attacker.initial_attack(defender)
    check_winner(attacker)


    for player in players:
        if player == defender:
            continue
        numcards = player.addon_attack(defender)
        check_winner(player)
        if numcards:
            morecards = True

    while(True):
        print("{}: {}".format(cstr("Defender's yard","BLUE"),defender.yard))

        bita=False
        skipped = False

        defended = defender.defend()
        defender_won = check_winner(defender)

        if defender_won:
            defender.transfer_to_bita(deck)
            bita = True
            break

        if (not defended):
            skipped = True
            break

        else:
            morecards = False
            for player in players:
                if player != defender:
                    numcards = player.addon_attack(defender)
                    check_winner(player)
                    if numcards:
                        morecards = True

            if not morecards:
                bita = True


        if (bita):
            defender.transfer_to_bita(deck)
            break

    for player in players:
        deck_empty = player.draw_cards(deck)



