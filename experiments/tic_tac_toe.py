# An environment where I attempt to get the AI to learn how to play Tic Tac Toe

import random 
from copy import deepcopy
import math

# Define the board in which the game takes place

class Board:
    def __init__(self):
        # the machine will play as O, human player will play X
        self.player: int
        self.action: list = []
        self.winner = 2
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
        self.action = []  # clear list before adding
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
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
        

class TreeNode:
    def __init__(self, board: Board,  action = None, parent = None ): #(b, move, empty or self)
        self.b = deepcopy(board)  # each node gets its own board copy
        self.board_state = deepcopy(board.state)
        self.visits = 0
        self.score = 0
        self.player = 2 # machine
        self.action = action # move that lead to this state
        self.parent = parent # parent node
        self.children = []
        self.b.check_avail_actions()  # get available actions for this state
        self.untried_actions: list = deepcopy(self.b.action)  # copy the action list
        self.wins = 0.0

    def expand(self):
        move = self.untried_actions.pop()
        # Create a new board state with the move applied
        child_board = deepcopy(self.b)
        child_board.play_turn(move)
        child_board.alternate_turn()
        child = TreeNode(child_board, move, self)
        self.children.append(child)
        return child

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0
    
    def is_terminal(self):
        return self.b.check_winner_state() is not None or not self.b.action
    
    def ucb(self, child, c = 1.41):
        exploitation = child.wins/child.visits
        exploration = c * math.sqrt(math.log2(self.visits)/child.visits)
        return exploitation + exploration
    
    def best_child(self):
        for child in self.children:
            if child.visits == 0:
                return child
            
        return max(self.children, key=self.ucb)
    
    def rollout(self):
        new_b = deepcopy(self.b)

        while True:
            winner = new_b.check_winner_state()  # check simulated board, not original
            if winner is not None:
                return winner
            new_b.check_avail_actions()  # update available actions
            if not new_b.action:  # no moves available = draw
                return None
            move = random.choice(new_b.action)
            new_b.play_turn(move)
            new_b.alternate_turn()
    
    def backpropagate(self, winner):
        self.visits += 1

        if winner is None:
            self.wins += 0.5
        elif winner == 2:  # machine player
            self.wins += 1.0

        if self.parent:
            self.parent.backpropagate(winner)
        
        
def mcts_search(root_state, iterations = 500):
    root = TreeNode(root_state)

    for _ in range(iterations):
        node = root
        
        # Selection & Expansion phase
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()
        
        if not node.is_terminal():
            node = node.expand()  # expand returns the new child
        
        # Rollout phase
        winner = node.rollout()
        
        # Backpropagation phase
        node.backpropagate(winner)
    
    if not root.children:
        return None
    best = max(root.children, key=lambda c: c.visits)
    return best.action
    

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
        # i can make a deepcopy of parent node before playing the move

        if b.player == 1:
            move = list(map(int, input("Human's turn:").split()))
            print(f"Human plays 1 at {move}")
        if b.player == 2:
            move = mcts_search(b, 300)
            print(f"Machine plays 2 at {move}")
        # here, move can be used as action applied to parent node
        b.play_turn(move)
        
        # print current state
        for r in b.state:
            print(r)
        print("\n")

        b.alternate_turn()
        b.winner = b.check_winner_state()

        # check if the game ends

        b.action.pop()
        if b.check_terminal() or b.winner != None:
            if b.winner == None:
                print("Final Result: Draw")
            elif b.winner == 1:
                print("Final Result: Human wins")
            else:
                print("Final Result: Machine wins")
            break

        b.action = [] # reset available moves


main()