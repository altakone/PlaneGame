import turtle
from turtle import *
import time
import random
SPAWN_LOCATION_X = [420 - ((i-1) * 20) for i in range(1, 44)]
SPAWN_LOCATION_Y = [320 - ((i-1) * 20)for i in range(1, 19)]
LEFT = -1
RIGHT = 1


class Invader(Turtle):
    def __init__(self):
        super().__init__()
        self.shape("enemy_plane.gif")
        self.direction = random.choice([LEFT, RIGHT])
        self.penup()
        self.goto(x=random.choice(SPAWN_LOCATION_X), y=random.choice(SPAWN_LOCATION_Y))


class Game:
    def __init__(self):
        self.invaders = []
        self.create_invaders()
        self.bullets = []

    def check_impact_with_plane(self):
        global plane
        for bullet in self.bullets:
            if abs(bullet.xcor() - plane.xcor()) <= 25 and abs(plane.ycor() - bullet.ycor()) <= 15:
                plane.life -= 1
                board.update()
                bullet.hideturtle()
                self.bullets.remove(bullet)
                bullet.goto(-1000, -1000)
                del bullet

    def fire(self):
        fire = random.randint(1, 39)
        if fire == 10:
            invader = random.choice(self.invaders)
            bullet = Bullet()
            self.bullets.append(bullet)
            bullet.color("green")
            bullet.goto(x=invader.xcor(), y=invader.ycor() - 5)

    def move_bullet(self):
        for bullet in self.bullets:
            if bullet.xcor() + (5 * bullet.direction) > 490 or bullet.xcor() + (5 * bullet.direction) < -490:
                bullet.direction *= -1
            bullet.goto(x=bullet.xcor(), y=bullet.ycor() - 5)

    def check_bul(self):
        for bullet in self.bullets:
            if bullet.ycor() < -400:
                bullet.hideturtle()
                bullet.goto(-1000, -1000)
                self.bullets.remove(bullet)
                del bullet

    def create_invaders(self):
        for _ in range(10):
            invader = Invader()
            self.invaders.append(invader)

    def moving_logic(self):
        for invader in self.invaders:
            if invader.xcor() + (invader.direction * 3) >= 420 or invader.xcor() + (invader.direction * 3) <= -420:
                invader.direction *= -1
            invader.goto(x=invader.xcor() + (invader.direction * 3), y=invader.ycor())

    def check_collusion(self):
        global plane, board
        for invader in self.invaders:
            for bullet in plane.bullet_list:
                if abs(bullet.xcor() - invader.xcor()) < 25 and abs(bullet.ycor() - invader.ycor()) < 15:
                    board.increase_score()
                    invader.goto(invader.xcor(), -1000)
                    invader.hideturtle()
                    self.invaders.remove(invader)
                    del invader
                    bullet.goto(bullet.xcor(), -1000)
                    bullet.hideturtle()
                    plane.bullet_list.remove(bullet)
                    del bullet
                    break


class Bullet(Turtle):
    def __init__(self):
        super().__init__()
        self.penup()
        self.shape("circle")
        self.color("red")
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.speed(0)
        self.direction = random.choice([LEFT, RIGHT])


class Score_board(Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.goto(-450, -350)
        self.score = -1
        self.increase_score()

    def update(self):
        self.clear()
        self.write(arg=f"Score:{self.score}\nLife:{plane.life}", font=("Courier", 24, "bold"))

    def increase_score(self):
        self.clear()
        self.score += 1
        self.write(arg=f"Score:{self.score}\nLife:{plane.life}", font=("Courier", 24, "bold"))


class Plane(Turtle):
    def __init__(self):
        super().__init__()
        self.life = 10
        self.penup()
        self.shape("plane.gif")
        self.start_pos()
        self.bullet_list = []

    def start_pos(self):
        self.goto(x=0, y=-340)

    def move_right(self):
        if self.xcor() <= 450:
            self.goto(x=self.xcor() + 40, y=self.ycor())

    def move_left(self):
        if self.xcor() >= -450:
            self.goto(x=self.xcor() - 40, y=self.ycor())

    def move_up(self):
        if self.ycor() <= -40:
            self.goto(x=self.xcor(), y=self.ycor() + 40)

    def move_down(self):
        if self.ycor() >= -350:
            self.goto(x=self.xcor(), y=self.ycor() - 40)


def shoot(x, y):
    global plane
    bullet = Bullet()
    bullet.goto(plane.xcor(), plane.ycor() + 25)
    plane.bullet_list.append(bullet)


def check_my_bullets():
    global plane
    for B in plane.bullet_list:
        if B.ycor() > 400:
            plane.bullet_list.remove(B)
            B.hideturtle()
            del B


screen = Screen()
screen.setup(width=1000, height=800)
screen.addshape("air.gif")
screen.addshape("plane.gif")
screen.addshape("enemy_plane.gif")
screen.title("Dog fighter")
screen.tracer(0)
background = Turtle()
background.penup()
background.shape("air.gif")
plane = Plane()
game = Game()
screen.listen()
screen.onkey(key="d", fun=plane.move_right)
screen.onkey(key="a", fun=plane.move_left)
screen.onkey(key="w", fun=plane.move_up)
screen.onkey(key="s", fun=plane.move_down)
screen.onclick(fun=shoot)
board = Score_board()


while plane.life > 0:
    time.sleep(0.02)
    screen.update()
    game.moving_logic()
    game.fire()
    for bul in plane.bullet_list:
        bul.goto(x=bul.xcor(), y=bul.ycor() + 25)
        check_my_bullets()
    for bul in game.bullets:
        game.move_bullet()
        game.check_bul()

    game.check_collusion()

    if len(game.invaders) == 0:
        game.create_invaders()

    game.check_impact_with_plane()

screen.mainloop()








