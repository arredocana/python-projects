import turtle as t
import random

tim = t.Turtle()
#tim.pensize(5)
tim.speed(0)
t.colormode(255)


def random_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return r, g, b


color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
directions = [0, 90, 180, 270]


def draw_shape(num_sides):
    angle = 360 / num_sides
    for _ in range(num_sides):
        tim.forward(100)
        tim.left(angle)

# for shape_side_n in range(3, 11):
#   color = "#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])
#   tim.color(color)
#   draw_shape(shape_side_n)

# for _ in range(200):
#  tim.color(random_color())
#  tim.forward(30)
#  tim.setheading(random.choice(directions))

def draw_spirograph(size_of_gap):
    for _ in range(int(360 / size_of_gap)):
        tim.color(random_color())
        tim.circle(100)
        tim.setheading(tim.heading() + size_of_gap)

#draw_spirograph(5)

def move_forwards():
    tim.forward(10)


screen = t.Screen()
screen.listen()
screen.onkey(key='w', fun=move_forwards)
screen.exitonclick()
