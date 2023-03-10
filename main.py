import os
import random
from tkinter import *
from pygame import mixer
mixer.init()

window = Tk()
w = 1000
h = 600
strength = 4
window.resizable(False, False)
window.geometry(str(w) + 'x' + str(h))
mixer.music.set_volume(0.2)

canvas = Canvas(window, width=w, height=h, bg="white")
canvas.place(in_=window, x=0, y=0)
controls_image = PhotoImage(file="controls.png")

collected_images = [PhotoImage(file="img/collected_1.png"), PhotoImage(file="img/collected_2.png")]
failed_images = [PhotoImage(file="img/failed_1.png"), PhotoImage(file="img/failed_2.png"), PhotoImage(file="img/failed_3.png")]


def play_sound(name):
    mixer.music.unload()
    mixer.music.load(os.path.join(os.path.dirname(__file__), 'sounds', name))
    mixer.music.play()


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
        global is_started
        is_started = True
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
        canvas.create_oval(self.x - 5, self.y - 5, self.x + 5, self.y + 5, fill="red", tags="enemy")


player = Player()
target = Target()
score = 0
enemies = [Enemy()]
is_started = False
is_failed = False
collected_img = None


def reset_collected_img():
    global collected_img
    collected_img = None


def restart():
    global player, target, score, enemies, is_failed, restart_button, is_started
    player = Player()
    target = Target()
    score = 0
    enemies = [Enemy()]
    is_failed = False
    restart_button.place_forget()
    mixer.music.unload()
    is_started = False
    game()


restart_button = Button(bg="black", fg='white', text="?????? ??????", command=restart)


def game():
    global score, target, is_failed, collected_img
    canvas.delete("all")
    if not is_started:
        canvas.create_image(100, h-100, image=controls_image)
    if collected_img:
        canvas.create_image(100, h-100, image=collected_img, tags="collect_img")
    target.place()
    for enemy in enemies:
        enemy.place()
        if (enemy.x - player.x) ** 2 + (enemy.y - player.y) ** 2 <= 100:
            is_failed = True
            break
    if player.x < -10 or player.x > 1010 or player.y > 610 or player.y < -10:
        is_failed = True
    if (target.x - player.x) ** 2 + (target.y - player.y) ** 2 <= 100:
        score += 1
        collected_img = collected_images[random.randint(0, len(collected_images) - 1)]
        window.after(1000, reset_collected_img)
        play_sound(f'collect\\{random.randint(1,4)}.mp3')
        enemies.append(Enemy())
        target = Target()
    if not is_failed:
        if not player.is_jumping and is_started:
            player.y += 2
        canvas.create_oval(player.x - 10, player.y - 10, player.x + 10, player.y + 10, fill="#131313", tags="player")
        canvas.create_text(50, 10, text="Score: " + str(score), font='Arial 14', fill='black')
        window.after(5, game)
    else:
        canvas.delete("all")
        play_sound(f'fail\\{random.randint(1,5)}.mp3')
        canvas.create_image(100, h-100, image=failed_images[random.randint(0, len(failed_images) - 1)], tags="failed_img")
        canvas.create_text(w / 2, h / 2, text="????????????????!", font='Arial 28', fill='red')
        canvas.create_text(w / 2, h / 2 + 50, text="????????: " + str(score), font='Arial 22', fill="green")
        restart_button.place(x=w/2-50, y=h/2 + 100, width=100, height=50)


game()


def get_key(*args):
    return args[0][0].keysym


window.bind("<KeyRelease>", lambda *args: player.movement(get_key(args)))

window.mainloop()
