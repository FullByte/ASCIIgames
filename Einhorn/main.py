from itertools import product # pip install itertools
from collections import OrderedDict
import math
import json
import random
import os
import sqlite3
import datetime

# Dice settings
diceFaces = 6
diceSmallestNumber = 1
diceHighestNumber = 6
diceAmount = 3

# Files
fileResults = "results.json"
fileRules = "rules.txt"
db_name = "einhorn_game_log.db"

# Game
scores = None

def show_dice():

    print("""  _______.
    ______    | .   . |\
   /     /\   |   .   |.\
  /  '  /  \  | .   . |.'|
 /_____/. . \ |_______|.'|
 \ . . \    /  \ ' .   \'|
  \ . . \  /    \____'__\|
   \_____\/
     NEW GAME """)

def createStatFiles():
    # Counter
    Dreifaltigkeit = 0
    Wunsch = 0
    Unvermeidlich = 0
    Einhorn = 0

    # Create a list of all possible roll attempts
    rolls = list(product(range(diceSmallestNumber,diceHighestNumber+1), repeat=diceAmount))

    results = []

    for roll in rolls:
        # Prepare list
        removedDoubleRoll = tuple(OrderedDict.fromkeys(roll).keys())
        sortedRoll = list(removedDoubleRoll)
        sortedRoll.sort() 

        # Create a dictionary to store the result of each roll
        result = {"roll": roll}

        # Determine the outcome and add it to the result dictionary
        if len(sortedRoll) == 2:
            result["outcome"] = "Wunsch"
            Wunsch += 1
        elif len(sortedRoll) == 1:
            result["outcome"] = "Dreifaltigkeit"
            Dreifaltigkeit += 1
        else:
            if (sortedRoll[1]-sortedRoll[0]==1) or (sortedRoll[2]-sortedRoll[1]==1):
                result["outcome"] = "Das Unvermeidliche"
                Unvermeidlich += 1
            else:
                result["outcome"] = "Einhorn"
                Einhorn += 1

        # Add the result to the results list
        results.append(result)

    # Write the results to a JSON file
    with open(fileResults, 'w') as f:
        json.dump(results, f)

    PrintStats(rolls, Dreifaltigkeit, Wunsch, Unvermeidlich, Einhorn)

def PrintStats(rolls, Dreifaltigkeit, Wunsch, Unvermeidlich, Einhorn):
    with open(fileRules, 'w') as f:
        f.write("Total amount of possible rolls: {}\n".format(len(rolls)))
        f.write("Total amount of distinct rolls: {}\n".format(int((math.factorial(diceFaces+diceAmount-1))/(math.factorial(diceAmount)*(math.factorial(diceFaces-1))))))
        f.write("\nDreifaltigkeit: {} ({:.1f}%)\n".format(Dreifaltigkeit, Dreifaltigkeit / len(rolls) * 100))
        f.write("Wunsch: {} ({:.1f}%)\n".format(Wunsch, Wunsch / len(rolls) * 100))
        f.write("Das Unvermeidliche: {} ({:.1f}%)\n".format(Unvermeidlich, Unvermeidlich / len(rolls) * 100))
        f.write("Einhorn: {} ({:.1f}%)\n".format(Einhorn, Einhorn / len(rolls) * 100))

def roll_dice():
    dice = [random.randint(1, diceFaces) for _ in range(3)]
    dice.sort()
    return tuple(dice)

def check_outcome(dice_roll):
    # Load the results from the JSON file
    with open(fileResults, 'r') as f:
        results = json.load(f)

    # Search for the dice roll in the results
    for result in results:
        if tuple(result['roll']) == dice_roll:
            return result['outcome']

    # If the dice roll was not found in the results
    return None

def play():
    # Clear the screen after every move
    os.system('cls' if os.name == 'nt' else 'clear')
    show_dice()

    # Get players and points
    scores = initialize_game()

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
            prediction TEXT,
            result TEXT,
            reward INTEGER,
            dice1 INTEGER,
            dice2 INTEGER,
            dice3 INTEGER
      )
    ''')

    # Game loop
    while True:
        for player, score in scores.items():
            # Ask for the prediction
            print(f"{player}, predict the outcome:")
            print("[1] Wunsch")
            print("[2] Das Unvermeidliche")
            print("[3] Einhorn")
            print("[4] Dreifaltigkeit")
            prediction = input("Enter your prediction (1-4): ")

            # Map the prediction number to the corresponding outcome
            prediction_map = {
                '1': 'Wunsch',
                '2': 'Das Unvermeidliche',
                '3': 'Einhorn',
                '4': 'Dreifaltigkeit'
            }
            prediction = prediction_map.get(prediction, None)

            dice_roll = roll_dice()
            outcome = check_outcome(dice_roll)

            print(f"The dice roll was {dice_roll} and the outcome was {outcome}. Your prediction was {prediction}.")
            points = determine_points(outcome, prediction)
            print(f"Points earned or lost: {points}")

            # Update the player's score
            scores[player]['current_game'] += points

            # Update the unicorn status
            if outcome == 'Einhorn':
                # Reset unicorn status for all players
                for p in scores:
                    scores[p]['has_unicorn'] = 0
                # Set unicorn status for the current player
                scores[player]['has_unicorn'] = 1

            # Insert a new row into the database
            c.execute('''
                INSERT INTO logs (game_id, timestamp, player, prediction, result, reward, dice1, dice2, dice3)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (1, datetime.datetime.now(), player, prediction, outcome, points, dice_roll[0], dice_roll[1], dice_roll[2]))
            conn.commit()

            # Check if the player has 0 or less points
            if scores[player]['current_game'] <= 0:
                print(f"{player} has 0 or less points. Game over.")
                return

    conn.close()


def determine_points(outcome, prediction):
    # Define the points for each outcome and prediction
    points_table = {
        'Das Unvermeidliche': {'correct': +2, 'wrong': -2, 'no_prediction': -1},
        'Wunsch': {'correct': +2, 'wrong': -2, 'no_prediction': -1},
        'Einhorn': {'correct': +5, 'wrong': -5, 'no_prediction': +1},
        'Dreifaltigkeit': {'correct': 'WIN', 'wrong': +1, 'no_prediction': +5}
    }

    # Check if the prediction is correct, wrong, or if there was no prediction
    if prediction == outcome:
        return points_table[outcome]['correct']
    elif prediction is None:
        return points_table[outcome]['no_prediction']
    else:
        return points_table[outcome]['wrong']

def initialize_game():
    # Ask for the number of players
    num_players = input("Enter the number of players (1-6): ")
    while not num_players.isdigit() or int(num_players) < 1 or int(num_players) > 6:
        print("Invalid input. Please enter a number between 1 and 6.")
        num_players = input("Enter the number of players (1-6): ")

    num_players = int(num_players)

    # Initialize a dictionary to keep track of the scores
    scores = {f'Player {i+1}': {'current_game': 6, 'previous_games': 0, 'roll': roll_dice(), 'has_unicorn': 0} for i in range(num_players)}

    # Determine the starting player
    starting_player = max(scores.items(), key=lambda x: x[1]['roll'])
    starting_player[1]['current_game'] = 7

    print(f"{starting_player[0]} starts the game with 7 points. All other players start with 6 points.")

    return scores

def menu():
    # Clear the screen 
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
\.
 \\      .
  \\ _,.+;)_
  .\\;~%:88%%.
 (( a   `)9,8;%.
 /`   _) ' `9%%%?
(' .-' j    '8%%'
 `"+   |    .88%)+._____..,,_   ,+%$%.
       :.   d%9`             `-%*'"'~%$.
    ___(   (%C    Einhorn      `.   68%%9
  ."        \7                  ;  C8%%)`
  : ."-.__,'.____________..,`   L.  \86' ,
  : L    : :            `  .'\.   '.  %$9%)
  ;  -.  : |             \  \  "-._ `. `~"
   `. !  : |              )  >     ". ?
     `'  : |            .' .'       : |
         ; !          .' .'         : |
        ,' ;         ' .'           ; (
       .  (         j  (            `  \\
       '""'          ""'             `"" 
""")


    # Create files
    if not os.path.exists(fileResults) or not os.path.exists(fileRules):
        createStatFiles()

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
    return None

def delete_database():
    return None

def rules():
    return None

menu()
