import random, time, sys#装载机 干净，利落。
import pygame, pgzrun

WIDTH, HEIGHT = 500, 700#画面不适中， 无背景


class Ship(Actor):
    def __init__(self):
        Actor.__init__(self, 'ship')#套路 头文字
        self.bottom = HEIGHT
        self.centerx = WIDTH / 2
        self.vel = 6#好 +速

    def update(self):
        if keyboard.A:
            self.x -= self.vel
        if keyboard.D:
            self.x += self.vel
        self.clamp_ip(0, 0, WIDTH, HEIGHT)#夹紧 微调

    def launch_rocket(self):#发射
        rocket = Rocket(self.x, self.y-50)#箭位
        game.rockets.append(rocket)

    def hit(self):
        sounds.ship_hit.play()
        time.sleep(3)
        sys.exit()


class Rocket(Actor):
    def __init__(self, x, y):
        Actor.__init__(self, 'rocket')
        sounds.rocket_launch.play()
        self.alive = True#旗帜
        self.x = x
        self.y = y
        self.vel = 10

    def update(self):
        self.y -= self.vel
        if(self.top < 0):
            self.alive = False
        for ufo in game.ufos:
            if self.colliderect(ufo):
                ufo.hit()
                self.alive = False
                return


class UFO(Actor):
    def __init__(self, x, y):
        Actor.__init__(self, 'ufo')
        self.alive = True
        self.x = x
        self.y = y
        self.x_vel = 2
        self.y_vel = 1
        self.bomb_rate = 0.007#炸弹 速度

    def update(self):
        self.x += self.x_vel
        self.y += self.y_vel

        if self.left < 0 and self.x_vel < 0:
            self.x_vel *= -1
        if self.right > WIDTH and self.x_vel > 0:
            self.x_vel *= -1

        if self.top > HEIGHT:
            self.alive = False

        if decide(self.bomb_rate) and self.top > 0:
            self.drop_bomb()

        if self.colliderect(game.ship):
            game.ship.hit()

    def drop_bomb(self):#减少
        game.bombs.append(Bomb(self.center))

    def hit(self):
        sounds.ufo_hit.play()
        self.alive = False


class Bomb(Actor):
    def __init__(self, center):
        Actor.__init__(self, 'bomb')
        sounds.bomb_drop.play()
        self.alive = True
        self.center = center
        self.vel = 5

    def update(self):
        self.y += self.vel
        if self.top > HEIGHT:
            self.alive = False
        if self.colliderect(game.ship):
            game.ship.hit()


class Game:
    def __init__(self):#初始化
        self.ship = Ship()
        self.rockets = []
        self.ufos = []
        self.bombs = []


def make_ufo_squadron(n_ufos):#中队
    return [UFO(i*40, -i*40) for i in range(0, n_ufos)]


def decide(chance):
    return random.random() < chance


def on_mouse_down():
    game.ship.launch_rocket()


def update():
    for actor in game.rockets + game.bombs + game.ufos:
        actor.update()
    game.ship.update()

    game.rockets = [r for r in game.rockets if r.alive]
    game.ufos = [u for u in game.ufos if u.alive]
    game.bombs = [b for b in game.bombs if b.alive]

    if len(game.ufos) == 0:
        game.ufos = make_ufo_squadron(5)#不死乔


def draw():
    screen.fill((255, 255, 255))

    for actor in game.rockets + game.bombs + game.ufos:
        actor.draw()
    game.ship.draw()


game = Game()
pygame.mixer.quit()
pygame.mixer.init(44100, -16, 2, 1024)
pgzrun.go()