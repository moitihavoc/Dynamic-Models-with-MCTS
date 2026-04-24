class Board:
    def __init__(self):
        # player: the machine will play as 2, human player will play 1
        # action: list of available moves, each move is a list of [row, column]
        # state: a 3x3 list representing the state of the board
        self.player: int
        self.action: list = []
        self.winner = 2
        self.state = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]  
    
    def first_to_play(self):
        # randomly determine which player goes first
        self.player = random.choice([1,2])

    def alternate_turn(self):
        # alternate between players' turns
        self.player = 1 if self.player == 2 else 2

    def check_avail_actions(self):
        # check available actions by checking which cell is 0
        self.action = [] 
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    self.action.append((i, j))
        return self.action

    def check_terminal(self):
        # check for terminal state by checking number of available actions
        if len(self.action) == 0:
            return True
        else:
            return False
        
    def check_winner_state(self):
        # check for winning conditions and return 1 or 2 or None depending on who wins
        for i in range(3): # check for 3 in a row for vertical and horizontal lines
            if self.state[i][0] == self.state[i][1] == self.state[i][2] != 0:
                return self.state[i][0]
            if self.state[0][i] == self.state[1][i] == self.state[2][i] != 0:
                return self.state[0][i]
        if self.state[0][0] == self.state[1][1] == self.state[2][2] != 0: # check for left to right diag
            return self.state[0][0]
        if self.state[0][2] == self.state[1][1] == self.state[2][0] != 0: # check for right to left diag
            return self.state[0][2]
        return None