import numpy as np

class LearnedWorldModel:
    def __init__(self):
        self.transitions = {} # (state, action) -> next_state
        self.outcomes = {}    # (state, action) -> (reward, is_over)
    
    def represent(self, real_state: list[list[int]]) -> list[list[int]]:
        """
        conver the real state into a latent space ID, which is a tuple -> hashable by self.transitions
        flatten the current state, and return the id representation along with the current player
        """
        rep_state = tuple(np.array(real_state).flatten().tolist())
        return rep_state
        

    def dynamics(self, latent_state: tuple, action: tuple, is_done: bool) -> tuple:
         """
         query the dictionary for the input state and action
         if there is none, return none, the reward will 0 to be neutral
         otherwise, return the result including the new state, the according reward and the terminal status of the game

         i might give positive reward to unknown states
         """
         result = self.transitions.get((latent_state, action))
         reward = self.outcomes.get((latent_state, action), 0.0)

         if(result is None): return (None, 0)

         return (result, reward, is_done)
    
    def update_dynamics(self, latent_state: tuple, action: tuple, next_state: tuple, reward: float):
        """
        if the state is unknown to the dynamics, call this update function only when move is applied in the real environment
        the reward is either 1 for win, 0.5 for draw, -1 for lose, 0 for rest
        """
        self.transitions[(latent_state, action)] = next_state
        self.outcomes[(latent_state, action)] = reward

    def predict(self, latent_state: tuple, action: tuple) -> float:
        """predicts the reward for the future; 1 step ahead in this case
        if the next state is none, return 2 to encourage exploration
        if not, return the reward in the lookup table 

        predict the positive rewards for the unknown state here for the simulation: 2 for unknonw, 1 for win, 0 for rest
        also supposedly generate a policy value, but for tic tac toe, the policy is likely uniform for unknown child states and therefore not significant
        I decided to remove it
        """
        next_state = self.transitions.get(latent_state, action)
        if (next_state is None): return 2

        return self.outcomes.get(latent_state, action)