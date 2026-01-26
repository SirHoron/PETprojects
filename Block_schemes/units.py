from pygame import Surface, sprite

class Blocks(sprite.Sprite):
    def init(self):
        sprite.Sprite.init(self)
        self.image = Surface((50, 50))
        self.image.fill((134, 43, 128))
        self.rect = self.image.get_rect()
        self.rect.center = (1200 / 2, 600 / 2)

class ItemsPanel(sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class Canvas(sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

class ExternalObjects(sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)