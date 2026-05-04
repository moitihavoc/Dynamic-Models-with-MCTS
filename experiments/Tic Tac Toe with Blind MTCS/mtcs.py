import world_model as wm
import math
# perform mcts based on what is in the dictionary

class TreeNode:
    def __init__(self, latent_state: tuple, parent: tuple = None):
        """
        use the latent state from the dictionary
        the children nodes is contained in another dictionary that map available action to latent states
        """
        self.state = latent_state
        self.parent = parent
        self.children: dict[tuple] = {}
        self.visit_count = 0
        self.treesearch_value = 0
        self.state_map: dict[tuple] # use the transition dictionary here

    def expand(self, available_actions: list[tuple]):
        """
        expand the children nodes of the state based on real available actions
        if the action in the given state results in a None by the dynamics function,

        the predict function will give it a value of a positive reward
        """

        if not self.children: # expand the node if it has no children
            for action in available_actions:
                if self.state_map.get((self.state, action)) is None:
                    self.children[action] = TreeNode(None)
                else: self.children[action] = TreeNode(self.state_map.get((self.state, action)))

    def pUCT(self, child, policy):
        """
        calculate the pUCT value of an action in a given state
        since i dont have a NN for prediction yet, the prior value will be 1/number of children
        constants: c1​=1.25,c2​=19652, but replace with c = 2 due to small simulation count 

        on other thoughts, since my prediction function is not a neural network, it should return priority instead of predicted reward. 
        It will return 2 for state that has not been explored; 1 for states with winning move; 0 with the remaining states

        the tree search value is the sum of predicted value + dynamic reward
        """
        c = 1.41 
        if child.visit_count == 0: return float('inf')
        exploitation = self.treesearch_value/self.visit_count
        exploration = c * math.sqrt(math.log2(self.visit_count)/child.visit_count) 
        return exploitation + exploration

    def select_best_action(self, policy):
        """
        select child with best pUCT
        if a child's visit count = 0, the puct can prioritize exploring that child thanks to the exploration term
        """
        return max(self.children.keys(), key=lambda a: self.pUCT(a, policy))

    def backpropagate(self, search_path: list, value: float):
        """
        update the tree search value and the visit count until reaching the root node
        """
        for node in reversed(search_path):
            node.visit_count += 1
            node.treesearch_value += value

            value = -value # so that it negates the opponent's action

def mcts_search(root_state: tuple, world_model: wm.LearnedWorldModel, available_actions: list,  iterations=500):
    root = TreeNode(root_state)

    # we get the available actions from the environment.
    for a in available_actions:
        root.children[a] = TreeNode(None, parent=root)
        

    for _ in range(iterations):
        node = root
        search_path = [node]
        value: float
        policy = 1/len(available_actions)


        while node.children:
            action = node.select_best_action(policy)
            next_state, reward = world_model.dynamics(node.state, action)
            predicted_value = world_model.predict(next_state, action)

            if next_state is None:
                value = predicted_value
                break

            node = node.children[action]
            search_path.append(node)

            if reward != 0:
                value = reward + predicted_value
                break
        else: value = 0

        if not node.children:
            node.expand(available_actions)
        
        node.backpropagate(search_path, value)
    
    return max(root.children, key=lambda a: root.children[a].visit_count)
