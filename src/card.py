


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
