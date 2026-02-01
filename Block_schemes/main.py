from pygame import init, display, event, QUIT, quit,\
MOUSEMOTION, MOUSEWHEEL, MOUSEBUTTONDOWN, MOUSEBUTTONUP,\
KEYDOWN, KEYUP, RESIZABLE, VIDEORESIZE, time
from units import *
import threading

class Unit_Group:
    def __init__(self, *args):
        self.spgroup = sprite.Group()
        self.listunit: list[Unit] = []
        if args:
            self.listunit.append(*args)
            for i in self.listunit:
                if i.group:
                    self.spgroup.add(i.group.sprites())
                else:
                    self.spgroup.add(i.image)
    def add(self, *args):
        self.listunit.append(*args)
        for i in args:
            if i.group:
                self.spgroup.add(i.group.sprites())
            else:
                self.spgroup.add(i.image)
    def update(self, func=None, *args):
        for i in self.listunit:
            i.update(func, *args)

class data:
    keysdel = {1073742048: False, 99: False, 118: False, None: "None"}

def main():
    init()
    MainScreen = display.set_mode(size=(1200, 600), flags=RESIZABLE)
    scrimsprites = Unit_Group()
    screensprites = Unit_Group()
    w, h = display.get_desktop_sizes()[0]
    screensprites.add(Screen(screensprites.spgroup, 0, 0, w, h))
    scrimsprites.add(Scrim(scrimsprites.spgroup, 0,120,1200,480))
    scrimsprites.add(Scrim(scrimsprites.spgroup, 0,0,1200,120, "sprites/Canvas1.png"))
    run = True
    clock = time.Clock()
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
                continue
            if e.type == MOUSEMOTION:
                pass
            if e.type == KEYDOWN:
                pass
            if e.type == KEYUP:
                pass
            if e.type == MOUSEBUTTONDOWN:
                pass
            if e.type == MOUSEBUTTONUP:
                pass
            if e.type == VIDEORESIZE:
                screensprites.update("resize", e.dict["size"])
                scrimsprites.update("resize", e.dict["size"])

        scrimsprites.spgroup.draw(screensprites.listunit[0].image.image)
        screensprites.spgroup.draw(MainScreen)
        display.update()
        clock.tick(60)
    quit()

if __name__ == "__main__":
    thrd = threading.Thread(target=main, daemon=True)
    thrd.start()
    thrd.join()