import pickle
import pandas as pd

class Minimax():

    def __init__(self, max_depth=4):

        self.max_depth = max_depth

        self.heuristic = [
            [0], [0], [0], [0], [0], [0], [0],
            [0], [0], [1, -1], [2, -2], [1, -1], [0], [0],
            [0], [0], [1, -2], [2, -2], [1, -2], [0], [0],
            [0], [0], [3, -2], [3, -2], [3, -2], [0], [0],
            [0], [0], [4, -3], [4, -3], [3, -3], [0], [0],
            [0], [1, -1], [3, -3], [4, -4], [3, -3], [1, -1], [0]
        ]

        self.model = pickle.load(open("../connect4-1/c4model.sav", 'rb'))

    def get_move(self, state):

        connect4_board = [' ' for i in range(42)]

        for sn, sv in enumerate(state):
            if sv == 0:
                connect4_board[sn] = 'R'
            elif sv == 1:
                connect4_board[sn] = 'B'

        turn = self.player(connect4_board)

        actions = self.actions(connect4_board)

        best_action = actions[0]
        values = []

        if turn == 'R':
            # max player

            local_best_min_v = -float('inf')

            for action in actions:
                self.current_depth = 0
                min_v = self.min_value(self.result(connect4_board, action))

                # print(f"Action: {action + 1}, Min Value: {min_v}")
                values.append(min_v)

                if min_v > local_best_min_v:
                    local_best_min_v = min_v
                    best_action = action

        else:
            # min player

            local_best_max_v = float('inf')

            for action in actions:
                self.current_depth = 0
                max_v = self.max_value(self.result(connect4_board, action))

                # print(f"Action: {action + 1}, Max Value: {max_v}")
                values.append(max_v)

                if max_v < local_best_max_v:
                    local_best_max_v = max_v
                    best_action = action
            
        return best_action, values

    def print_board(self, board):
        for l in range(0, 42, 7):
            row = ''.join([board[l + i] + '|' for i in range(7)])
            print(row[:13])
            print('-+-+-+-+-+-+-')

    def player(self, board):
        return 'B' if board.count('R') > board.count('B') else 'R'

    def is_tie(self, board):
        return len([sq for sq in board if sq == ' ']) == 0

    def utility(self, board):
        return 0 if self.is_tie(board) else -1000 if self.player(board) == "R" else 1000

    def terminal(self, board):
        # use modulo 7 to detect new row
        row = 0
        for sq in range(42):
            if sq % 7 == 0:
                row += 1

            distance_to_new_row = 7 * row - (sq + 1)
            distance_to_column_end = [i for i in range(6) if (sq + 1) + i * 7 > 35][0]

            if board[sq] == ' ':
                continue

            # 4 horizontally
            if distance_to_new_row >= 3 and board[sq] == board[sq + 1] and board[sq] == board[sq + 2] and board[sq] == board[sq + 3]:
                return True
            # 4 vertically
            elif distance_to_column_end > 2 and board[sq] == board[sq + 7] and board[sq] == board[sq + 14] and board[sq] == board[sq + 21]:
                return True
            # 4 diagonally
            elif distance_to_new_row >= 3 and distance_to_column_end >= 2 and sq + 24 < len(board) and board[sq] == board[sq + 8] and board[sq] == board[sq + 16] and board[sq] == board[sq + 24]:
                return True
            elif distance_to_new_row >= 3 and distance_to_column_end <= 2 and 0 <= sq - 18 < len(board) and board[sq] == board[sq - 6] and board[sq] == board[sq - 12] and board[sq] == board[sq - 18]:
                return True

        return self.is_tie(board)

    def actions(self, board):
        return [sn for sn in range(7) if board[sn] == ' ']

    def result(self, board, action):
        result = board[:]
        for r in range(6):
            current_sq = board[action + 35 - r * 7]
            if current_sq == ' ':
                result[action + 35 - r * 7] = self.player(board)
                break
        return result

    def evaluate(self, board):

        total_score = 0
        for vn, values in enumerate(self.heuristic):
            for value in values:
                if value < 0 and board[vn] == 'B':
                    total_score += value
                elif value > 0 and board[vn] == 'R':
                    total_score += value

        conv_data = []

        for sq in board:
            if sq.isdigit() or sq == ' ':
                conv_data.append(0)
            elif sq == 'R':
                conv_data.append(1)
            else:
                conv_data.append(-1)  

        c4_board = pd.Series(conv_data, index=[f"pos_{sn + 1}" for sn, sv in enumerate(board)])

        total_score += self.model.predict([c4_board])[0][0]

        return total_score

    def min_value(self, board):
        if self.terminal(board):
            return self.utility(board)

        if self.current_depth > self.max_depth:
            return self.evaluate(board)

        self.current_depth += 1
        v = float('inf')

        for action in self.actions(board):
            max_v = self.max_value(self.result(board, action))
            v = min(v, max_v)

        return v

    def max_value(self, board):
        if self.terminal(board):
            return self.utility(board)

        if self.current_depth > self.max_depth:
            return self.evaluate(board)

        self.current_depth += 1
        v = -float('inf')

        for action in self.actions(board):
            min_v = self.min_value(self.result(board, action))
            v = max(v, min_v)

        return v