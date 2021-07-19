#Manzi Bryan
#Lab 1
#CS 1
#1st October 2018
from cs1lib import *

#Constants and Starting Positions
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 400
PADDLE_HEIGHT = 80
PADDLE_WIDTH = 20
paddle_speed = 4
BOUNDARY_WIDTH = 5
MINIMUM_X = 0
MINIMUM_Y = 0
x_ball = 200
y_ball = 200
BALL_RADIUS = 10
OFFSET = BALL_RADIUS

#BUTTONS USED THROUGHOUT GAME
pressed_a = False
pressed_z = False
pressed_k = False
pressed_m = False
pressed_q = False
pressed_space_bar = False
game_start = False


#DRAW ALL PIECES
def draw_background():
    set_clear_color(0, 0, 0) #Black
    clear()
    set_stroke_color(1, 0, 0)


def draw_boundaries():
    enable_stroke()
    set_stroke_width(BOUNDARY_WIDTH)
    set_stroke_color(0, 0.5, 0.9)
    draw_line(MINIMUM_X, MINIMUM_Y + BOUNDARY_WIDTH/2, WINDOW_WIDTH, MINIMUM_Y + BOUNDARY_WIDTH/2)
    draw_line(MINIMUM_X, WINDOW_HEIGHT - BOUNDARY_WIDTH/2, WINDOW_WIDTH, WINDOW_HEIGHT - BOUNDARY_WIDTH/2)


def draw_paddles():

    disable_stroke()

    #draw left paddle
    set_fill_color(1, 1, 0) #yellow
    draw_rectangle(xl, yl, PADDLE_WIDTH, PADDLE_HEIGHT)

    #draw_right_paddle
    set_fill_color(1, 0, 1) #magenta
    draw_rectangle(xr, yr, -PADDLE_WIDTH, -PADDLE_HEIGHT)

xl = MINIMUM_X #top left corner
yl = MINIMUM_Y + BOUNDARY_WIDTH

xr = WINDOW_WIDTH
yr = WINDOW_HEIGHT - BOUNDARY_WIDTH #bottom right corner


def draw_ball():
    disable_stroke()
    set_fill_color(0, 1, 1)  # blue-green
    draw_circle(x_ball, y_ball, BALL_RADIUS)


def create_all_drawings():
    draw_background()
    draw_boundaries()
    draw_paddles()
    draw_ball()


#MAKING PIECES MOVE: ALL FUNCTIONS AFTER THIS COMMENT WILL BE USED TO MAKE THE BALLS AND PADDLES MOVE


def key_down(key): #This records if one of the four keys is pushed down. Later I will use these booleans to control the paddle
    global pressed_a, pressed_k, pressed_m, pressed_q, pressed_z, pressed_space_bar

    if key == "a":
        pressed_a = True
    elif key == "k":
        pressed_k = True
    elif key == "m":
        pressed_m = True
    elif key == "q":
        quit()
    elif key == "z":
        pressed_z = True
    elif key == " ":
        pressed_space_bar = True


def key_up(key):# If one of the four keys is released, this function negates the previous function. This ensures that we
                #  need to hold down the buttons for long instead of just pressing them once to create motion.
    global pressed_a, pressed_k, pressed_m, pressed_q, pressed_z, pressed_space_bar, x_ball, y_ball
    if key == "a":
        pressed_a = False
    elif key == "k":
        pressed_k = False
    elif key == "m":
        pressed_m = False
    elif key == "q":
        pressed_q = False
    elif key == "z":
        pressed_z = False
    elif key == " ":
        pressed_space_bar = False


def imobilize_game():
    global paddle_speed, x_ball_speed, y_ball_speed
    paddle_speed = 0
    x_ball_speed = 0
    y_ball_speed = 0


def game_stop_and_start():
    global x_ball, y_ball, pressed_space_bar, paddle_speed, x_ball_speed, y_ball_speed, game_start, yl, yr
    if x_ball < BALL_RADIUS or x_ball > WINDOW_WIDTH - BALL_RADIUS:
        enable_stroke()
        set_font_size(12)
        draw_text('Game Over!', (WINDOW_WIDTH/3), WINDOW_HEIGHT/2)
        draw_text('Press Space Bar to Restart', WINDOW_WIDTH/7, WINDOW_HEIGHT/1.6)
        imobilize_game()
    if pressed_space_bar:
        game_start = True
        x_ball = 200
        y_ball = 200
        yl = MINIMUM_Y + BOUNDARY_WIDTH
        yr = WINDOW_HEIGHT - BOUNDARY_WIDTH
        paddle_speed = 5
        x_ball_speed = 0.5
        y_ball_speed = 0.5


def make_paddle_move(): # This is the function which makes the movement.The formula F=F+/- paddle_speed enables us to \
                        # move the paddle because if the boolean is true then the y position of the paddles has to change.

    global xl, yl, xr, yr, paddle_speed
    if pressed_a and yl > BOUNDARY_WIDTH:
        yl = yl - paddle_speed
    if pressed_z and yl < WINDOW_HEIGHT-PADDLE_HEIGHT - BOUNDARY_WIDTH:
        yl = yl + paddle_speed
    if pressed_k and yr > PADDLE_HEIGHT + BOUNDARY_WIDTH:
        yr = yr - paddle_speed
    if pressed_m and yr < WINDOW_HEIGHT - BOUNDARY_WIDTH:
        yr = yr + paddle_speed


def make_ball_move():
    global x_ball, y_ball, x_ball_speed, y_ball_speed, PADDLE_WIDTH, PADDLE_HEIGHT, BALL_RADIUS, WINDOW_HEIGHT, OFFSET,\
        pressed_space_bar, paddle_speed
    if game_start: #Spacebar starts game
        x_ball = x_ball - x_ball_speed
        y_ball = y_ball + y_ball_speed
    if y_ball >= WINDOW_HEIGHT-BALL_RADIUS - BOUNDARY_WIDTH or y_ball <= BALL_RADIUS + BOUNDARY_WIDTH: #Creates boundary at top and bottom wall
        y_ball_speed = - y_ball_speed
    if x_ball <= PADDLE_WIDTH + BALL_RADIUS and yl < y_ball < yl + PADDLE_HEIGHT: #makes ball bounce off of left paddle
        x_ball = x_ball + OFFSET
        x_ball_speed = - x_ball_speed
    if x_ball >= WINDOW_WIDTH - PADDLE_WIDTH - BALL_RADIUS and yr - PADDLE_HEIGHT < y_ball < yr: # makes ball bounce off of right paddle
        x_ball = x_ball - OFFSET
        x_ball_speed = -x_ball_speed


def create_all_motion():
    make_paddle_move()
    make_ball_move()


#THIS FUNCTION CALLS THE TWO MOST IMPORTANT FUNCTIONS, THE ONE WHICH DRAWS EVERYTHING AND THE ONE WHICH MAKES THE DRAWN THINGS MOVE
def play_pong():
    global game_start
    create_all_drawings()
    create_all_motion()
    game_stop_and_start()


start_graphics(play_pong, title = "Atari Pong", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, key_press = key_down, key_release = key_up, framerate=150)