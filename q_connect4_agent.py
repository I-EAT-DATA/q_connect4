import random

from q_connect4 import Connect4

class QConnect4Agent(Connect4):

    def __init__(self, alpha=0.5, epsilon=0.1, q=dict()):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of the current board state
         - `action` is an int of the move made
        """
        self.q = q
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self, old_state, action, new_state, reward):
        """
        Update Q-learning model, given an old state, an action taken
        in that state, a new resulting state, and the reward received
        from taking that action.
        """
        old = self.get_q_value(old_state, action)
        best_future = self.best_future_reward(new_state)
        self.update_q_value(old_state, action, old, reward, best_future)

    def get_q_value(self, state, action):
        """
        Return the Q-value for the state `state` and the action `action`.
        If no Q-value exists yet in `self.q`, return 0.
        """

        return self.q[(tuple(state), action)] if (tuple(state), action) in self.q else 0

    def update_q_value(self, state, action, old_q, reward, future_rewards):
        """
        Update the Q-value for the state `state` and the action `action`
        given the previous Q-value `old_q`, a current reward `reward`,
        and an estiamte of future rewards `future_rewards`.

        Use the formula:

        Q(s, a) <- old value estimate
                   + alpha * (new value estimate - old value estimate)

        where `old value estimate` is the previous Q-value,
        `alpha` is the learning rate, and `new value estimate`
        is the sum of the current reward and estimated future rewards.
        """

        new_value_estimate = reward + future_rewards
        self.q[(tuple(state), action)] = old_q + self.alpha * ( new_value_estimate - old_q )

    def best_future_reward(self, state):
        """
        Given a state `state`, consider all possible `(state, action)`
        pairs available in that state and return the maximum of all
        of their Q-values.

        Use 0 as the Q-value if a `(state, action)` pair has no
        Q-value in `self.q`. If there are no available actions in
        `state`, return 0.
        """

        rewards = []

        for action in self.available_actions(state):
            if (tuple(state), action) in self.q:
                rewards.append(self.q[(tuple(state), action)])
            else:
                rewards.append(0)

        return max(rewards) if rewards else 0

    def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `i` to take.

        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).

        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.

        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """

        actions = self.available_actions(state)

        if epsilon and random.random() <= self.epsilon:
            return random.choice(list(actions))

        best_q_v = -float('inf')
        best_action = None

        for action in actions:
            q_v = 0
            if (tuple(state), action) in self.q:
                q_v = self.q[(tuple(state), action)]
            if q_v >= best_q_v:
                best_q_v = q_v
                best_action = action

        return best_action
