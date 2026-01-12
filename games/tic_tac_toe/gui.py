import turtle
from .constants_TTT import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_ROWS, BOARD_COLS, CELL_SIZE, GRID_LINE_WIDTH, GRID_COLOR, \
    X_COLOR, SYMBOL_LINE_WIDTH, SYMBOL_OFFSET_RATIO, O_COLOR, O_RADIUS_RATIO, WIN_COLOR, WIN_LINE_WIDTH

t = turtle.Turtle()
screen = turtle.Screen()

def setup_gui():

    # defining the gui screen properties

    turtle.setup(SCREEN_WIDTH, SCREEN_HEIGHT)
    turtle.setworldcoordinates(-SCREEN_WIDTH // 2, -SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    t.hideturtle()
    t.speed(6)

def draw_board():

    # drawing the tic tac toe board grid lines

    t.pensize(GRID_LINE_WIDTH)
    t.color(GRID_COLOR)

    side = SCREEN_WIDTH // 2
    for i in range(1, BOARD_COLS):
        x = -side + (i * CELL_SIZE)
        t.penup()
        t.goto(x, side)
        t.pendown()
        t.goto(x, -side)
        t.penup()

    for i in range(1, BOARD_ROWS):
        y = side - (i * CELL_SIZE)
        t.penup()
        t.goto(-side, y)
        t.pendown()
        t.goto(side, y)


def draw_x(row_index, col_index):

    # drawing the X symbol in the specified cell based on row and column indices (1, 2, 3)

    t.color(X_COLOR)
    t.pensize(SYMBOL_LINE_WIDTH)
    x = -SCREEN_WIDTH // 2 + (col_index - 1) * CELL_SIZE + CELL_SIZE // 2
    y = SCREEN_HEIGHT // 2 - (row_index - 1) * CELL_SIZE - CELL_SIZE // 2

    offset = CELL_SIZE * SYMBOL_OFFSET_RATIO
    # Draw first diagonal (\)
    t.penup()
    t.goto(x - offset, y + offset)
    t.pendown()
    t.goto(x + offset, y - offset)
    t.penup()

    # Draw second diagonal (/)
    t.goto(x + offset, y + offset)
    t.pendown()
    t.goto(x - offset, y - offset)
    t.penup()
    screen.update()

def draw_o(row_index, col_index):
    """
    מצייר את צורת העיגול בתא המתאים, לפי אינדקסים של שורה ועמודה (1, 2, 3) [2].
    """
    t.color(O_COLOR)
    t.pensize(SYMBOL_LINE_WIDTH)

    x = -SCREEN_WIDTH // 2 + (col_index - 1) * CELL_SIZE + CELL_SIZE // 2
    y = SCREEN_HEIGHT // 2 - (row_index - 1) * CELL_SIZE - CELL_SIZE // 2

    radius = CELL_SIZE * O_RADIUS_RATIO

    t.penup()
    t.goto(x, y - radius)
    t.setheading(0)
    t.pendown()
    t.circle(radius)
    t.penup()
    screen.update()

def mark_winner(start_row, start_col, end_row, end_col):
    """
    מסמן את הרצף המנצח על לוח המשחק באמצעות קו, כנדרש [3].
    הקואורדינטות הן האינדקסים של התאים (1, 2, 3).
    """
    # TODO: 1. קבע צבע בולט (לדוגמה, אדום) ועובי קו גדול (t.color(), t.pensize()).
    # TODO: 2. המר את אינדקסי תא ההתחלה (start_row, start_col) לנקודת פיקסל.
    # TODO: 3. המר את אינדקסי תא הסיום (end_row, end_col) לנקודת פיקסל.
    # TODO: 4. השתמש ב-t.penup(), t.goto(start_pixel) ולאחר מכן t.pendown() ו-t.goto(end_pixel) כדי לצייר קו ישר שמסמן את הניצחון.
    t.color(WIN_COLOR)
    t.pensize(WIN_LINE_WIDTH)

    start_x = -SCREEN_WIDTH // 2 + (start_col - 1) * CELL_SIZE + CELL_SIZE // 2
    start_y = SCREEN_HEIGHT // 2 - (start_row - 1) * CELL_SIZE - CELL_SIZE // 2

    end_x = -SCREEN_WIDTH // 2 + (end_col - 1) * CELL_SIZE + CELL_SIZE // 2
    end_y = SCREEN_HEIGHT // 2 - (end_row - 1) * CELL_SIZE - CELL_SIZE // 2

    t.penup()
    t.goto(start_x, start_y)
    t.pendown()
    t.goto(end_x, end_y)
    t.penup()
    screen.update()

def start_gui_loop():
    """
    מפעיל את לולאת ה-GUI הראשית ושומר את החלון פתוח.
    """
    turtle.done()