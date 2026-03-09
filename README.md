# Dynamic-Models-with-MCTS
Project: Dynamic Models for Real-Time Autonomous Decision Making in the Real World

# Objectives
- Implement MCTS simulation where policies adapts and changes in real-time to respond to the changing environment
- Integrate Dynamic Models to traditional MCTS
- Measure the performance of the aforementioned approaches
- Ultimately, a conference-style paper

# Description
**Monte Carlo Tree Search**(MCTS) Algorithm is heavily used in planning and simulation, with the main application being combinatorial games such as Chess, Go, Shogi,etc. The traditional version of the algorithms excels in these environments where there are zero-sum results, perfect information, uncertainty over rewards and discrete turns of actions. However, in realistic environments, the elements within can be highly stochastic, which can lead to infinite branching and overwhelm the Tree built by the algorithm. In addition, perfect information is rarely achieved in the real world and the zero-sum equilibrium breaks, resulting in the necessity of more complex single-agent optimization. A plausible suggestion to adapt the MCTS algorithm to this problem is the use of **Dynamic Models**. By enabling the policies to change in real-time with reinforment learning, in response to environmental changes, it is prospective that such a hybrid approach can enhance MCTS in solving stochastic control problems posed by real-world environments.

# Methodology