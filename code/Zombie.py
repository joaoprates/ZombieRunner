"""
Inimigo zumbi que anda da direita para a esquerda.
"""

from __future__ import annotations

import random
import pygame

from .Const import SCREEN_WIDTH, SCREEN_HEIGHT


class Zombie(pygame.sprite.Sprite):
    """Inimigo que vem em direção ao jogador."""

    def __init__(
        self,
        image_surface: pygame.Surface,
        min_speed: float = 2.0,
        max_speed: float = 5.0,
    ) -> None:
        super().__init__()
        self.base_image = image_surface
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.speed_x = 0.0

        self.reset_position()

    def reset_position(self) -> None:
        """Posiciona o zumbi fora da tela, à direita, em uma altura aleatória."""
        self.image = self.base_image
        self.rect = self.image.get_rect()
        self.rect.left = SCREEN_WIDTH + random.randint(20, 150)
        self.rect.y = random.randint(20, SCREEN_HEIGHT - self.rect.height - 20)
        self.speed_x = random.uniform(self.min_speed, self.max_speed)

    def update(self) -> None:
        self.rect.x -= int(self.speed_x)

        # Se sair da tela pela esquerda, reaparece à direita
        if self.rect.right < 0:
            self.reset_position()
