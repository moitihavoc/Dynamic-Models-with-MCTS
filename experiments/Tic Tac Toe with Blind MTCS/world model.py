class LearnedWorldModel:
    def __init__(self):
        self.transitions = {} # (state, action) -> next_state
        self.outcomes = {}    # (state, action) -> (reward, is_over)

    def update(self, s, a, s_next, r, done):
        self.transitions[(s, a)] = s_next
        self.outcomes[(s, a)] = (r, done)  

    def predict(self, s, a):
        return self.transitions.get((s, a)), self.outcomes.get((s, a))