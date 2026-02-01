from segments import *

class Unit:
    group: sprite.Group|None = None
    image: sprite.Sprite|None = None
    def __init__(self):
        pass
    def update(self, strfunc = "", *ar):
        if strfunc:
            self.image.func[strfunc](*ar)

class Blocks(Unit):
    def __init__(self, x,y):
        self._canv = FBlock(x,y)
        self.dictpomps = {"midtop": Pomp(self.canv.rect.midtop[0]-5, self.canv.rect.midtop[1]+1),
                      "midright": Pomp(self.canv.rect.midright[0]-11, self.canv.rect.midright[1]-5),
                      "midleft": Pomp(self.canv.rect.midleft[0]+1, self.canv.rect.midleft[1]-5),
                      "midbottom": Pomp(self.canv.rect.midbottom[0]-5, self.canv.rect.midbottom[1]-11)
                      }
        self.listpomps: Pomp = [self.dictpomps["midtop"],self.dictpomps["midbottom"],self.dictpomps["midright"],self.dictpomps["midleft"]]
        self.group = sprite.Group([self._canv, *self.listpomps])
        self.rect = self.canv.rect
    def update(self, func: object|None = None, *ar, **kw):
        if func:
            for i in self.group.sprites():
                i.func(ar, kw)
        else:
            self.group.update(ar, kwargs=kw)
 
class Screen(Unit):
    def __init__(self, groups, x, y, w, h):
        self.image = Screen_item(groups, x, y, w, h)
        self.rect = self.image.rect
class Scrim(Unit):
    def __init__(self, groups, x, y, w, h, paint="sprites/Canvas.png"):
        self.image = Scrim_item(groups, x, y, w, h, paint)
        self.rect = self.image.rect