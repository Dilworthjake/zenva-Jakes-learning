# import turtle
from turtle import *

# increase speed of turtle
speed(10)

# set background colour to black
bgcolor("black")
# colour and draw the sun
color("orange")
begin_fill()
circle(60)
end_fill()
# lift pen relocate to the first planet
penup()
forward(100)
pendown()
# colour and draw  planet one
color("grey")
begin_fill()
circle(20)
end_fill()
# lift pen relocate to the second planet
penup()
forward(80)
pendown()
# colour and draw planet two
color("red")
begin_fill()
circle(40)
end_fill()
# lift pen relocate to the third planet
penup()
forward(90)
pendown()
# colour and draw planet three
color("green")
begin_fill()
circle(30)
end_fill()
# finish
done()
