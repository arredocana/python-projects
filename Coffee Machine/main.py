MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}

resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}

COINS = {
    "quarters": 0.25,
    "dimes": 0.1,
    "nickles": 0.05,
    "pennies": 0.01
}


def print_report():
    """Print resources of the coffee machine"""
    for k, v in resources.items():
        print(f"{k.capitalize()}: {v}ml")
    print(f"Money: ${profit}")


def check_resources(order_ingredients):
    """Returns True when order can be made, False if ingredients are insufficient"""
    for ingredient in order_ingredients:
        if ingredient in resources:
            if (resources[ingredient] - order_ingredients[ingredient]) < 0:
                print(f"Sorry there is not enough {ingredient}.")
                return False
    return True


def process_coins():
    """Returns the total calculated from coins inserted."""
    total = 0
    print("Insert coins.")
    for coin in COINS:
        total += int(input(f"How many {coin}?: ")) * COINS[coin]
    return round(total, 2)


def check_payment(money_received, drink_name):
    """Return True when the payment is accepted or False is money is insufficient."""
    drink_cost = MENU[drink_name]["cost"]
    print(f"A {drink_name} costs ${drink_cost}. Here there are ${money_received}.")

    if money_received >= drink_cost:
        if money_received > drink_cost:
            change = round(money_received - drink_cost, 2)
            print(f"Here is ${change} dollars in change.")
        global profit
        profit += drink_cost
        return True
    else:
        print("Sorry that's not enough money. Money refunded.")
        return False


def make_coffee(drink_name, order_ingredients):
    """Deduct the required ingredients from the resources"""
    for ingredient, value in order_ingredients.items():
        if ingredient in resources:
            resources[ingredient] -= value
    print(f"Here is your {drink_name}.Enjoy!☕")


status = True
profit = 0
drinks = ["espresso", "latte", "cappuccino"]

while status:
    choice = input("What would you like? (espresso/latte/cappuccino): ")
    if choice == "off":
        status = False
    elif choice == "report":
        print_report()
    elif choice in drinks:
        drink = MENU[choice]
        if check_resources(drink["ingredients"]):
            payment = process_coins()
            if check_payment(payment, choice):
                make_coffee(choice, drink["ingredients"])
    else:
        print("Please select a coffee of this machine")
