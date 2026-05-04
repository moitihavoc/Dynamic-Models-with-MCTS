from env import Board
from world_model import LearnedWorldModel
from mtcs import mcts_search

def train():
    env = Board()
    model = LearnedWorldModel()
    
    print("Start tic tac toe Training...")
    
    for _ in range(1001): 
        curr_player = env.first_to_play()
        env.__init__() # resets the board
        while True:
            root_state = model.represent(env.state)
            available_actions = env.check_avail_actions()
            chosen_action = mcts_search(root_state, model, available_actions)

            env.play_turn(chosen_action)
            winner = env.check_winner_state()

            if env.check_terminal():
                winner = env.check_winner_state()




            

if __name__ == "__main__":
    train()