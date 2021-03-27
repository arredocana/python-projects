import turtle as t
import random

tim = t.Turtle()
tim.speed('fastest')

def move_forward():
    tim.forward(10)

def move_backward():
    tim.backward(10)

def counter_clockwise():
    new_heading = tim.heading() + 10
    tim.setheading(new_heading)

screen = t.Screen()
screen.listen()
screen.onkeypress(key='w', fun=move_forward)
screen.onkeypress(key='s', fun=move_backward)
screen.onkeypress(key='a', fun=counter_clockwise)
screen.onkeypress(key='r', fun=tim.reset)
screen.onkeypress(key='c', fun=tim.clear)
screen.exitonclick()