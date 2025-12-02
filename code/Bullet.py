"""
Projétil disparado pelo jogador.
"""

from __future__ import annotations

import pygame


class Bullet(pygame.sprite.Sprite):
    """Projétil que se move para a direita."""

    def __init__(
        self,
        image_surface: pygame.Surface,
        position: tuple[int, int],
        speed: int = 12,
    ) -> None:
        super().__init__()
        self.image = image_surface
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed = speed

    def update(self) -> None:
        self.rect.x += self.speed
        if self.rect.left > pygame.display.get_surface().get_width():
            self.kill()
