from pygame import init, display, event, QUIT, quit,\
MOUSEMOTION, MOUSEWHEEL, MOUSEBUTTONDOWN, MOUSEBUTTONUP,\
KEYDOWN, KEYUP, RESIZABLE, VIDEORESIZE, time
from units import *
import threading

class data:
    allsprites = sprite.Group()
    blocks = [sprite.Group()]
    keysdel = {1073742048: False, 99: False, 118: False, None: "None"}
    flage = [False, 0]
    count = 1

def main():
    init()
    screen = display.set_mode(size=(1200, 600), flags=RESIZABLE)
    allsprites, keysdel, blocks, flage, count = data.allsprites, data.keysdel, data.blocks, data.flage, data.count
    Canvas1((1200, 600), (0,0,0), allsprites)
    spblock: list[Blocks] = [Blocks((allsprites, blocks[0]), 600, 300)]
    run = True
    clock = time.Clock()
    while run:
        for e in event.get():
            if e.type == QUIT:
                run = False
                continue
            if e.type == MOUSEMOTION:
                if flage[0]:
                    blocks[flage[1]].update(*e.dict["rel"])
                    continue
                for f in range(len(spblock[flage[1]].listpomps)):
                    if spblock[flage[1]].listpomps[f].rect.collidepoint(e.dict["pos"]):
                        spblock[flage[1]].listpomps[f].UpdateStates()
                    else:
                        spblock[flage[1]].listpomps[f].UpdateStatesTo()
                continue
            if e.type == KEYDOWN:
                print(e.dict)
                if type(keysdel.get(e.dict["key"])) == bool:
                    keysdel[e.dict["key"]] = True
                continue
            if e.type == KEYUP:
                if type(keysdel.get(e.dict["key"])) == bool:
                    keysdel[e.dict["key"]] = False
                continue
            if e.type == MOUSEBUTTONDOWN:
                for i in range(len(spblock)):
                    if spblock[i].rect().collidepoint(e.dict["pos"]):
                        flage[0] = True
                        flage[1] = i
            if e.type == MOUSEBUTTONUP:
                flage[0] = False
            if e.type == VIDEORESIZE:
                pass

        if keysdel[1073742048] and keysdel[99]:
            run = False
        if keysdel[1073742048] and keysdel[118]:
            if count:
                blocks.append(sprite.Group())
                spblock.append(Blocks((allsprites, blocks[len(blocks)-1]), 600, 300))
                count = 0
        else:
            count = 1
        allsprites.draw(screen)
        display.update()
        clock.tick(60)
    quit()

if __name__ == "__main__":
    thrd = threading.Thread(target=main, daemon=True)
    thrd.start()
    thrd.join()