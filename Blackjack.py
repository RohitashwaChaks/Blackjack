#!/usr/bin/env python
# coding: utf-8

# Python script to simulate a Blackjack game

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

class Board():
    def __init__(self):
        self.leaderBoard = []
        self.roundStatus = 0 # roundStatus: 0 = round over; 1 = round underway
        
        self.playerCount = int(input("Enter the number of Players: "))
        self.deckCount = int(input("Enter the number of Decks: "))
        self.cardpool = CardPool(self.deckCount)
        #self.cardpool.showDeck()
        
        self.dealer = Dealer()
        
        self.players = {}
        for i in range(0,self.playerCount,1):
            temp = Player()
            self.players[temp.name] = temp
    
    def GetPlayerSummary(self):
        for player in self.players:
            print(self.players[player].GetDetails())
    
    def GetCardPool(self):
        self.cardpool.ShowDeck()
        
    def CheckWin(self):
        winner = []
        for player in self.players:
            if not self.dealer.CheckBusted():
                dealerScore = self.dealer.GetHandDetails()['Points']
                if not self.players[player].CheckBusted():
                    if self.players[player].GetHandDetails()['Points'] >= dealerScore:
                        winner.append(player) # Player is a winner if Neither Player nor Dealer busts and player score >= dealer score
            else:
                winner.append(player) # Everyone is a winner if Dealer Busts
        return winner
                
                
    
    def DistributeCards(self, noOfCards,player):
        for i in range(0,noOfCards,1):
            (marker, cardsPoint) = self.cardpool.AssignCard(player)
            if player != "Dealer":
                self.players[player].Play(marker,cardsPoint)
            else:
                self.dealer.Play(marker,cardsPoint)
        
    def BeginRound(self):
        self.roundStatus = 1
        
        # Players Dealt and Bet
        for player in self.players:
            #deal out cards
            print("\nNow Dealing:",player)
            self.DistributeCards(2,player)
                #print info about cards delt here
            print(self.players[player].GetHandDetails())
            #bet
            print("\nNow Betting:",player)
            self.players[player].PlaceBet()
            
        # Dealer Dealt
        print("\nDealer Cards:")
        self.DistributeCards(2,"Dealer")
        self.dealer.DealerShow()
        return 0
    
    def PlayRound(self):
        # Players Call
        for player in self.players:
            print("Playing:",player)
            while(self.players[player].playState):
                print(self.players[player].GetHandDetails())
                move = int(input("Stand (0) | Hit (1) :"))
                if move == 1:
                    (marker, cardsPoint) = self.cardpool.AssignCard(player)
                    self.players[player].Play(marker, cardsPoint)
                else:
                    self.players[player].Play()
            print("Final Status for "+player+":",self.players[player].GetHandDetails())
        return 0
    
    def EndRound(self):
        self.roundStatus = 0
        
        while(self.dealer.playState):
            if self.dealer.GetHandDetails()['Points'] >= self.dealer.threshold:
                self.dealer.playState = False
                break
            (marker, cardsPoint) = self.cardpool.AssignCard("Dealer")
            self.dealer.Play(marker, cardsPoint)
        print("Final Status for Dealer:",self.dealer.GetHandDetails())
        
        winner = self.CheckWin()
        
        print("Winners are:",winner)
        for player in self.players:
            self.players[player].RoundEnds(player in winner)
        
        self.dealer.RefreshHand()
        return 0
    
    def UpdateLeaderBoard(self):
        temp = []
        for player in self.players:
            if self.players[player].GetDetails()['Broke']:
                temp.append(player)
        for player in temp:
            del self.players[player]
            self.leaderBoard.append(player)
    
    def ShowLeaderBoard(self):
        self.leaderBoard.reverse()
        for i in range(0,len(self.leaderBoard),1):
            print("#",i+1,"->",self.leaderBoard[i])
    
    def CheckGameState(self):
        if len(self.leaderBoard)< self.playerCount:
            return True
        else:
            return False
        
    def RefreshCardPool(self):
        cardPoolStatus = self.cardpool.GetDeck()
        if len(cardPoolStatus['Unplayed']) < 4*self.playerCount:
            print("---- Refreshing Card Pool ----")
            self.cardpool.RefreshPool()
        return 0

#Initialising Game

board = Board()
players = []
for x in board.players:
    players.append(x)

board.GetPlayerSummary()

#Playing the Game
while(board.CheckGameState()):
    print()
    board.BeginRound()
    print()
    board.PlayRound()
    print()
    board.EndRound()
    print()
    board.GetPlayerSummary()
    print()
    board.UpdateLeaderBoard()
    print()
    board.RefreshCardPool()


# Results
board.ShowLeaderBoard()


# CardPool Status
board.GetCardPool()