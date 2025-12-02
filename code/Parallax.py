"""
Camadas de parallax para o fundo.
"""

from __future__ import annotations

import pygame

from .Const import SCREEN_WIDTH, SCREEN_HEIGHT


class ParallaxLayer:
    """Uma camada de fundo que se move horizontalmente (parallax)."""

    def __init__(
        self,
        image: pygame.Surface,
        speed: float,
    ) -> None:
        # Garante que a imagem tenha o tamanho da tela ou maior em largura
        self.image = pygame.transform.smoothscale(
            image,
            (max(SCREEN_WIDTH, image.get_width()), SCREEN_HEIGHT),
        )
        self.speed = speed
        self.x = 0.0

    def update(self) -> None:
        self.x -= self.speed
        width = self.image.get_width()
        if self.x <= -width:
            self.x += width

    def draw(self, screen: pygame.Surface) -> None:
        width = self.image.get_width()
        screen.blit(self.image, (int(self.x), 0))
        screen.blit(self.image, (int(self.x) + width, 0))


class ParallaxManager:
    """Controla múltiplas camadas de parallax."""

    def __init__(self, base_image: pygame.Surface) -> None:
        # Duas camadas com velocidades diferentes usando a mesma arte
        darker = base_image.copy()
        darker.fill((40, 40, 40), special_flags=pygame.BLEND_RGB_SUB)

        self.layers: list[ParallaxLayer] = [
            ParallaxLayer(darker, speed=0.5),   # fundo distante
            ParallaxLayer(base_image, speed=1.5),  # frente
        ]

    def update(self) -> None:
        for layer in self.layers:
            layer.update()

    def draw(self, screen: pygame.Surface) -> None:
        for layer in self.layers:
            layer.draw(screen)
