import pygame as pg

pg.init()

WIDTH = 400
HEIGHT = 200

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

INPUTS = {
    'A': {'num': 0, 'pos': (350, 100), 'size': (50, 50)},
    'B': {'num': 1, 'pos': (300, 150), 'size': (50, 50)},
    'X': {'num': 3, 'pos': (300, 50), 'size': (50, 50)},
    'Y': {'num': 4, 'pos': (250, 100), 'size': (50, 50)},
    'ST': {'num': 11, 'pos': (200, 100), 'size': (50, 25)},
    'SEL': {'num': 10, 'pos': (150, 100), 'size': (50, 25)},
    'L': {'num': 6, 'pos': (0, 0), 'size': (75, 25)},
    'R': {'num': 7, 'pos': (325, 0), 'size': (75, 25)},
    'UP': {'num': (1, -1), 'pos': (50, 50), 'size': (50, 50)},
    'DWN': {'num': (1, 1), 'pos': (50, 150), 'size': (50, 50)},
    'LFT': {'num': (0, -1), 'pos': (0, 100), 'size': (50, 50)},
    'RGT': {'num': (0, 1), 'pos': (100, 100), 'size': (50, 50)}
    }


class InputDisplay(pg.Surface):

    def __init__(self, master, number):
        pg.Surface.__init__(self, (WIDTH, HEIGHT))
        self.master = master
        self.rect = self.get_rect()
        self.controller = pg.joystick.Joystick(number)
        self.controller.init()
        self.running = True
        self.buttons = pg.sprite.Group()
        for i in INPUTS.keys():
            if type(INPUTS[i]['num']) == int:
                Button(self, **INPUTS[i])
            else:
                Direction(self, **INPUTS[i])

    def loop(self):
        self.buttons.update()
        self.buttons.draw(self)
        pg.display.update()


class Button(pg.sprite.Sprite):

    def __init__(self, master, num, pos, size):
        self.master = master
        self.num = num
        self.groups = master.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image  = pg.Surface(size)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        joystick = self.master.controller
        if joystick.get_button(self.num):
            self.image.fill(WHITE)
        else:
            self.image.fill(GREEN)


class Direction(pg.sprite.Sprite):

    def __init__(self, master, num, pos, size):
        self.master = master
        self.axis = num[0]
        self.loc = num[1]
        self.groups = master.buttons
        pg.sprite.Sprite.__init__(self, self.groups)
        self.image  = pg.Surface(size)
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos

    def update(self):
        joystick = self.master.controller
        if round(joystick.get_axis(self.axis)) == self.loc:
            self.image.fill(WHITE)
        else:
            self.image.fill(GREEN)


if __name__ == '__main__':
    display = pg.display.set_mode((WIDTH, HEIGHT))
    app = InputDisplay(display, 0)
    print(app.controller.get_init())
    while app.running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                app.running = False
            #print(event)
        display.blit(app, (0, 0))
        app.loop()
    pg.quit()
