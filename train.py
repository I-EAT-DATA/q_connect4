from q_connect4_agent import QConnect4Agent
from q_connect4 import Connect4
from minimax import Minimax

def train(q_agent, n):
    """
    Train QAgent `q_agent` by having it play `n` games against itself
    """
    
    # opponent = Minimax(max_depth=20)
    # print("--- train", n)
    for i in range(n):
        # if (i + 1) % 100 == 0:
        #     print(f"Training game {i + 1}")
        # print(f"Training game {i + 1}")
        game = Connect4()

        prev_data = {
            0: {"state": None, "action": None},
            1: {"state": None, "action": None}
        }

        while True:

            state = game.board[:]

            action = q_agent.choose_action(game.board)

            # if game.player == 0:
            #     action = player.choose_action(game.board)
            # else:
            #     action, values = opponent.get_move(state)

            prev_data[game.player]["state"] = state
            prev_data[game.player]["action"] = action

            game.move(action)
            new_state = game.board[:]

            if game.result is not None:
                # print(f"Winner: {game.result}")
                q_agent.update(state, action, new_state, -1)
                # if the game is over the person whose turn it is must have won
                q_agent.update(prev_data[game.player]["state"], prev_data[game.player]["action"], new_state, 1)
                break
            elif prev_data[game.player]["state"] is not None:
                q_agent.update(prev_data[game.player]["state"], prev_data[game.player]["action"], new_state, 0)

    return q_agent.q