import random
from tkinter import *

window = Tk()
w = 1000
h = 600
strength = 4
window.geometry(str(w) + 'x' + str(h))

canvas = Canvas(window, width=w, height=h)
canvas.place(in_=window, x=0, y=0)


class Player:
    def __init__(self):
        self.x = w / 2
        self.y = h / 2
        self.is_jumping = False

    def toggle_is_jumping(self, *args):
        self.is_jumping = False

    def movement(self, direction):
        if direction == "Up":
            self.jump()
        elif direction == "Left":
            for i in range(1, 7):
                window.after(10 * i, lambda *a: self.move("left"))
        elif direction == "Right":
            for i in range(1, 7):
                window.after(10 * i, lambda *a: self.move("right"))

    def jump(self, *args):
        self.is_jumping = True
        for i in range(1, 15):
            window.after(10 * i, lambda *a: self.move("up"))
        window.after(150, self.toggle_is_jumping)

    def move(self, direction):
        if direction == "up":
            self.y -= strength
        elif direction == "down":
            self.y += strength
        elif direction == "left":
            self.x -= strength
        else:
            self.x += strength


class Target:
    def __init__(self):
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)

    def place(self):
        canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill='green', tags="target")


class Enemy:
    def __init__(self):
        self.x = random.randint(0, w)
        self.y = random.randint(0, h)

    def place(self):
        canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill="red")


player = Player()
target = Target()
score = 0
enemies = [Enemy()]
is_failed = False


def restart():
    global player, target, score, enemies
    player = Player()
    target = Target()
    score = 0
    enemies = [Enemy()]
    game()


def game():
    global score, target, is_failed
    canvas.delete("all")
    target.place()
    for enemy in enemies:
        enemy.place()
        if (enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2 <= 100:
            is_failed = True
            break
    if (target.x - player.x) ** 2 + (target.y - player.y) ** 2 <= 100:
        score += 1
        enemies.append(Enemy())
        print(score)
        target = Target()
    if not is_failed:
        if not player.is_jumping:
            player.y += 2
        canvas.create_oval(player.x - 10, player.y - 10, player.x + 10, player.y + 10, fill="#131313")
        canvas.create_text(50, 10, text="Score: " + str(score), font='Arial 14', fill='black')
        window.after(5, game)
    else:
        canvas.delete("all")
        canvas.create_text(w / 2, h / 2, text="Проигрыш!", font='Arial 28', fill='red')
        canvas.create_text(w / 2, h / 2 + 50, text="Счёт: " + str(score), font='Arial 22', fill="green")
        restart_button = Button(bg="black", fg='white', text="еще раз", command=restart)
        restart_button.place(x=w/2-50, y=h/2 + 100, width=100, height=50)


game()


def get_key(*args):
    return args[0][0].keysym


window.bind("<Key-Right>", lambda *args: player.move("right"))
window.bind("<KeyRelease>", lambda *args: player.movement(get_key(args)))

window.mainloop()
