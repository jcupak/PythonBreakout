# Day 86 Python Breakout Game
# 100 Days of Python Code
# Filename: scoreboard.py
# Author:   John J Cupak Jr, jcupak@gmail.com
# History:  2021-06-17 Completed

from turtle import Turtle

ALIGNMENT = "left"
FONT      = ("Courier", 60, "normal")
MAX_SCORE = (14 * 7) + (14 * 5) + (14 * 3) + (14 * 1)  # All bricks cleared


class Scoreboard(Turtle):
    """Displays and updates scoreboard"""

    def __init__(self):
        """Initialized the Scoreboard class"""

        super().__init__()
        self.color("white")
        self.penup()
        self.hideturtle()
        self.score = 0
        self.lives = 3  # Max number of turns
        self.update_scoreboard()

    def update_scoreboard(self):
        """Display single player game score"""

        self.clear()
        self.goto(-380, 210)
        self.write(f"SCORE:{self.score:03}", align=ALIGNMENT, font=FONT)
        self.goto(100, 210)
        self.write(f"LIVES:{self.lives}", align=ALIGNMENT, font=FONT)

        if self.is_game_over():
            self.goto(0,-200)
            self.write(f"GAME OVER!", align="center", font=FONT)

    def update_score(self, points):
        """Updates and displays single player score"""

        self.score += points
        self.update_scoreboard()

    def update_lives(self):
        """Decrements single player turn"""

        self.lives += -1  # Decrement
        self.update_scoreboard()

    def is_game_over(self):
        """Returns true when either highest score achieved or three turns over"""

        return self.score == MAX_SCORE or self.lives == 0

    def reset(self):
        """Resets single player scoreboard"""

        self.score = 0
        self.lives = 3
        self.update_scoreboard()
