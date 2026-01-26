from pygame import init, display, event, QUIT, quit,\
MOUSEMOTION, MOUSEWHEEL, MOUSEBUTTONDOWN, MOUSEBUTTONUP,\
KEYDOWN, KEYUP, RESIZABLE
from units import *
import threading

def main():
    keysdel = {1073742048: False, 99: False, None: "None"}
    init()
    display.set_mode(size=(1200, 600), flags=RESIZABLE)
    run = True
    allsprites = sprite.Group()
    allsprites.add(Blocks())
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
                continue
            if e.type == MOUSEMOTION:
                continue
            if e.type == KEYDOWN:
                if type(keysdel.get(e.dict["key"])) == bool:
                    print(e.dict["key"])
                    keysdel[e.dict["key"]] = True
                continue
            if e.type == KEYUP:
                if type(keysdel.get(e.dict["key"])) == bool:
                    print(e.dict["key"])
                    keysdel[e.dict["key"]] = False
                continue

        if keysdel[1073742048] and keysdel[99]:
            run = False
        
        allsprites.update()
    quit()

if __name__ == "__main__":
    thrd = threading.Thread(target=main, daemon=True)
    thrd.start()
    thrd.join()