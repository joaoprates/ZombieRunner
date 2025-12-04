import pygame

class Brain(pygame.sprite.Sprite):
    """Projétil lançado pelo chefão."""

    def __init__(self, image_surface, x, y, speed=6):
        super().__init__()
        self.image = image_surface
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()
