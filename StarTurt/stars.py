from turtle import *  # Importing the turtle graphics library
from random import *  # Importing the random library to generate random numbers

bgcolor("black")  # Setting the background color to black
hideturtle()  # Hiding the turtle cursor

speed(0)  # Setting the turtle speed to the fastest (0 is the fastest speed)

width = window_width()  # Getting the width of the turtle graphics window
height = window_height()  # Getting the height of the turtle graphics window


# Function to draw a star at a given (x, y) position
def draw_star(x_pos, y_pos):
    size = randrange(
        4, 10
    )  # Randomly determining the size of the star (between 4 and 10)
    penup()
    goto(
        x_pos, y_pos
    )  # Moving the turtle to the specified (x, y) position without drawing
    pendown()
    dot(
        size, "white"
    )  # Drawing a white dot at the current position with the specified size


# Loop to draw 100 stars at random positions on the screen
for i in range(100):
    x = randrange(
        -width // 2, width // 2
    )  # Randomly determining the x-coordinate of the star (between -width/2 and width/2)
    y = randrange(
        -height // 2, height // 2
    )  # Randomly determining the y-coordinate of the star (between -height/2 and height/2)
    draw_star(x, y)

done()  # Finishing the turtle graphics and keeping the window open until it is closed by the user
