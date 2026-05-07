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
        while not env.check_terminal():
            root_state = model.represent(env.state)
            available_actions = env.check_avail_actions()
            chosen_action = mcts_search(root_state, model, available_actions)
            reward:float = 0.0

            env.play_turn(chosen_action)
            env.alternate_turn()
            next_state = model.represent(env.state)

            if env.check_terminal():
                winner = env.check_winner_state()
                if winner == env.player:
                    reward = -1.0
                elif winner is None:
                    reward = 0.5
                reward = 1.0
            
            model.update_dynamics(root_state, chosen_action, next_state, reward)
            # model.save()
            
# add a play function, uses model.load() before playing





            

if __name__ == "__main__":
    train()