# valueIterationAgents.py
# -----------------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*
        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount = 0.9, iterations = 100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.
          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0

        states = mdp.getStates()

        # Write value iteration code here
        "*** CS5368 YOUR CODE HERE ***"
        temp = 0
        for value in states:
            self.values[value] = 0
        while temp < self.iterations:
            n_value = self.values.copy()
            for value in states:
                if mdp.isTerminal(value):
                    n_value[value] = 0
                else:
                    m_value = []
                    for step in mdp.getPossibleActions(value):
                        QValue = self.computeQValueFromValues(value, step)
                        m_value.append(QValue)
                    n_value[value] = max(m_value)
            self.values = n_value
            temp += 1
        
    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]


    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** CS5368 YOUR CODE HERE ***"
        States = self.mdp.getTransitionStatesAndProbs(state, action)
        value = 0
        discount = self.discount
        for State, Probs in States:
            reward = self.mdp.getReward(state, action, State)
            qvalue = self.getValue(State)
            value += Probs * (reward + discount * qvalue)
        return value
        util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.
          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** CS5368 YOUR CODE HERE ***"
        Actions = self.mdp.getPossibleActions(state)
        value = util.Counter()
        if self.mdp.isTerminal(state):
            return None
        for possibleAction in Actions:
            value[possibleAction] = self.computeQValueFromValues(state, possibleAction)
        Action = value.argMax()
        return Action
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
