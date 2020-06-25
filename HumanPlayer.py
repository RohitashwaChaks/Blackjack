from Player import *

class Player(Participant):
    def __init__(self):
        super().__init__()
        self.name = input("Enter Player Name:")
        self.balance = int(input("Enter Balance for "+self.name+":"))
        self.bet = 0
        self.isBroke = False     #   False: Not Broke; True: Broke
        
    def GetDetails(self):
        temp = {
            'Name': self.name,
            'Cards Held': self.cardsHeld,
            'Points': self.totalPoints,
            'Balance': self.balance,
            'Bet': self.bet,
            'Broke': self.isBroke,
            'Busted': self.CheckBusted()
        }
        return temp
    
    def IsNotBroke(self):
        if self.balance <= 0:
            self.isBroke = True
            self.Stand()
            return False
        else:
            return True
        
    def PlaceBet(self):
        if self.IsNotBroke():
            while self.bet == 0:
                bid = int(input("Enter Bet for "+self.name+" this round:"))
                if bid <= self.balance and bid > 0:
                    self.bet = bid
                    self.balance -= self.bet
                    return self.bet
                else:
                    print("Insufficient Balance. Current Balance: ",self.balance)
        else:
            print("Player "+self.name+" Broke")
            return -1
        
    def Play(self, cardMarker = "", cardpoints = 0):
        if self.playState and not self.isBroke:
            if cardMarker != "" and cardpoints != 0:
                return self.Hit(cardMarker, cardpoints)
            else:
                return self.Stand()
        elif self.isBroke:
            print("Player "+self.name+" Broke")
            return -1
        elif not self.playState:
            print("Player "+self.name+" Standing")
            return self.Stand()
        else:
            print("ERROR in Play for",self.name)
            return -500
    
    def RoundEnds(self, isWin):
        #isWin: False = Loose Round; True = Win Round
        if isWin:
            self.balance += 2*self.bet            
        self.bet = 0
        self.RefreshHand()
        if self.balance == 0:
            self.isBroke = True
        return self.balance
