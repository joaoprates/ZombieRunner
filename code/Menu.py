"""
Telas de menu e game over.
"""

from __future__ import annotations

import pygame

from .Const import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WHITE,
    YELLOW,
    RED,
)


class Menu:
    """Responsável por desenhar o menu e a tela de game over."""

    def __init__(
        self,
        background_surface: pygame.Surface,
        title_font: pygame.font.Font,
        text_font: pygame.font.Font,
    ) -> None:
        self.background = pygame.transform.smoothscale(
            background_surface,
            (SCREEN_WIDTH, SCREEN_HEIGHT),
        )
        self.title_font = title_font
        self.text_font = text_font

    def draw_main_menu(self, screen: pygame.Surface) -> None:
        screen.blit(self.background, (0, 0))

        title = self.title_font.render("ZOMBIE RUNNER", True, YELLOW)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 140))
        screen.blit(title, title_rect)

        lines = [
            "Controles",
            "SETAS - mover",
            "SPACE - atirar",
            "ESC - sair",
            "",
            "Pressione ENTER para iniciar",
        ]

        for i, text in enumerate(lines):
            surf = self.text_font.render(text, True, WHITE)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 30))
            screen.blit(surf, rect)

        dev = self.text_font.render("Developed by Pratesdev.com", True, RED)
        dev_rect = dev.get_rect(bottomright=(SCREEN_WIDTH - 12, SCREEN_HEIGHT - 12))
        screen.blit(dev, dev_rect)

    def draw_game_over(
        self,
        screen: pygame.Surface,
        final_score: int,
    ) -> None:
        screen.blit(self.background, (0, 0))

        title = self.title_font.render("GAME OVER", True, RED)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 160))
        screen.blit(title, title_rect)

        score_text = self.text_font.render(
            f"Pontuacao final - {final_score}",
            True,
            WHITE,
        )
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 230))
        screen.blit(score_text, score_rect)

        info_text = self.text_font.render(
            "ENTER - voltar ao menu ou ESC - sair",
            True,
            WHITE,
        )
        info_rect = info_text.get_rect(center=(SCREEN_WIDTH // 2, 290))
        screen.blit(info_text, info_rect)
