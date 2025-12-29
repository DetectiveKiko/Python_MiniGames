# games/four_in_a_row/gui.py

import turtle
from games.four_in_a_row.constants import (
    BOARD_ROWS, BOARD_COLS, SCREEN_WIDTH, SCREEN_HEIGHT,
    CELL_SIZE, SYMBOL_P1
)

screen = turtle.Screen()
t = turtle.Turtle()


def setup_gui():
    screen.setup(SCREEN_WIDTH + 50, SCREEN_HEIGHT + 50)
    screen.title("Four in a Row")
    # Set coordinates so (0,0) is bottom-left
    screen.setworldcoordinates(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
    t.speed(0)
    t.hideturtle()
    screen.tracer(0)


def draw_board():
    t.clear()
    # Draw Blue Background
    t.penup()
    t.goto(0, 0)
    t.color("black")
    t.begin_fill()
    for _ in range(2):
        t.forward(SCREEN_WIDTH)
        t.left(90)
        t.forward(SCREEN_HEIGHT)
        t.left(90)
    t.end_fill()

    # Draw White Slots
    for r in range(BOARD_ROWS):
        for c in range(BOARD_COLS):
            draw_slot(r, c, "white")
    screen.update()


def draw_slot(row, col, color):
    """Draws a circle at the specific row/col."""
    x = col * CELL_SIZE + (CELL_SIZE // 2)
    y = row * CELL_SIZE + (CELL_SIZE // 2)
    radius = CELL_SIZE // 2.5

    t.penup()
    t.goto(x, y - radius)
    t.pendown()
    t.color(color)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()


def drop_piece_visual(row, col, symbol):
    """Updates a slot color based on player symbol."""
    color = "yellow" if symbol == SYMBOL_P1 else "green"
    draw_slot(row, col, color)
    screen.update()