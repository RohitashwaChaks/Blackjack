class Participant:
    def __init__(self):
        self.cardsHeld = []
        self.totalPoints = 0
        self.bustScore = 21      #   score at which player busts
        self.playState = True    #   False: Standing; True: Playing
        
    
    def GetHandDetails(self):
        temp = {
            'Cards Held': self.cardsHeld,
            'Points': self.totalPoints,
        }
        return temp
    
    def CheckBusted(self):
        if self.totalPoints > self.bustScore:
            return True
        return False
    
    def Hit(self, cardMarker, cardPoints):
        if self.playState:      #if-else redundant
            self.cardsHeld.append(cardMarker)
            self.totalPoints += cardPoints
            #print("Card Added:",cardMarker,"; Card Points:",cardPoints)
            if self.CheckBusted():
                self.Stand()
            return self.totalPoints
            #returns total Points after the hit
        else:
            return self.Stand()
    
    def Stand(self):
        self.playState = False
        return self.totalPoints
    
    def Show(self):
        return self.totalPoints
    
    def RefreshHand(self):
        self.cardsHeld = []
        self.totalPoints = 0
        self.playState = True
        return 0
