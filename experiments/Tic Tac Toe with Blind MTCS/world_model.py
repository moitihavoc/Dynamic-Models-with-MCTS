import numpy as np

class LearnedWorldModel:
    def __init__(self):
        self.transitions = {} # (state, action) -> next_state
        self.outcomes = {}    # (state, action) -> (reward, is_over)
    
    def represent(self, real_state: list[list[int]], curr_player: int) -> list[list[int]]:
        """
        conver the real state into a latent space ID, which is a tuple -> hashable by self.transitions
        flatten the current state, and return the id representation along with the current player
        """
        flat = np.array(real_state)
        rep_state = tuple(np.array(real_state).flatten().tolist())
        return (rep_state, curr_player)
        

    def dynamics(self, latent_state: tuple, action: tuple, is_done: bool) -> tuple:
         """
         query the dictionary for the input state and action
         if there is none, return none, the reward will 0.5 to be neutral
         otherwise, return the result including the new state, the according reward and the terminal status of the game
         """
         result = self.transitions.get((latent_state, action))
         reward = self.outcomes.get(latent_state, action)

         if(result == 0): return None

         return (result, reward, is_done)
    
    def update_dynamics(self, latent_state: tuple, action: tuple, next_state: tuple, reward: float):
        """
        if the state is unknown to the dynamics, call this update function only when move is applied in the real environment
        """
        self.transitions[(latent_state, action)] = next_state
        self.outcomes[(latent_state, action)] = reward

    def predict(self, latent_state: tuple, tuple: list) -> tuple:
        """
        query the dictionaries for the next state and expected reward
        """
        return self.transitions.get((latent_state, action)), self.outcomes.get((latent_state, action))