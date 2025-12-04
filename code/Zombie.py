"""
Inimigo zumbi que anda da direita para a esquerda.
"""

from __future__ import annotations

import random
import pygame

from .Const import SCREEN_WIDTH, SCREEN_HEIGHT


class Zombie(pygame.sprite.Sprite):
    """Inimigo que se move da direita para a esquerda em direção ao jogador."""

    def __init__(
        self,
        image_surface: pygame.Surface,
        min_speed: float = 2.0,
        max_speed: float = 5.0,
    ) -> None:
        """
        Cria um novo zumbi com velocidade e posição inicial aleatórias.

        Args:
            image_surface: superfície da sprite do zumbi.
            min_speed: velocidade mínima horizontal.
            max_speed: velocidade máxima horizontal.
        """
        super().__init__()
        self.base_image = image_surface
        self.image = self.base_image
        self.rect = self.image.get_rect()

        self.min_speed = min_speed
        self.max_speed = max_speed
        self.speed_x: float = 0.0

        self.reset_position()

    def reset_position(self) -> None:
        """Reposiciona o zumbi fora da tela, no lado direito."""
        self.image = self.base_image
        self.rect = self.image.get_rect()

        # Aparece um pouco fora da tela, para a animação parecer natural
        self.rect.left = SCREEN_WIDTH + random.randint(20, 150)

        # Y aleatório dentro dos limites
        self.rect.y = random.randint(20, SCREEN_HEIGHT - self.rect.height - 20)

        # Velocidade horizontal inicial (float)
        self.speed_x = random.uniform(self.min_speed, self.max_speed)

    def update(self) -> None:
        """Movimenta o zumbi na horizontal e reseta quando sai da tela."""
        # Movimento suave (sem converter para int)
        self.rect.x -= self.speed_x

        # Quando sair totalmente da tela à esquerda, reaparece à direita
        if self.rect.right < 0:
            self.reset_position()
