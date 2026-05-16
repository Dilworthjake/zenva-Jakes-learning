# grab the turtle module
from turtle import *

diameter = 40  # set the initial diameter of the balloon
pop_size = 200  # set the diameter at which the balloon will pop


# create a function to draw the balloon
def draw_balloon():
    color("red")  # set the color of the balloon to red
    dot(diameter)  # draw a dot with the current diameter to represent the balloon


# create a function to inflate the balloon
def inflate_balloon():
    global diameter  # use the global keyword to modify the diameter variable defined outside the function
    diameter += 10  # increase the diameter by 10 units
    clear()  # clear the previous drawing of the balloon
    draw_balloon()  # redraw the balloon with the new diameter

    if (
        diameter >= pop_size
    ):  # check if the diameter has reached or exceeded the pop size
        clear()  # clear the balloon drawing
        diameter = 40  # reset the diameter to the initial size
        write(
            "POP!", align="center", font=("Arial", 24, "bold")
        )  # write "POP!" in the center of the screen to show that the balloon has popped


# create a function to deflate the balloon
def deflate_balloon():
    global diameter  # use the global keyword to modify the diameter variable defined outside the function
    diameter -= 10  # decrease the diameter by 10 units
    clear()  # clear the previous drawing of the balloon
    draw_balloon()  # redraw the balloon with the new diameter

    if (
        diameter <= 0
    ):  # check if the diameter has reached or gone below 0, which means the balloon is empty
        clear()  # clear the balloon drawing
        diameter = 40  # reset the diameter to the initial size
        write(
            "Empty!", align="center", font=("Arial", 24, "bold")
        )  # write "Empty!" in the center of the screen to show that the balloon is empty


draw_balloon()  # call the function to draw the initial balloon
onkey(
    inflate_balloon, "Up"
)  # set up the event listener to call the inflate_balloon function when the Up key is pressed
onkey(
    deflate_balloon, "Down"
)  # set up the event listener to call the deflate_balloon function when the Down key is pressed
listen()  # start listening for events (key presses)

done()  # call the done function to start the turtle graphics loop and keep the window open until it is closed by the user
