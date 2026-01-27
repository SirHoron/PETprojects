from segments import *

class Blocks():
    def __init__(self, group,x,y):
        self.canv = FBlock(group, x,y)
        self.dictpomps = {"midtop": Pomp(group, self.canv.rect.midtop[0]-5, self.canv.rect.midtop[1]+1),
                      "midright": Pomp(group, self.canv.rect.midright[0]-11, self.canv.rect.midright[1]-5),
                      "midleft": Pomp(group, self.canv.rect.midleft[0]+1, self.canv.rect.midleft[1]-5),
                      "midbottom": Pomp(group, self.canv.rect.midbottom[0]-5, self.canv.rect.midbottom[1]-11)
                      }
        self.listpomps: Pomp = [self.dictpomps["midtop"],self.dictpomps["midbottom"],self.dictpomps["midright"],self.dictpomps["midleft"]]
    def rect(self):
        return self.canv.rect

class Canvas1(sprite.Sprite):
    def __init__(self, surf, color, group):
        sprite.Sprite.__init__(self)
        self.image = Surface(surf)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(1200 / 2, 600 / 2))
        self.add(group)
    def update(self):
        pass
class Node(sprite.Sprite):
    def __init__(self, group):
        sprite.Sprite.__init__(self)
        self.image = image.load("sprites/Node.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(1200 / 2, 600 / 2))
        self.add(group)
    def update(self):
        self.image = transform.rotozoom(self.image, 45, 2.0)

class ItemsPanel(sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class Canvas(sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class ExternalObjects(sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)