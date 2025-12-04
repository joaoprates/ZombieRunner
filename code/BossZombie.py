import pygame
import random
from .Const import SCREEN_WIDTH, SCREEN_HEIGHT

class BossZombie(pygame.sprite.Sprite):
    """Chefão do level 5 (zumbi fortão)."""

    def __init__(self, image_surface: pygame.Surface, life: int = 20):
        super().__init__()
        self.base_image = image_surface
        self.image = self.base_image
        self.rect = self.image.get_rect()

        # vida do chefe (muitos tiros)
        self.max_life = life
        self.life = life

        # posição inicial (fora da tela)
        self.rect.x = SCREEN_WIDTH + 100
        self.rect.y = SCREEN_HEIGHT // 2

        # movimento horizontal inicial
        self.speed_x = 2.0

        # movimento vertical
        self.speed_y = 2.5

        # estado: entrando → parado direita → atirando
        self.entering = True

        # timer de ataque
        self.attack_timer = 0
        self.attack_interval = 1500  # 1.5s por ataque

    def update(self):
        # Fase 1: boss entra na tela
        if self.entering:
            self.rect.x -= self.speed_x
            if self.rect.right <= SCREEN_WIDTH - 120:
                self.entering = False
            return

        # Fase 2: movimento vertical contínuo
        self.rect.y += self.speed_y
        if self.rect.top <= 10 or self.rect.bottom >= SCREEN_HEIGHT - 10:
            self.speed_y *= -1

        # Fase 3: ataque
        self.attack_timer += 16
        if self.attack_timer >= self.attack_interval:
            self.attack_timer = 0
            return "ATTACK"  # sinaliza para o Game criar um cérebro

        return None

    def take_damage(self, amount=1):
        self.life -= amount
        if self.life <= 0:
            return True  # morreu
        return False

