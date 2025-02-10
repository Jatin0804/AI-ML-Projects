def display_board(board):
    """
    Parameters:
    - board (list): A 2D list representing the Tic-Tac-Toe board.

    Each cell of the board is displayed, separated by '|' for columns,
    and rows are separated by a line of dashes ('-----').
    """

    for i, row in enumerate(board):
        # Display the cells of the current row, separated by '|'
        print('|'.join(row))

        # Display a line of dashes to separate rows, but not after the last row
        if i < len(board) - 1:
            print('-' * 5)

# Create a 3x3 grid to represent the Tic-Tac-Toe board
board = [[' ' for _ in range(3)] for _ in range(3)]

display_board(board)

def check_win(board, player):
    """
    Check if the specified player has won the Tic-Tac-Toe game.

    Parameters:
    - board (list): A 2D list representing the Tic-Tac-Toe board.
    - player (str): The player to check for a win ('X' or 'O').

    Returns:
    - bool: True if the specified player has won, False otherwise.
    """
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

def is_draw(board):
    """
    Check if the Tic-Tac-Toe game is a draw (no more empty spaces on the board).

    Parameters:
    - board (list): A 2D list representing the Tic-Tac-Toe board.

    Returns:
    - bool: True if the game is a draw, False otherwise.
    """
    return all(cell != ' ' for row in board for cell in row)

import time
def player_move(board):
    """
    Get the player's move (row and column) from the user input.

    Parameters:
    - board (list): A 2D list representing the Tic-Tac-Toe board.

    Returns:
    - tuple: The selected row and column coordinates.
    """
    while True:
        try:
            time.sleep(1)
            # Get input for row and column from the player
            row = int(input("Enter row (0, 1, 2): "))
            col = int(input("Enter column (0, 1, 2): "))

            # Check if the input is within the valid range and the selected cell is empty
            if 0 <= row <= 2 and 0 <= col <= 2 and board[row][col] == ' ':
                return row, col
            else:
                print("Invalid move. Try again.")
        except ValueError:
            # Handle the case where the input is not a valid integer
            print("Invalid input. Enter numbers between 0 and 2.")

def minimax(board, depth, is_maximizing, max_depth):
    """
    Implement the Minimax algorithm for Tic-Tac-Toe.

    This function recursively explores the game tree using the Minimax algorithm to determine the optimal move for the current player. It assigns scores to game states based on the outcome of the game or the specified depth.
    """

    # Base case: Check if the game is won by 'X' or 'O' or if it's a draw
    if check_win(board, 'X'):
        return -1                 # 'X' wins, return a negative value
    elif check_win(board, 'O'):
        return 1                  # 'O' wins, return a positive value
    elif is_draw(board) or depth == max_depth:
        return 0                  # It's a draw or reached the specified depth, return 0

    if is_maximizing:
        # If maximizing, initialize the maximum evaluation score to negative infinity
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    # Simulate the move for the maximizing player ('O')
                    board[i][j] = 'O'
                    # Recursively call minimax for the next level with the minimizing player's turn
                    eval = minimax(board, depth + 1, False, max_depth)
                    # Undo the move
                    board[i][j] = ' '
                    # Update the maximum evaluation score
                    max_eval = max(max_eval, eval)
        return max_eval
    else:
        # If minimizing, initialize the minimum evaluation score to positive infinity
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    # Simulate the move for the minimizing player ('X')
                    board[i][j] = 'X'
                    # Recursively call minimax for the next level with the maximizing player's turn
                    eval = minimax(board, depth + 1, True, max_depth)
                    # Undo the move
                    board[i][j] = ' '
                    # Update the minimum evaluation score
                    min_eval = min(min_eval, eval)
        return min_eval

def ai_move(board, max_depth):
    """
    Determine the optimal move for the AI player using Minimax algorithm.

    This function iterates through each empty space on the board, simulates placing an 'O' in that space, and evaluates the move using the Minimax algorithm.
    The AI player chooses the move with the highest evaluation score.
    """
    best_eval = -float('inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                eval = minimax(board, 0, False, max_depth)
                board[i][j] = ' '
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)

    return best_move

def main():
    """

    The game loop alternates between player and AI turns, displaying the current state of the board after each move.
    The loop continues until there is a winner ('X' or 'O'), a draw, or the player chooses to exit the game.
    """

    # Reset the game board
    board = [[' ' for _ in range(3)] for _ in range(3)]

    player_turn = True

    while True:
        display_board(board)

        if player_turn:
            print("\n")
            print("Your turn:")
            row, col = player_move(board)
            print("\n")
            board[row][col] = 'X'
        else:
            print("\n")
            input("Press Enter for the Ai player to go...")
            """
            Change the depth explored by the AI player by changing the number in
            parentheses in the next line of code. The default value is 0.
            """
            row, col = ai_move(board, 10)
            print("\n")
            board[row][col] = 'O'

        if check_win(board, 'X'):
            display_board(board)
            print("You win!")
            break
        elif check_win(board, 'O'):
            display_board(board)
            print("AI wins!")
            break
        elif is_draw(board):
            display_board(board)
            print("It's a draw!")
            break

        player_turn = not player_turn

if __name__ == "__main__":
    main()
