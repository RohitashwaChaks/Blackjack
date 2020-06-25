from Player import *

class Dealer(Participant):
    def __init__(self):
        super().__init__()
        self.threshold = 17
        
    def Play(self,cardMarker,cardPoints):
        if self.playState:
            if cardMarker != "" and cardPoints != 0:
                return self.Hit(cardMarker, cardPoints)
            else:
                return self.Stand()
        elif not self.playState:
            print("Dealer Standing")
            return self.Stand()
        else:
            print("ERROR in Play for Dealer")
            return -500
        return self.totalPoints
    
    def DealerShow(self):
        cards = self.GetHandDetails()['Cards Held'].copy()
        cards[1] = '*'
        print(cards)
        return 0
