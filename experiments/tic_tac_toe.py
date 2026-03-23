# An environment where I attempt to get the AI to learn how to play Tic Tac Toe

import math
import random 
from copy import deepcopy

# Define the board in which the game takes place

class Board:
    def __init__(self):
        # the machine will play as O, human player will play X
        self.player: int
        self.action: list = []
        # represents the postions of a 3x3 game board, using indexes as positions
        # 1 = X, 2 = O
        self.state = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]  
    
    # randomly determine which player goes first
    def first_to_play(self):
        self.player = random.choice([1,2])
    
    # make changes to the board after a position is entered
    def play_turn(self, position:list):
        row = position[0]
        column = position[1]
        self.state[row][column] = self.player

    # alternate between players' turns
    def alternate_turn(self):
        self.player = 1 if self.player == 2 else 2

    # check available actions by checking which cell is 0
    def check_avail_actions(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0 and self.state[i][j] not in self.action:
                    self.action.append([i, j])
        return self.action

    # check for terminal state
    def check_terminal(self):
        if len(self.action) == 0:
            return True
        else:
            return False
        
    # check for winning conditions and return 1 or 2 or None depending on who wins
    def check_winner_state(self):
        for i in range(3):
            if self.state[i][0] == self.state[i][1] == self.state[i][2] != 0:
                return self.state[i][0]
            if self.state[0][i] == self.state[1][i] == self.state[2][i] != 0:
                return self.state[0][i]
        if self.state[0][0] == self.state[1][1] == self.state[2][2] != 0:
            return self.state[0][0]
        if self.state[0][2] == self.state[1][1] == self.state[2][0] != 0:
            return self.state[0][2]
        return None
    
    # TODO: implement handling if move input is not available

def main():
    print("Game Starts!")

    # determines first player
    b = Board()
    b.first_to_play()
    if b.player == 1:
        print("Human plays")
    if b.player == 2:
        print("Machine plays")

    while True:
        b.check_avail_actions()
        print("Available moves: ")
        print(b.action)
        print()

        if b.player == 1:
            move = list(map(int, input("Human's turn:").split()))
            print(f"Human plays 1 at {move}")
        if b.player == 2:
            move = list(map(int, input("Machine's turn:").split()))
            print(f"Machine plays 2 at {move}")
        b.play_turn(move)
        
        # print current state
        for r in b.state:
            print(r)
        print("\n")

        b.alternate_turn()
        winner = b.check_winner_state()

        # check if the game ends

        b.action.pop()
        if b.check_terminal() or winner != None:
            if winner == None:
                print("Final Result: Draw")
            elif winner == 1:
                print("Final Result: Human wins")
            else:
                print("Final Result: Machine wins")
            break

        b.action = [] # reset available moves


main()
