import sqlite3
import time
import os

db_name = "tictactoe_game_log.db"

def print_ultimate_board(ultimate_board, active_board=None):
    print("      1      2      3    ")
    print("  -----------------------")
    for big_row in range(3):
        for small_row in range(3):
            row_to_print = f"{big_row + 1} |" if small_row == 1 else "  |"
            for big_col in range(3):
                formatted_row = []
                for small_col in range(3):
                    cell = ultimate_board[big_row][big_col][small_row][small_col]
                    if cell == '#':
                        if active_board is not None and active_board == (big_row, big_col):
                            formatted_row.append(f"\033[92m{cell}\033[0m")  # Green for active field
                        else:
                            formatted_row.append(f"\033[90m{cell}\033[0m")  # Grey for inactive field
                    elif cell == 'X':
                        formatted_row.append(f"\033[91m{cell}\033[0m")  # Red for 'X'
                    else:
                        formatted_row.append(f"\033[94m{cell}\033[0m")  # Blue for 'O'
                row_to_print += ' '.join(formatted_row) + ' | '
            print(row_to_print)
        if big_row != 2:
            print("  -----------------------")
    print("  -----------------------")

   
def check_win(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != '#':
            return f"{row[0]}" if row[0] == 'X' else f"{row[0]}"
    
    # Check columns
    for col in range(len(board)):
        if board[0][col] == board[1][col] == board[2][col] != '#':
            return f"{board[0][col]}" if board[0][col] == 'X' else f"{board[0][col]}"
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '#':
        return f"{board[0][0]}" if board[0][0] == 'X' else f"{board[0][0]}"
    if board[0][2] == board[1][1] == board[2][0] != '#':
        return f"{board[0][2]}" if board[0][2] == 'X' else f"{board[0][2]}"
    return None

def check_ultimate_win_old_deleteme(ultimate_board):
    # Create a 2D list to store the winner of each small board
    winners = [[check_win(ultimate_board[i][j]) for j in range(3)] for i in range(3)]
    # Check for a win condition in the winners list
    return check_win(winners)

def check_ultimate_win(ultimate_board):
    # Create a 2D list to store the winner of each small board
    winners = [[check_win(ultimate_board[i][j]) for j in range(3)] for i in range(3)]
    # Check for a win condition in the winners list
    ultimate_winner = check_win(winners)
    if ultimate_winner:
        return ultimate_winner

    # Count the number of small boards won by each player
    x_wins = sum(row.count("X") for row in winners)
    o_wins = sum(row.count("O") for row in winners)

    # If no player has won the game and there are no more moves left, the player with the most small boards won is the winner
    if not any('#' in row for board in ultimate_board for row in board):
        if x_wins > o_wins:
            return "X"
        elif o_wins > x_wins:
            return "O"
        else:
            return "Draw"

    return None

def is_board_won(ultimate_board, next_board):
    # Check if the board at next_board has been won
    return check_win(ultimate_board[next_board[0]][next_board[1]]) is not None

def play():
    # Clear the screen after every move
    os.system('cls' if os.name == 'nt' else 'clear')

    # Connect to the SQLite database (it will be created if it doesn't exist)
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Create a table for logs if it doesn't exist
    c.execute('''
         CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY,
            game_id INTEGER,
            timestamp TEXT,
            player TEXT,
            player_x_name TEXT, 
            player_o_name TEXT,
            big_row INTEGER,
            big_col INTEGER,
            small_row INTEGER,
            small_col INTEGER
      )
    ''')

    # Start a new game
    game_id = c.execute('SELECT MAX(game_id) FROM logs').fetchone()[0]
    if game_id is None:
      game_id = 1
    else:
      game_id += 1

    ultimate_board = [[[['#' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]
    player = 'X'
    next_board = None

    while True:
        print_ultimate_board(ultimate_board, next_board)
        
        if player == 'X':
            print("\033[91mPlayer", player, "'s turn\033[0m")  # Red for 'X'
        else:
            print("\033[94mPlayer", player, "'s turn\033[0m")  # Blue for 'O'
        
        try:
            if next_board is None:
                big_col_input = input("Enter big column: ")
                big_col = int(big_col_input) - 1

                big_row_input = input("Enter big row: ")                
                big_row = int(big_row_input) - 1
            elif is_board_won(ultimate_board, next_board):
                print("The referenced board has already been won.\nYou may choose any free board to play next.")
                while True:
                    big_col_input = input("Enter big column: ")
                    big_col = int(big_col_input) - 1

                    big_row_input = input("Enter big row: ")                
                    big_row = int(big_row_input) - 1

                    # Check if the entered board has been won
                    if not is_board_won(ultimate_board, (big_row, big_col)):
                        break
                    else:
                        print("This board has already been won. Please choose another board.")
            else:
                big_row, big_col = next_board

            col_input = input("Enter small column: ")
            col = int(col_input) - 1

            row_input = input("Enter small row: ")            
            row = int(row_input) - 1            

            # Check if the chosen field is already occupied
            if ultimate_board[big_row][big_col][row][col] != '#':                
                os.system('cls' if os.name == 'nt' else 'clear')
                print("Field in row " + str(row+1) + " and column " + str(col+1) + " is already occupied. Choose another field.")
                continue
            ultimate_board[big_row][big_col][row][col] = player

            # Log the move
            from datetime import datetime
            timestamp = datetime.now().isoformat()
            c.execute('''
                INSERT INTO logs (game_id, timestamp, player, player_x_name, player_o_name, big_row, big_col, small_row, small_col)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (game_id, timestamp, player, "", "", big_row, big_col, row, col))
            conn.commit()            

            # Check for wins
            winner = check_win(ultimate_board[big_row][big_col])
            if winner:
                ultimate_board[big_row][big_col] = [[winner for _ in range(3)] for _ in range(3)]
                print("Player", player, "wins the small field!")

            ultimate_winner = check_ultimate_win(ultimate_board)
            if ultimate_winner == "None":
                # Switch the player after checking for a win
                player = 'O' if player == 'X' else 'X'
                next_board = (row, col)
            else:
                # Determine the winner
                if ultimate_winner == "X":
                    print("Player X wins the game!")
                else:
                    print("Player O wins the game!")
                break

            # Clear the screen after every move
            os.system('cls' if os.name == 'nt' else 'clear')

        except (ValueError, IndexError):
            print("Invalid move, try again.")


    conn.close()

    # Show last board
    print("Final Board:")
    print_ultimate_board(ultimate_board)

    # Save or delete game recording
    end_game(game_id)    

def menu():
    # Clear the screen 
    os.system('cls' if os.name == 'nt' else 'clear')

    print("""
       ██    ██ ██   ████████ ██ ███    ███  █████  ████████ ███████      
       ██    ██ ██      ██    ██ ████  ████ ██   ██    ██    ██           
       ██    ██ ██      ██    ██ ██ ████ ██ ███████    ██    █████        
       ██    ██ ██      ██    ██ ██  ██  ██ ██   ██    ██    ██           
        ██████  ███████ ██    ██ ██      ██ ██   ██    ██    ███████      
                                                                         
                                                                                
████████ ██  ██████     ████████  █████   ██████     ████████  ██████  ███████ 
   ██    ██ ██             ██    ██   ██ ██             ██    ██    ██ ██      
   ██    ██ ██             ██    ███████ ██             ██    ██    ██ █████   
   ██    ██ ██             ██    ██   ██ ██             ██    ██    ██ ██      
   ██    ██  ██████        ██    ██   ██  ██████        ██     ██████  ███████ 
                                                                               
    """)

    while True:
        print("="*30 + "\n" + " "*10 + "MENU" + "\n" + "="*30)
        print("[1] Play")
        print("[2] View Replay")
        print("[3] Delete Replays")
        print("[4] Rules")
        print("[5] Exit")
        print("="*30)
        choice = input("Enter your choice: ")

        if choice == '1':
            play()
        elif choice == '2':
            replay_menu()
        elif choice == '3':
            delete_database()
        elif choice == '4':
            rules()
        elif choice == '5':
            print("Exiting the game.")
            break
        else:
            print("Invalid choice. Please choose again.")

def replay_menu():
    # Clear the screen 
    os.system('cls' if os.name == 'nt' else 'clear')

    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    offset = 0
    while True:
        # Fetch the 10 newest game logs
        c.execute('''
            SELECT game_id, player_x_name, player_o_name, MAX(timestamp)
            FROM logs
            GROUP BY game_id
            ORDER BY MAX(timestamp) DESC
            LIMIT 10 OFFSET ?
        ''', (offset,))
        game_logs = c.fetchall()

        # Print the game logs in a tabular format
        print("{:<10} {:<20} {:<20} {:<20}".format('Game ID', 'Player X', 'Player O', 'Timestamp'))
        for game_log in game_logs:
            game_id, player_x_name, player_o_name, timestamp = game_log
            print("{:<10} {:<20} {:<20} {:<20}".format(game_id, player_x_name, player_o_name, timestamp))

        more = input("Choose (m)ore,, (b)ack or enter the game id to replay: ")
        if more.lower() == 'm':
            offset += 10
        elif more.lower() == 'b':
            if offset <= 10:
                offset = 0
            else:
                offset -= 10
        else:
            try:
                game_id = more
                # Check if the entered game_id is valid
                if int(game_id) in [game_log[0] for game_log in game_logs]:
                    replay(game_id)
                    break
                else:
                    print("Invalid game id. Please choose again.")
            except ValueError:
                print("Invalid input. Please enter a valid game id.")

    conn.close()

def replay(game_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Fetch the game logs for the specified game_id
    c.execute('SELECT * FROM logs WHERE game_id = ? ORDER BY timestamp', (game_id,))
    logs = c.fetchall()

    # Initialize an empty board
    ultimate_board = [[[['#' for _ in range(3)] for _ in range(3)] for _ in range(3)] for _ in range(3)]

    # Replay the game
    for log in logs:
        _, _, _, player, _, _, big_row, big_col, small_row, small_col = log
        ultimate_board[big_row][big_col][small_row][small_col] = player

        # Print the board, wait 3 seconds and clear the screen
        print_ultimate_board(ultimate_board)
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')

    conn.close()

    # Rerun the Replay?
    print("1. Replay the game")
    print("2. Return to main menu (default)")
    choice = input("Enter your choice: ")

    if choice == '1':
        replay(game_id)

def rules():    
    print("Ultimate Tic Tac Toe")
    print("\nRules:")
    print("1. The game is played on a grid that's 3x3 Tic Tac Toe boards.")
    print("2. The first player may start in any cell in any mini board.")
    print("3. The board in which the next player must play is determined by the cell the previous player chose.")
    print("4. If sent to a board that's already won, the player may choose any other free board.")
    print("5. The game is won if a player manages to win 3 boards that add to a row on the big board.")
    print("6. Else, if no further moves are possible the player with the most won mini boards wins the game.")
    print("\nColors:")
    print("1. 'X' is represented in Red.")
    print("2. 'O' is represented in Blue.")
    print("3. Fields that can be played are in green.")
    print("\nFeatures:")
    print("1. All moves are recorded and games can be saved and reviewed anytime.")

def delete_database():
    if os.path.exists(db_name):
        os.remove(db_name)
        print("Database deleted successfully.")
    else:
        print("The file does not exist.")

def end_game(game_id):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    c = conn.cursor()

    # Ask to save or delete game
    save_game = input("Do you want to save the game? (y)es [default] or (n)o: ")
    if save_game.lower() == 'n':
        # Delete the game logs from the database
        c.execute('DELETE FROM logs WHERE game_id = ?', (game_id,))
    else:
        # Get player names
        player_x_name = input("Enter a name for player 1 (playing X): ")
        player_o_name = input("Enter a name for player 2 (playing O): ")

        # Update the game name in the database
        c.execute('UPDATE logs SET player_x_name = ? WHERE game_id = ?', (player_x_name, game_id))
        c.execute('UPDATE logs SET player_o_name = ? WHERE game_id = ?', (player_o_name, game_id))
        
    conn.commit()
    conn.close()

# Call the menu function
menu()
