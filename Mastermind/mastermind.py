import random
import itertools

random.seed(0)

def score_guess(guess, secret_code, verbose=False):
    red = 0
    white = 0
    for i in range(len(guess)):
        if guess[i] == secret_code[i]:
            red += 1
        else:
            if guess[i] in secret_code:
                white += 1
    return (red, white)

def play_mastermind(n=5, c=7):
    print("#" * 22)
    print("Mastermind!")
    print("#" * 22)
    print("\nYou are playing a game with {} colors and {} digits.".format(c, n))
    print()

    secret_code = []
    for i in range(n):
        secret_code.append(random.randint(0, c - 1))
    print("The secret code is:", secret_code)
    print()

    possible_secret_codes = list(itertools.product(range(c), repeat=n))
    guesses = 0
    guess = tuple([0 if (i < (n / 2)) else 1 for i in range(n)])

    while True:
        guesses += 1
        print("Try this guess: ", guess)
        input("Press enter to continue...")
        correct, close = score_guess(guess, secret_code)
        print("# of Red pegs:", correct)
        print("# of White pegs:", close)
        print()

        if correct == n:
            print("You win!")
            break
        
        possible_secret_codes = [x for x in possible_secret_codes if score_guess(guess, x) == (correct, close)]
        guess = random.choice(possible_secret_codes)

    print("It took", guesses, "guesses to win.\n")
    return guesses

if __name__ == "__main__":
    play_mastermind(n=5, c=7)
