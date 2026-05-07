import random
from env import Board
from world_model import LearnedWorldModel
from mtcs import mcts_search

def train():
    env = Board()
    model = LearnedWorldModel()
    
    model.load()
    print("Start tic tac toe training.")
    
    for _ in range(1001): 
        env.__init__() # resets the board
        env.first_to_play()
        while not env.check_terminal():
            root_state = model.represent(env.state)
            available_actions = env.check_avail_actions()
            chosen_action = mcts_search(root_state, model, available_actions)
            reward:float = 0.0

            env.play_turn(chosen_action)
            moving_player = env.player

            if env.check_terminal():
                winner = env.check_winner_state()
                if winner == moving_player:
                    reward = 1.0 # player who just made the move won
                elif winner is None:
                    reward = 0.5 # draw
                else:
                    reward = -1.0 # lose
            
            next_state = model.represent(env.state)
            model.update_dynamics(root_state, chosen_action, next_state, reward)
            env.alternate_turn()
        model.save()
    model.save()
    print("Training successful.")
            
# add a play function, uses model.load() before playing

def play():
    model = LearnedWorldModel()
    b = Board()
    model.load()

    print("Game Starts!")
    # determines first player
    b.first_to_play()
    if b.player == 1:
        print("Random plays")
    if b.player == 2:
        print("Machine plays")

    while True:
        available_actions = b.check_avail_actions()
        print("Available moves: ")
        print(b.action)
        print()
        # i can make a deepcopy of parent node before playing the move

        if b.player == 1:
            move = random.choice(b.action)
            print(f"Random plays 1 at {move}")
        if b.player == 2:
            move = mcts_search(model.represent(b.state), model, available_actions)
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

        if b.check_terminal() or b.winner != None:
            if b.winner == None:
                print("Final Result: Draw")
            elif b.winner == 1:
                print("Final Result: random wins")
            else:
                print("Final Result: Machine wins")
            break

            

if __name__ == "__main__":
    train()
    play()