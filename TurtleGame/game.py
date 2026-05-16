from turtle import *  # Importing the turtle module to create a simple game

speed(0)  # Set the turtle speed to the fastest

move_distance = 50  # Define the distance the turtle will move with each key press

# The main function sets up the game environment, including the background color, drawing the goal area, and setting up the turtle's initial position and key bindings for movement.


def main():
    bgcolor("#E2803A")  # Set the background color of the game window

    penup()
    goto(200, 450)
    pendown()

    # Draw the goal area as a blue rectangle on the right side of the screen
    color("blue")

    begin_fill()
    goto(500, 450)
    goto(500, -450)
    goto(200, -450)
    goto(200, 450)
    end_fill()
    # Set up the turtle's initial position, color, and shape
    penup()
    goto(-200, 0)
    color("green")
    shape("turtle")
    pendown()
    # Set up key bindings for movement in four directions
    onkey(move_up, "Up")
    onkey(move_down, "Down")
    onkey(move_left, "Left")
    onkey(move_right, "Right")


# Each movement function sets the turtle's heading in the appropriate direction, moves it forward by the defined distance, and then checks if the turtle has reached the goal area.
def move_up():
    setheading(90)
    penup()
    forward(move_distance)
    pendown()
    check_goal()


def move_down():
    setheading(270)
    penup()
    forward(move_distance)
    pendown()
    check_goal()


def move_left():
    setheading(180)
    penup()
    forward(move_distance)
    pendown()
    check_goal()


def move_right():
    setheading(0)
    penup()
    forward(move_distance)
    pendown()
    check_goal()


# The check_goal function checks if the turtle's current position is within the defined goal area. If it is, it hides the turtle, displays a "You Win!" message, and disables further movement by unbinding the key events.
def check_goal():
    if xcor() > 200 and xcor() < 500 and ycor() < 450 and ycor() > -450:
        hideturtle()
        color("white")
        write("You Win!")
        penup()
        goto(-200, 0)
        pendown()
        onkey(None, "Up")
        onkey(None, "Down")
        onkey(None, "Left")
        onkey(None, "Right")


# The reset_game function clears the screen and restarts the game by calling the main function again. It also shows the turtle again in case it was hidden after winning.
def reset_game():
    clear()
    main()
    showturtle()


# Start the game by calling the main function, setting up the key binding for resetting the game with the spacebar, and starting the event loop to listen for key presses.
main()
onkey(reset_game, "space")
listen()

# Start the turtle graphics event loop to keep the window open and responsive to user input.
done()
