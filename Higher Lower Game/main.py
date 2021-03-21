from art import logo, vs
from game_data import data
import random


def random_number(deck):
    random.shuffle(deck)
    index = random.randint(0, len(deck)-1)
    n = deck[index]
    deck.pop(index)
    return n


def get_random_account(deck):
    index = random_number(deck)
    user_dict = data[index]
    return user_dict


def format_data(account):
    """Format account into printable format: name, description and country"""
    name = account["name"]
    description = account["description"]
    country = account["country"]
    # print(f'{name}: {account["follower_count"]}')
    return f"{name}, a {description}, from {country}"


def check_answer(guess, a_followers, b_followers):
    """Checks followers against user's guess
  and returns True if they got it right.
  Or False if they got it wrong."""
    if a_followers > b_followers:
        return guess == "a"
    else:
        return guess == "b"


def play():
    print(logo)

    deck = list(range(0, len(data)))
    score = 0
    account_a = get_random_account(deck)
    game_over = False

    while not game_over:

        account_b = get_random_account(deck)

        print(f"Compare A: {format_data(account_a)}")
        print(vs)
        print(f"Against B: {format_data(account_b)}")

        guess = input("Who has more followers? Type 'A' or 'B': ").lower()
        a_follower_count = account_a['follower_count']
        b_follower_count = account_b['follower_count']
        is_correct = check_answer(guess, a_follower_count, b_follower_count)

        if is_correct:
            score += 1
            print(f"You're right! Current score: {score}. {len(deck)}")
            account_a = account_b
        else:
            print(f"Sorry, that's wrong. Final score: {score}\n")
            game_over = True
            if input("Play again (y/n): ") == 'y':
                play()
            else:
                return


play()
