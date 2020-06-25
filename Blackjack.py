#!/usr/bin/env python
# coding: utf-8

# Python script to simulate a Blackjack game

from Cardpool import *
from Dealer import *
from HumanPlayer import *

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



if __name__=="__main__":
        
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

    
