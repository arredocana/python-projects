import random
from art import logo

EASY_LEVELS_TURNS = 10
HARD_LEVELS_TURNS = 5


# Function to set difficulty
def set_difficulty():
    level = input("Choose a difficulty. Type 'easy' or 'hard': ")
    if level == 'easy':
        return EASY_LEVELS_TURNS
    else:
        return HARD_LEVELS_TURNS


def check_answer(guess, answer, turns):
    if guess == answer:
        print(f"You got it! The answer was {answer}.")
    elif guess < answer:
        print("Too low.")
        return turns - 1
    else:
        print("Too high.")
        return turns - 1


def play():
    print(logo)
    game_over = False

    # Choose a random number
    print("Welcome to the Number Guessing Game!")
    print("I'm thinking of a number between 1 and 100.")
    answer = random.randint(1, 100)
    print(f"Pss, the correct number is {answer}.")

    turns = set_difficulty()
    guess = 0

    while guess != answer:
        print(f"You have {turns} remaining to guess the number.")

        # Let the user guess a number
        guess = int(input("Make a guess: "))

        # Track the number of turns and reduce by 1 if they get it wrong
        turns = check_answer(guess, answer, turns)

        if turns == 0:
            print("You've run out of guesses, you lose.")
            return
        elif guess != answer:
            print("Guess again.")


while input("Play again? (y/n): ") == 'y':
    play()


