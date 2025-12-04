from __future__ import annotations
from .Const import INITIAL_LIVES


class Score:
    """Representa o estado de pontuação do jogador."""

    def __init__(self, initial_lives: int = INITIAL_LIVES) -> None:
        self.initial_lives = initial_lives
        self.points = 0
        self.lives = initial_lives
        self.kills = 0  # novo: zumbis mortos

    def reset(self) -> None:
        """Reinicia os valores de score e vidas."""
        self.points = 0
        self.lives = self.initial_lives
        self.kills = 0

    def add_points(self, amount: int) -> None:
        self.points += max(0, int(amount))

    def lose_life(self, amount: int = 1) -> None:
        self.lives -= max(0, int(amount))

    def add_kill(self, amount: int = 1) -> None:
        """Incrementa o contador de zumbis mortos."""
        self.kills += max(0, int(amount))

    def is_game_over(self) -> bool:
        return self.lives <= 0
