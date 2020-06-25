import random

class CardPool:
    def __init__(self, noOfDecks):
        self.HOUSE = ({'Clubs':'C', 'Diamond':'D', 'Hearts':'H', 'Spades':'S'})
        self.SUITE = ({'2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10, 'A':11})
        self.unPlayed = []
        self.played = []
        self.deck = {}
        self.cardsInPlay = 0
        for n in range(0,noOfDecks,1):
            for house in self.HOUSE:
                for card in self.SUITE:
                    self.deck[str(self.cardsInPlay)] ={'marker': self.HOUSE[house]+card, 'played' : False, 'player' : "", 'points': self.SUITE[card]}
                    self.unPlayed.append(self.cardsInPlay)
                    self.cardsInPlay+=1

    
    ## UPDATE METHODS
    
    def AssignCard(self, player):
        card = random.randint(0,len(self.unPlayed)-1)
        card = self.unPlayed[card]
        
        if not self.deck[str(card)]['played']:
            self.deck[str(card)]['played'] = True
            self.deck[str(card)]['player'] = player

            self.unPlayed.remove(card)
            self.played.append(card)

            return self.deck[str(card)]['marker'],self.deck[str(card)]['points']
        else:
            print("ERROR in assignCard!")
            return -1
        
    def RefreshPool(self):
        for card in self.deck:
            self.deck[card]['played'] = False
            self.deck[card]['player'] = ""
    
    ## GET METHODS
        
    def GetPoints(self, cardId):
        return self.deck[cardId]['points']
    
    def GetMarker(self, cardId):
        return self.deck[cardId]['marker']
    
    def GetDeck(self):
        temp = {
            'Unplayed': self.unPlayed,
            'Played': self.played
        }
        return temp
    
    ## SHOW METHODS
    
    def ShowDeck(self):
        print(self.cardsInPlay)
        print("CardPool:")
        for x in self.deck:
            print(self.deck[x])
        print("Unplayed:")
        for x in self.unPlayed:
            print(x,end=",")
        print("\b\nPlayed:",)
        for x in self.played:
            print(x,end=",")
        if len(self.played) > 0:
            print("\b")
        else:
            print()
