# Day 86 Python Breakout Game
# 100 Days of Python Code
# Author: John J Cupak Jr, jcupak@gmail.com
# History: 2021-06-17 Completed

# NOTE: 0,0 is center of screen

import turtle
import time
import os
from scoreboard import Scoreboard

# Breakout brick color rows and points from top to bottom
COLORS = ["red", "red", "orange", "orange", "green", "green", "yellow", "yellow"]
POINTS = [ 7,       7,        5,        5,       3,       3,        1,        1 ]
ROWS   = [ 180,   150,      120,       90,      60,      30,        0,      -30]
DEBUG  = os.getenv('DEBUG')  # Get debug flag

# Create the game screen DONE
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Python Breakout Game")
screen.bgcolor("black")
screen.tracer(0)  # Turn off animation

screen.listen()

# Create the bricks DONE
# NOTE: Each brick is an individual turtle object
brick_start_x = -335  # Left side of screen
brick_start_y =  180  # Top row
brick_number  =    0

# How many bricks?
brick_rows    = 8
brick_columns = 7
brick_number  = 0
bricks = []                                             # Empty list of bricks
brick_value = []                                        # Empty array of brick values

for row in range(brick_rows):                           # Vertical top-to-bottom direction
    if DEBUG:
        print(f"Creating bricks on row={row} at y={brick_start_y + (row * -30):3}")
    for column in range(brick_columns):                 # Horizontal left-to-right direction
        brick = turtle.Turtle()                         # Create brick
        brick.speed(1)
        brick.shape("square")
        brick.shapesize(stretch_wid=1, stretch_len=5)   # Change brick shape to rectangle
        brick.color(COLORS[row])                        # Set brick color for row
        brick_value.append(POINTS[row])                 # Set brick value
        brick_number += 1                               # Count brick just created
        brick.penup()                                   # Hide pen move
        brick_x = brick_start_x + (110 * column)        # Brick horizontal position
        brick_y = brick_start_y + (row * -30)           # Brick vertical position (down)
        brick.setpos(brick_x, brick_y)                  # Place and show brick
        bricks.append(brick)                            # Save individual brick

# Create the bottom paddle DONE
paddle = turtle.Turtle()
paddle.speed(0)
paddle.shape("square")
paddle_length = 5
paddle.shapesize(stretch_wid=1, stretch_len=paddle_length)
paddle.color("white")
paddle.penup()
paddle_x    = 0                  # Paddle initial horizontal position
paddle_y = -250                  # Paddle initial vertical position
paddle.goto(paddle_x, paddle_y)  # Set paddle intial position
paddle_dx = 20                   # Set paddle horizontal movement

# Create the ball DONE
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.speed(1)              # Slowest speed
ball.penup()
ball_x  =    0             # Ball initial horizontal position
ball_y  = paddle_y + 20    # Ball initial vertical position (just above paddle)
ball.goto(ball_x, ball_y)  # Ball initial position

ball_dx =    5             # Ball initial horizontal movement (to the right)
ball_dy =   -5             # Ball initial vertical movement (downwards)

ball_speed = 0.01          # Ball initial speed

scoreboard = Scoreboard()        # Setup and initialize single player scoreboard


# Paddle horizontal movement functions DONE
def move_paddle_left():
    paddle_x = paddle.xcor() - paddle_dx
    paddle.setx(paddle_x)


def move_paddle_right():
    paddle_x = paddle.xcor() + paddle_dx
    paddle.setx(paddle_x)


# Keyboard binding for paddle movements
screen.listen()
screen.onkeypress(move_paddle_left, "Left")    # Left arrow
screen.onkeypress(move_paddle_right, "Right")  # Right arrow

# Main game loop  DONE
game_is_running = True
while game_is_running:

    screen.update()

    time.sleep(ball_speed)           # Slow down game animation

    # Move the ball
    ball_x = ball.xcor() + ball_dx
    ball_y = ball.ycor() + ball_dy
    ball.setposition(ball_x, ball_y)

    #  Get paddle horizontal position DONE
    paddle_x = paddle.xcor()

    # Check paddle limits DONE
    if paddle_x > 340:           # Paddle hit right wall
        if DEBUG:
            print(f"Paddle hit right wall at {paddle_x}. Sticks")
        paddle_x = 340           # Fix paddle right limit
        paddle.setx(paddle_x)

    if paddle_x < -350:          # Paddle hit left wall
        if DEBUG:
            print(f"Paddle hit left wall at {paddle_x}. Sticks")
        paddle_x = -350          # Fix paddle left limit
        paddle.setx(paddle_x)

    # Check for ball collision with side walls DONE
    if ball_x > 380:             # Right wall margin
        if DEBUG:
            print(f"Ball hit right wall at {ball.position()}. Rebounds to left")
        ball_x = 380
        ball.setx(ball_x)        # Hit right wall (400 - 20)
        ball_dx *= -1            # Ball rebounds left

    if ball_x < -380:            # Left wall margin
        if DEBUG:
            print(f"Ball hit left wall at {ball.position()}. Rebounds to right")
        ball_x = -380
        ball.setx(ball_x)        # Hit left wall
        ball_dx *= -1            # Ball rebounds right

    if ball_y > 180:             # Top wall margin
        if DEBUG:
            print(f"Ball hit top wall at {ball.position()}. Rebounds downward")
        ball_y = 180
        ball.sety(ball_y)         # Hit top wall
        ball_dy *= -1             # Ball rebounds down

    if ball_y < -280:             # Ball missed paddle and hit bottom wall
        if DEBUG:
            print(f"Ball hit bottom wall at {ball.position()}. Rebounds upwards")
        ball_y = -280
        # time.sleep(1)
        ball_dy *= -1              # Ball rebounds up
        scoreboard.update_lives()  # Lose a life

    # Check for ball collision with paddle DONE
    ball_x   = ball.xcor()
    ball_y   = ball.ycor()
    paddle_x = paddle.xcor()
    paddle_y = paddle.ycor()
    ball_y_distance = abs(paddle_y - ball_y)  # Get vertical distance between ball and paddle
    ball_distance = ball.distance(paddle)     # Get vector distance of ball to paddle

    # Check if ball hits paddle and is moving down DONE
    if ball.distance(paddle) < 50 and ball_y_distance < 20 and ball_dy < 0:
        if DEBUG:
            print(f"Ball hit paddle at {ball.position()}. Rebounds up.")
        ball_x += 15 * ball_dy # Move ball horizontally
        ball_y += 15           # Move ball up away from paddle
        ball_dy *= -1          # Reverse ball direction to up
        os.system('afplay bounce.mp3&')  # Contact!

    # Ball collision with brick DONE
    for brick in bricks:
        if brick.distance(ball) < 50:
            if DEBUG:
                print(f"Ball hit brick at {brick.position()}. Rebounds down.")
            ball_dy *= -1                # Ball has hit brick; change ball direction
            scoreboard.update_score(POINTS[ROWS.index(int(brick.ycor()))])  # Get score based on row
            brick.goto(1000, 1000)       # Move brick out of playing area

    game_is_running = not scoreboard.is_game_over()

screen.exitonclick()

if __name__ == '__main__':

    print('\nThank you for playing Python Breakout')
