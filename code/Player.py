"""
Jogador controlado pelo usuário.
"""

from __future__ import annotations

import pygame

from .Const import SCREEN_HEIGHT
from .Bullet import Bullet


class Player(pygame.sprite.Sprite):
    """Personagem do jogador (sobrevivente)."""

    def __init__(
        self,
        image_surface: pygame.Surface,
        speed: int = 6,
        shot_cooldown_ms: int = 220,
    ) -> None:
        super().__init__()
        self.image = image_surface
        self.rect = self.image.get_rect()
        self.rect.midleft = (40, SCREEN_HEIGHT // 2)

        self.speed = speed
        self.shot_cooldown_ms = shot_cooldown_ms
        self.last_shot_time = 0

    def update(self) -> None:
        keys = pygame.key.get_pressed()

        # Cima
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed

        # Baixo
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Esquerda
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed

        # Direita
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Mantém dentro da tela
        screen = pygame.display.get_surface()
        if screen:
            width, height = screen.get_size()
            self.rect.left = max(0, self.rect.left)
            self.rect.top = max(0, self.rect.top)
            self.rect.right = min(width, self.rect.right)
            self.rect.bottom = min(height, self.rect.bottom)

    def can_shoot(self) -> bool:
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot_time >= self.shot_cooldown_ms

    def shoot(self, bullet_image: pygame.Surface) -> Bullet | None:
        """Cria um projétil, se o cooldown permitir."""
        if not self.can_shoot():
            return None

        bullet = Bullet(bullet_image, self.rect.midright)
        self.last_shot_time = pygame.time.get_ticks()
        return bullet
