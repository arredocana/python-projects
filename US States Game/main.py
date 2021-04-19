import pandas as pd
import turtle

screen = turtle.Screen()
screen.title("US States Game")
image = "data/blank_states_img.gif"
screen.addshape(image)
turtle.shape(image)

data = pd.read_csv("data/50_states.csv")
all_states = data["state"].to_list()
guessed_states = []

while len(guessed_states) < 50:

    answer_state = screen.textinput(title=f"{len(guessed_states)}/50 Guess the State",
                                    prompt="What's another state's name?").title()

    if answer_state == "Exit":
        missing_states = [state for state in all_states if state not in guessed_states]
        pd.DataFrame(missing_states).to_csv("data/states_to_learn.csv")
        break

    if answer_state in all_states:
        guessed_states.append(answer_state)
        t = turtle.Turtle()
        t.hideturtle()
        t.penup()
        state_data = data[data["state"] == answer_state]
        t.goto(int(state_data.x), int(state_data.y))
        t.write(answer_state)