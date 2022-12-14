# Implementation of classic arcade game Pong

import PySimpleGUI
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
paddle1_pos = [3, 140]
paddle2_pos = [WIDTH - 3, 140]
paddle1_vel = 0
paddle2_vel = 0
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if direction == LEFT:
        ball_vel = [-random.randrange(120 / 60, 240 / 60), -random.randrange(60 / 60, 180 / 60)]
    if direction == RIGHT:
        ball_vel = (random.randrange(120/60, 240/60), -random.randrange(60 / 60, 180 / 60))


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    spawn_ball(random.choice([LEFT, RIGHT]))
    score1 = 0
    score2 = 0


def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, paddle1_vel, paddle2_vel
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    if paddle1_pos[1] <= 0 or paddle1_pos[1] >= 320:
        paddle1_vel = 0
    if paddle2_pos[1] <= 0 or paddle2_pos[1] >= 320:
        paddle2_vel = 0

    # draw paddles
    canvas.draw_line(paddle1_pos, [paddle1_pos[0], paddle1_pos[1] + PAD_HEIGHT], PAD_WIDTH, 'White')
    canvas.draw_line(paddle2_pos, [paddle2_pos[0], paddle2_pos[1] + PAD_HEIGHT], PAD_WIDTH, 'White')

    # determine whether paddle and ball collide
    if (ball_pos[0] <= BALL_RADIUS + 11) and (
            ball_pos[1] >= paddle1_pos[1] and ball_pos[1] <= paddle1_pos[1] + PAD_HEIGHT):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] += 0.1 * ball_vel[0]
    if (ball_pos[0] >= WIDTH - BALL_RADIUS - 11) and (
            ball_pos[1] >= paddle2_pos[1] and ball_pos[1] <= paddle2_pos[1] + PAD_HEIGHT):
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] += 0.1 * ball_vel[0]
    if ball_pos[0] < BALL_RADIUS:
        spawn_ball(RIGHT)
        score2 += 1
    if ball_pos[0] > WIDTH - BALL_RADIUS:
        spawn_ball(LEFT)
        score1 += 1
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = -ball_vel[1]

    # draw scores
    canvas.draw_text(str(score1), (150, 40), 30, 'White')
    canvas.draw_text(str(score2), (450, 40), 30, 'White')


def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == PySimpleGUI.KEY_MAP["w"] and paddle1_pos[1] > 0:
        paddle1_vel -= 5
    if key == PySimpleGUI.KEY_MAP["s"] and paddle1_pos[1] < 320:
        paddle1_vel += 5
    if key == PySimpleGUI.KEY_MAP["up"] and paddle2_pos[1] > 0:
        paddle2_vel -= 5
    if key == PySimpleGUI.KEY_MAP["down"] and paddle2_pos[1] < 320:
        paddle2_vel += 5


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == PySimpleGUI.KEY_MAP["w"] or key == PySimpleGUI.KEY_MAP["s"]:
        paddle1_vel = 0
    if key == PySimpleGUI.KEY_MAP["up"] or key == PySimpleGUI.KEY_MAP["down"]:
        paddle2_vel = 0


def reset_handler():
    new_game()


# create frame
frame = PySimpleGUI.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
button1 = frame.add_button('Reset', reset_handler)

# start frame
new_game()
frame.start()
