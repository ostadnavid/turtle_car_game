import turtle
import time
import numpy as np
import random
import sys

if sys.platform == 'win32':
    import winsound


def play_sound(fname):
    if sys.platform == 'win32':
        winsound.PlaySound(fname, winsound.SND_ASYNC)


# changing these values a lot might broke the game
w, h = 600, 600
step = 20
fire_timer = 70
num_blocks = 1
cols_rate = 8
block_generation_rate = 70

font = 'Bitstream Vera Sans Mono'

score = 0
high_score = 0

x_range = np.arange(-1 * step * cols_rate, step * cols_rate + 1, step*1.5).tolist()

wn = turtle.Screen()
wn.setup(w, h)
wn.bgcolor('black')
wn.tracer(0)
wn.title('car game by @ostadpold')

car = turtle.Turtle()
car.shape('square')
car.penup()
car.speed(0)
car.color('white')
car.goto(random.choice(x_range), -1 * h / 2 + step * 3)
car.direction = 'stop'

pen_content = 'Score: {}\nHigh Score: {}\nFire: {}'

pen = turtle.Turtle()
pen.speed(0)
pen.shape('square')
pen.color('white')
pen.penup()
pen.hideturtle()
pen.goto(-1 * w / 2 + 100, h / 2 - 100)
pen.write(pen_content.format(score, high_score, 'Not Ready'), align='center', font=(font, 16, 'normal'))
# 5 column

print('columns: ',len(x_range))

def make_border():
    for x in x_range:
        p = turtle.Turtle()
        p.hideturtle()
        p.pencolor('gray')
        p.penup()
        p.speed(0)
        p.goto(x, -1*h/2)
        p.pendown()
        p.goto(x, h/2)

make_border()

def compute_score():
    global passed_blocks
    return passed_blocks / 10


def move_blocks():
    global passed_blocks
    if car.direction != 'stop':
        for block in blocks:
            if block.ycor() < -1 * h / 2 - step:
                block.sety(h / 2)
                block.setx(random.choice(x_range))
                passed_blocks += 1
            else:
                block.sety(block.ycor() - step)


def go_up():
    if car.ycor() < h / 2 - step * 2:
        car.sety(car.ycor() + step)


def go_down():
    if car.ycor() > -1 * h / 2 + step * 2:
        car.sety(car.ycor() - step)


def go_left():
    if car.xcor() > min(x_range):
        car.setx(car.xcor() - step * 1.5)


def go_right():
    if car.xcor() < max(x_range):
        car.setx(car.xcor() + step * 1.5)


def fire():
    global fire_coldown
    global fires
    global ready_fires

    if ready_fires != 0:
        play_sound('audios\\laser_shot.wav')
        fire = turtle.Turtle('square')
        fire.color('blue')
        fire.penup()
        fire.shapesize(1.5, .5, 1)
        fire.speed(0)
        fire.goto(car.xcor(), car.ycor() + step)

        fires.append(fire)

        ready_fires -= 1


def get_random_block():
    block = turtle.Turtle()
    block.shape('square')
    block.color('red')
    block.penup()
    block.speed(0)
    block.goto(random.choice(x_range), h / 2)

    return block


def reset():
    global blocks
    global high_score
    global score
    global passed_blocks
    global n_iterations
    global car
    global done
    global fires
    global fire_coldown
    global ready_fires

    play_sound('audios\\game_over.wav')
    for block in blocks:
        block.goto(0, 1000)
    for fire in fires:
        fire.goto(0,-1000)
    blocks = []
    fires = []

    done = False
    n_iterations = 0
    passed_blocks = 0
    car.direction = 'stop'
    if high_score < score:
        high_score = score
    score = 0

    car.goto(random.choice(x_range), -1 * h / 2 + step * 3)
    fire_coldown = fire_timer
    ready_fires = 0


def move_fires():
    global fires

    for fire in fires:
        if fire.ycor() < h / 2 + step:
            fire.goto(fire.xcor(), fire.ycor() + step)
        else:
            fires.remove(fire)


def collision_with_blocks():
    for block in blocks:
        if block.xcor() == car.xcor() and car.distance(block) < 25:
            return True
    return False


def collision_with_fires():
    for block in blocks:
        for fire in fires:
            if fire.distance(block) <= 25 and block.xcor() == fire.xcor():
                fire.goto(0, 1000)
                block.goto(0, -1000)
                fires.remove(fire)


def write_pen(fire=False):
    global pen
    global ready_fires
    if ready_fires > 0:
        fire = f'Ready({ready_fires})'
    else:
        fire = f'Not Ready({fire})'
    pen.clear()
    pen.write(pen_content.format(score, high_score, fire), align='center', font=(font, 16, 'normal'))

def make_move(move):
    if move == 'fire':
        fire()
    elif move == 'up':
        go_up()
    elif move == 'left':
        go_left()
    elif move == 'right':
        go_right()
    elif move == 'down':
        go_down()

wn.listen()
wn.onkeypress(go_left, 'a')
wn.onkeypress(go_right, 'd')
wn.onkeypress(go_up, 'w')
wn.onkeypress(go_down, 's')
wn.onkeypress(fire, ' ')

blocks = []
fires = []
n_iterations = 0
passed_blocks = 0
fire_coldown = fire_timer
ready_fires = 0

done = False

while True:
    score = compute_score()
    write_pen(fire_coldown)
    if 0 < fire_coldown:
        fire_coldown -= 1
    if fire_coldown == 0:
        play_sound('audios\\fire_ready.wav')
        ready_fires += 1
        fire_coldown = fire_timer
        write_pen(0)

    # random_move = random.choice(['fire', 'up', 'down', 'right', 'left'])
    # make_move(random_move)
    wn.update()

    if done:
        reset()
        time.sleep(2.5)
    # beginning of the game
    if car.direction == 'stop':
        car.direction = 'go'

    # add block to game
    if n_iterations % block_generation_rate == 0 and len(blocks) < num_blocks:
        blocks.append(get_random_block())

    move_blocks()
    move_fires()

    collision_with_fires()
    if collision_with_blocks():
        done = True

    n_iterations += 1
    time.sleep(.1)
