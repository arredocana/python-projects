from menu import Menu
from coffee_maker import CoffeeMaker
from money_machine import MoneyMachine

my_menu = Menu()
coffee_maker = CoffeeMaker()
money_machine = MoneyMachine()

status = True

while status:
    options = my_menu.get_items()
    choice = input(f"What would you like? ({options}) ?: ")
    if choice == "off":
        status = False
    elif choice == "report":
        coffee_maker.report()
        money_machine.report()
    else:
        drink = my_menu.find_drink(choice)
        if drink is not None:
            if coffee_maker.is_resource_sufficient(drink) and money_machine.make_payment(drink.cost):
                coffee_maker.make_coffee(drink)
