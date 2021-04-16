import math
import random
import time

class Connect4():

    def __init__(self):
        """
        Initialize game board.
        Each game board has
            - `board`: the state of the game
            - `player`: whoever is currently playing
            - `winner`: the winner of the game once there is one
        """
        self.board = [' ' for sq in range(42)]
        self.player = 0
        self.result = None

    def available_actions(self, state):
        """
        Connect4.available_actions(state) takes a `state` list as input
        and returns all of the available actions `i` in that state.

        Action `i` represents placing a chip in `i` column.
        """
        return [sn for sn in range(7) if state[sn] == ' ']

    def other_player(self, player):
        """
        Connect4.other_player(player) returns the player that is not
        `player`. Assumes `player` is either 0 or 1.
        """
        return 0 if player == 1 else 1

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = self.other_player(self.player)

    def is_tie(self):
        """
        Check if the current state of `board` is tie  
        """
        return len([sq for sq in self.board if sq == ' ']) == 0

    def terminal(self):
        """
        Check if the current state of `board` is terminal
        """
        row = 0
        for sq in range(42):
            if sq % 7 == 0:
                row += 1

            distance_to_new_row = 7 * row - (sq + 1)
            distance_to_column_end = [i for i in range(6) if (sq + 1) + i * 7 > 35][0]

            if self.board[sq] == ' ':
                continue

            # 4 horizontally
            if distance_to_new_row >= 3 and self.board[sq] == self.board[sq + 1] and self.board[sq] == self.board[sq + 2] and self.board[sq] == self.board[sq + 3]:
                return True
            # 4 vertically
            elif distance_to_column_end > 2 and self.board[sq] == self.board[sq + 7] and self.board[sq] == self.board[sq + 14] and self.board[sq] == self.board[sq + 21]:
                return True
            # 4 diagonally
            elif distance_to_new_row >= 3 and distance_to_column_end >= 2 and sq + 24 < len(self.board) and self.board[sq] == self.board[sq + 8] and self.board[sq] == self.board[sq + 16] and self.board[sq] == self.board[sq + 24]:
                return True
            elif distance_to_new_row >= 3 and distance_to_column_end <= 2 and 0 <= sq - 18 < len(self.board) and self.board[sq] == self.board[sq - 6] and self.board[sq] == self.board[sq - 12] and self.board[sq] == self.board[sq - 18]:
                return True

    def move(self, action):
        """
        Make the move `action` for the current player.
        `action` must be an int `i`.
        """

        # Update board
        for r in range(6):
            current_sq = action + 35 - r * 7
            if self.board[current_sq] == ' ':
                self.board[action + 35 - r * 7] = self.player
                break

        self.switch_player()

        # Check for a winner
        if self.terminal():
            self.result = self.player
        elif self.is_tie():
            self.result = -1


class QConnect4Agent(Connect4):

    def __init__(self, alpha=0.6, epsilon=0.2):
        """
        Initialize AI with an empty Q-learning dictionary,
        an alpha (learning) rate, and an epsilon rate.

        The Q-learning dictionary maps `(state, action)`
        pairs to a Q-value (a number).
         - `state` is a tuple of the current board state
         - `action` is an int of the move made
        """
        self.q = dict()
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
        # raise NotImplementedError

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
        # raise NotImplementedError

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
        # raise NotImplementedError

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

        if random.random() <= self.epsilon:
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
        # raise NotImplementedError


def train(n):
    """
    Train an AI by playing `n` games against itself.
    """

    player = QConnect4Agent()

    # Play n games
    for i in range(n):
        print(f"Playing training game {i + 1}")
        game = Connect4()

        # Keep track of last move made by either player
        last = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        # Game loop
        while True:

            # Keep track of current state and action
            state = game.board.copy()
            action = player.choose_action(game.board)

            # Keep track of last state and action
            last[game.player]["state"] = state
            last[game.player]["action"] = action

            # Make move
            game.move(action)
            new_state = game.board.copy()

            # When game is over, update Q values with rewards
            if game.result is not None:
                player.update(state, action, new_state, -1)
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    1
                )
                break

            # If game is continuing, no rewards yet
            elif last[game.player]["state"] is not None:
                player.update(
                    last[game.player]["state"],
                    last[game.player]["action"],
                    new_state,
                    0
                )

    print("Done training")

    # Return the trained AI
    return player


def play(ai, human=None):
    """
    Play human game against the AI.
    `human_player` can be set to 0 or 1 to specify whether
    human player moves first or second.
    """

    # If no player order set, choose human's order randomly
    if human is None:
        human = random.randint(0, 1)

    # Create new game
    game = Connect4()

    # Game loop
    while True:

        # Print the board
        for l in range(0, 42, 7):
            row = ''.join([f"{game.board[l + i]}|" for i in range(7)])
            print(row[:13])
            print('-+-+-+-+-+-+-')

        # Get actions
        actions = game.available_actions(game.board)
        time.sleep(1)

        print(game.player, human)

        # Let human make a move
        if game.player == human:
            print("Your Turn")
            while True:
                column = int(input().strip()) - 1
                
                if not column in actions:
                    print('That place is already filled or invalid. Still your move.')
                else:
                    break

        # Have AI make a move
        else:
            print("AI's Turn")
            column = ai.choose_action(game.board, epsilon=False)
            print(f"AI chose to take put a chip in column {column}.")

        # Make move
        game.move(column)

        # Check for winner
        if game.result is not None:
            print("\nGAME OVER\n")
            winner = "Human" if game.result == human else "AI"
            print(f"Winner is {winner}")
            break
            
    if input("Play again?\n").lower() == "y":
        play(ai)

ai = train(10000)

play(ai)