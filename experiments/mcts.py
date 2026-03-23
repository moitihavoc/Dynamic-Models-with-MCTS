# implements the mcts algorithm itself.

import math
import random
from tic_tac_toe import Board
from copy import deepcopy

class TreeNode:
    def __init__(self, board: Board,  action = None, parent = None ): #(b, move, empty or self)
        self.b = board
        self.board_state = board.state
        self.visits = 0
        self.score = 0
        self.player = 2 # machine
        self.action = action # move that lead to this state
        self.parent = parent # parent node
        self.children = []
        self.untried_actions: list = board.action
        self.wins = 0.0

    def expand(self):
        move = self.untried_actions.pop()
        new_state = deepcopy(self.board_state)
        new_state[move[0]][move[1]] = self.player
        child = TreeNode(self.b, move, self)
        self.children.append(child)

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
            winner = self.b.check_winner_state()
            if winner is not None:
                return winner
            actions = new_b.action
            move = random.choice(actions)
            new_b.play_turn(move)
            new_b.alternate_turn()
    
    def backpropagate(self, winner):
        self.visits += 1

        if winner is None:
            self.wins += 0.5
        elif self.b.winner == 2:
            self.wins += 1.0

        if self.parent:
            self.parent.backpropagate(winner)
        
        
def mcts_search(root_state, iterations = 500):
    root = TreeNode(root_state)

    for _ in range(iterations):
        node = root

        if not node.is_terminal() and not node.is_fully_expanded():
            node.expand()
        
        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()
        
        winner = node.rollout()
        node.backpropagate(winner)
    
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

