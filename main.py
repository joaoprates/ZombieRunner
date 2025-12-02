"""
Ponto de entrada do jogo.

Para rodar:
    python main.py
"""

from code.Game import Game


def main() -> None:
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
