"""
Fundo do jogo: apenas delega para o gerenciador de parallax.
"""

from __future__ import annotations

import pygame

from .Parallax import ParallaxManager


class Background:
    """Wrapper simples para o parallax (facilita extensão futura)."""

    def __init__(self, base_image: pygame.Surface) -> None:
        self.parallax = ParallaxManager(base_image)

    def update(self) -> None:
        self.parallax.update()

    def draw(self, screen: pygame.Surface) -> None:
        self.parallax.draw(screen)
