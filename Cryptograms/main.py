# Cryptograms: Puzzle where a short piece of encrypted text is given, and the player must decrypt it.
def cryptogram():
    cryptograms = {
        "L qlfk zklwh dqg uhdg doo ryhu, dqg eodfn dqg uhdg zlwklq": "I am black white and read all over, and black and read within",
        "Wkh ehvw wklqjv lq olih duh iuhh": "The best things in life are free",
        "Wkh ehjlnqlqj ri doo nqrzohgjh lv wkh oryh ri zlvgrp": "The beginning of all knowledge is the love of wisdom"
    }

    for cryptogram, answer in cryptograms.items():
        print("Here is the cryptogram: ", cryptogram)
        user_answer = input("What is your answer? ")

        if user_answer.lower() == answer:
            print("Correct!")
        else:
            print("Incorrect. The correct answer is: ", answer)

cryptogram()
