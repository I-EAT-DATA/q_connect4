from q_connect4_agent import QConnect4Agent
from q_connect4 import Connect4
from minimax import Minimax

def play(q_agent, human=0, helper=False, helper_depth=20):
    """
    Play human game against the QAgent.
    `human` can be set to 0 or 1 to specify whether
    human moves first or second.
    """

    connect4 = Connect4()
    helper = Minimax(max_depth=helper_depth) if helper else None

    while True:

        for l in range(0, 42, 7):
            row = ''.join([f"{connect4.board[l + i]}|" for i in range(7)])
            print(row[:13])
            print('-+-+-+-+-+-+-')

        actions = connect4.available_actions(connect4.board)

        if connect4.player == human:
            print("Your Move.")

            while True:
                column = int(input().strip()) - 1
                
                if not column in actions:
                    print('That place is already filled or invalid. Still your move.')
                else:
                    break

            # column, values = helper.get_move(connect4.board)
        else:
            print("QAgent's Move.")

            if helper:
                action, values = helper.get_move(connect4.board)
                if values.count(1000) >= 1 or values.count(-1000) >= 1:
                    column = action 
                else:
                    column = q_agent.choose_action(connect4.board, epsilon=False)
            else:
                column = q_agent.choose_action(connect4.board, epsilon=False)

            print(f"QAgent put a chip in column {column + 1}.")

        connect4.move(column)

        if connect4.result is not None:
            print("\nGAME OVER\n")

            winner = "Human" if connect4.result == human else "QAgent"
            print(f"Winner is {winner}")

            break
            
    if input("Play again?\n").lower() == "y":
        play(q_agent)
