import random
import os
import time
import platform

def clear_console():
    if platform.system() == 'Windows':  # For Windows
        os.system('cls')
    else:  # For Linux/OS X
        os.system('clear')

def hangman():
    word_list = ["python", "java", "hangman", "computer", "programmer", "software", "debugging"]
    random_number = random.randint(0, len(word_list) - 1)
    chosen_word = word_list[random_number]
    guess_word = []
    for letter in chosen_word:
        guess_word.append("_")

    attempts = 6

    stages = ['''
      +---+
      |   |
          |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
          |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
      |   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|   |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\\  |
          |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\\  |
     /    |
          |
    =========''', '''
      +---+
      |   |
      O   |
     /|\\  |
     / \\  |
          |
    =========''']

    while attempts > 0:
        clear_console()
        print(stages[6 - attempts])
        print("The word is: ", guess_word)
        print("Guess the characters")
        print("You have ", attempts, " attempts left")

        guess = input()

        if guess not in chosen_word:
            attempts -= 1

        else:
            for index in range(len(chosen_word)):
                if chosen_word[index] == guess:
                    guess_word[index] = guess

        if '_' not in guess_word:
            print("You won!")
            break

        time.sleep(1)

    if attempts == 0:
        clear_console()
        print(stages[6 - attempts])
        print("You lost! The word was: ", chosen_word)

hangman()