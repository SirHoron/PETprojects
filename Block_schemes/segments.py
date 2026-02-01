from pygame import Surface, sprite, image, transform, Rect

class Segments(sprite.Sprite):
    state = 1
    winsize = (1200,600)
    sprtsize = (1200, 600)
    def __init__(self):
        self.image: Surface
        self.rect: Rect
    def update(self, *args, **kwargs):
        pass
    def resize(self, newsize):
        w,h = self.winsize
        w1,h1 = newsize
        self.image = transform.scale(self.image, (round((w1/w)*self.sprtsize[0]),round((h1/h)*self.sprtsize[1])))
        self.winsize = newsize
    def UpdateStates():
        pass

class Pomp(Segments):
    def __init__(self, x, y, w, h):
        sprite.Sprite.__init__(self)
        self.sprtsize = (w, h)
        self.image = image.load(f"sprites/Помпа.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.func: dict[str, object] = {"resize": self.resize, "update": self.update, "UpdateStates": self.UpdateStates}
    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    def UpdateStates(self):
        if self.state:
            self.image = image.load(f"sprites/Помпа1.png").convert_alpha()
            self.state = 0
        else:
            self.image = image.load(f"sprites/Помпа.png").convert_alpha()
            self.state = 1

class FBlock(Segments):
    def __init__(self, x, y, w, h):
        sprite.Sprite.__init__(self)
        self.sprtsize = (w, h)
        self.image = image.load("sprites/block.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.func: dict[str, object] = {"resize": self.resize, "update": self.update, "UpdateStates": self.UpdateStates}
    def update(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy

    def UpdateStates(self):
        pass

class Screen_item(Segments):
    def __init__(self, groups, x=0, y=0, w=10, h=10):
        sprite.Sprite.__init__(self)
        self.sprtsize = (w, h)
        self.image = image.load("sprites/Screen.jpg").convert_alpha()
        self.image = transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.add(groups)
        self.func: dict[str, object] = {"resize": self.resize, "update": self.update, "UpdateStates": self.UpdateStates}
    def resize(self, newsize):
        pass
        
class Scrim_item(Segments):
    def __init__(self, groups, x=0, y=0, w=10, h=10, paint=""):
        sprite.Sprite.__init__(self)
        self.sprtsize = (w, h)
        self.image = image.load(paint).convert_alpha()
        self.image = transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.add(groups)
        self.func: dict[str, object] = {"resize": self.resize, "update": self.update, "UpdateStates": self.UpdateStates}
    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
        