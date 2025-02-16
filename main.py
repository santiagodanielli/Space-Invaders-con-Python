import random
import time
import turtle

CANNON_STEP = 10
LASER_LENGTH = 20
LASER_SPEED = 10
ALIEN_SPAWN_INTERVAL = 1.2  # Seconds
ALIEN_SPEED = 0.1

window = turtle.Screen()
window.tracer(0)
window.setup(0.5, 0.75)
window.bgcolor(0.2, 0.2, 0.2)
window.title("Space Invader con Turtle")

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

# canon laser
cannon = turtle.Turtle()
cannon.penup()
cannon.color(1, 1, 1)
cannon.shape("square")
cannon.setposition(0, FLOOR_LEVEL)

# timer
text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(LEFT * 0.8, TOP * 0.8)
text.color(1, 1, 1)

lasers = []
aliens = []


def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 10)
    cannon.turtlesize(1, 1.5)
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 20)
    cannon.turtlesize(0.8, 0.3)
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL)


def move_left():
    new_x = cannon.xcor() - CANNON_STEP
    if new_x >= LEFT + GUTTER:
        cannon.setx(new_x)
        draw_cannon()


def move_right():
    new_x = cannon.xcor() + CANNON_STEP
    if new_x <= RIGHT - GUTTER:
        cannon.setx(new_x)
        draw_cannon()


def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color(1, 0, 0)
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor())
    laser.setheading(90)
    # mover laser
    laser.forward(20)
    # preparar para dibujar laser
    laser.pendown()
    laser.pensize(5)

    lasers.append(laser)


def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    # dibujar laser
    laser.forward(LASER_LENGTH)
    laser.forward(-LASER_LENGTH)


def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(1.5)
    alien.setposition(
        random.randint(
            int(LEFT + GUTTER),
            int(RIGHT - GUTTER),
        ),
        TOP,
    )
    alien.shape("turtle")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())
    aliens.append(alien)


def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)
    turtle.turtles().remove(sprite)


# comandos de juego
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeypress(create_laser, "space")
window.onkeypress(turtle.bye, "q")
window.listen()

draw_cannon()

# loop
alien_timer = 0
game_timer = time.time()
score = 0
game_running = True
while game_running:
    time_elapsed = time.time() - game_timer
    text.clear()
    text.write(
        f"Time: {time_elapsed:5.1f}s\nScore: {score:5}",
        font=("Courier", 20, "bold"),
    )
    # mover laser
    for laser in lasers.copy():
        move_laser(laser)
        # remover laser cuando sale de pantalla
        if laser.ycor() > TOP:
            remove_sprite(laser, lasers)
            break
        # colision con alien
        for alien in aliens.copy():
            if laser.distance(alien) < 20:
                remove_sprite(laser, lasers)
                remove_sprite(alien, aliens)
                score += 1
                break
    # nuevos alien cuando termine intervalo de tiempo
    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        create_alien()
        alien_timer = time.time()

    # mover alien
    for alien in aliens:
        alien.forward(ALIEN_SPEED)
        if alien.ycor() < FLOOR_LEVEL:
            game_running = False
            break
    window.update()

# game over
splash_text = turtle.Turtle()
splash_text.hideturtle()
splash_text.color(1, 1, 1)
splash_text.write("GAME OVER", font=("Courier", 40, "bold"), align="center")

turtle.done()