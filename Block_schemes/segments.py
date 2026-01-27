from pygame import Surface, sprite, image, transform

class Pomp(sprite.Sprite):
    def __init__(self, groups, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load(f"sprites/Помпа.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.add(groups)
    def update(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy
    def UpdateStates(self):
        self.image = image.load(f"sprites/Помпа1.png").convert_alpha()
    def UpdateStatesTo(self):
        self.image = image.load(f"sprites/Помпа.png").convert_alpha()

class FBlock(sprite.Sprite):
    def __init__(self, group, x, y):
        sprite.Sprite.__init__(self)
        self.image = image.load("sprites/block.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x,y))
        self.add(group)
    def update(self, dx, dy):
        self.rect.centerx += dx
        self.rect.centery += dy