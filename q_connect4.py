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

    def switch_player(self):
        """
        Switch the current player to the other player.
        """
        self.player = 0 if self.player == 1 else 1

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

        for r in range(6):
            current_sq = action + 35 - r * 7
            if self.board[current_sq] == ' ':
                self.board[action + 35 - r * 7] = self.player
                break

        if self.terminal():
            self.result = self.player
        elif self.is_tie():
            self.result = 2
        else:
            self.switch_player()