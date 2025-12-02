"""
Lógica principal do jogo: loop, estados, colisões.
"""

from __future__ import annotations

import sys
import random

import pygame

from .Const import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    WINDOW_TITLE,
    WHITE,
    GREEN,
    STATE_MENU,
    STATE_PLAYING,
    STATE_GAME_OVER,
    PLAYER_IMG,
    ZOMBIE_IMG,
    BULLET_IMG,
    BACKGROUND_IMG,
    MENU_BACKGROUND_IMG,
    FONT_FILE,
    SHOOT_SOUND_FILE,
    HIT_SOUND_FILE,
    MUSIC_FILE,
    POINTS_PER_ZOMBIE,
)
from .Background import Background
from .Menu import Menu
from .Player import Player
from .Zombie import Zombie
from .Score import Score


class Game:
    """Classe principal do jogo Zombie Runner."""

    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()

        # Carrega assets
        background_image = self.load_image(BACKGROUND_IMG)
        self.background = Background(background_image)

        self.player_image = self.load_image(PLAYER_IMG, scale=(72, 72))
        self.zombie_image = self.load_image(ZOMBIE_IMG, scale=(72, 72))
        self.bullet_image = self.load_image(BULLET_IMG, scale=(28, 12))

        menu_background_image = self.load_image(
            MENU_BACKGROUND_IMG,
            fallback=background_image,
        )

        self.font_title = self.load_font(FONT_FILE, 42)
        self.font_text = self.load_font(FONT_FILE, 24)

        self.menu = Menu(menu_background_image, self.font_title, self.font_text)

        # Sons
        self.shoot_sound = self.load_sound(SHOOT_SOUND_FILE)
        self.hit_sound = self.load_sound(HIT_SOUND_FILE)
        self.music_loaded = self.load_music(MUSIC_FILE)

        # Estado do jogo
        self.state = STATE_MENU
        self.score = Score()

        # Sprites
        self.all_sprites = pygame.sprite.Group()
        self.zombie_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.player: Player | None = None

        # Inicia no menu, sem rodar a música
        if self.music_loaded:
            pygame.mixer.music.set_volume(0.4)

    # ========= Helpers de carregamento ========= #

    @staticmethod
    def load_image(
        path: str,
        scale: tuple[int, int] | None = None,
        fallback: pygame.Surface | None = None,
    ) -> pygame.Surface:
        try:
            image = pygame.image.load(path).convert_alpha()
        except (pygame.error, FileNotFoundError):
            if fallback is not None:
                image = fallback.copy()
            else:
                # Quadrado cinza padrão
                image = pygame.Surface((100, 100))
                image.fill((80, 80, 80))

        if scale is not None:
            image = pygame.transform.smoothscale(image, scale)

        return image

    @staticmethod
    def load_font(path: str, size: int) -> pygame.font.Font:
        try:
            return pygame.font.Font(path, size)
        except (IOError, FileNotFoundError):
            return pygame.font.SysFont("arial", size)

    @staticmethod
    def load_sound(path: str) -> pygame.mixer.Sound | None:
        try:
            return pygame.mixer.Sound(path)
        except (pygame.error, FileNotFoundError):
            return None

    @staticmethod
    def load_music(path: str) -> bool:
        try:
            pygame.mixer.music.load(path)
            return True
        except (pygame.error, FileNotFoundError):
            return False

    # ========= Setup ========= #

    def start_new_game(self) -> None:
        """Reseta score, recria player e zumbis."""
        self.score.reset()

        self.all_sprites.empty()
        self.zombie_group.empty()
        self.bullet_group.empty()

        self.player = Player(self.player_image)
        self.all_sprites.add(self.player)

        # Cria vários zumbis iniciais
        for _ in range(8):
            zombie = Zombie(self.zombie_image)
            self.all_sprites.add(zombie)
            self.zombie_group.add(zombie)

        if self.music_loaded:
            pygame.mixer.music.play(-1)

        self.state = STATE_PLAYING

    # ========= Loop principal ========= #

    def run(self) -> None:
        running = True
        while running:
            self.clock.tick(FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if self.state == STATE_MENU:
                    self.handle_menu_events(event)
                elif self.state == STATE_PLAYING:
                    self.handle_playing_events(event)
                elif self.state == STATE_GAME_OVER:
                    self.handle_game_over_events(event)

            if self.state == STATE_PLAYING:
                self.update_game()

            self.draw()

        pygame.quit()
        sys.exit()

    # ========= Eventos ========= #

    def handle_menu_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.start_new_game()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def handle_playing_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.player is not None:
                bullet = self.player.shoot(self.bullet_image)
                if bullet is not None:
                    self.all_sprites.add(bullet)
                    self.bullet_group.add(bullet)
                    if self.shoot_sound is not None:
                        self.shoot_sound.play()
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    def handle_game_over_events(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state = STATE_MENU
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # ========= Lógica ========= #

    def update_game(self) -> None:
        """Atualiza fundo, sprites e colisões."""
        self.background.update()
        self.all_sprites.update()

        # Colisão projétil x zumbi
        hits = pygame.sprite.groupcollide(
            self.zombie_group,
            self.bullet_group,
            True,
            True,
        )
        for _ in hits:
            self.score.add_points(POINTS_PER_ZOMBIE)
            if self.hit_sound is not None:
                self.hit_sound.play()

            # Recria novo zumbi sempre que um morre
            zombie = Zombie(self.zombie_image)
            self.all_sprites.add(zombie)
            self.zombie_group.add(zombie)

        # Colisão zumbi x player
        if self.player is not None:
            collisions = pygame.sprite.spritecollide(
                self.player,
                self.zombie_group,
                True,
            )
            if collisions:
                self.score.lose_life(1)
                for _ in collisions:
                    zombie = Zombie(self.zombie_image)
                    self.all_sprites.add(zombie)
                    self.zombie_group.add(zombie)

            if self.score.is_game_over():
                self.state = STATE_GAME_OVER
                if self.music_loaded:
                    pygame.mixer.music.stop()

    # ========= Desenho ========= #

    def draw(self) -> None:
        if self.state == STATE_MENU:
            self.menu.draw_main_menu(self.screen)
        elif self.state == STATE_PLAYING:
            self.draw_playing()
        elif self.state == STATE_GAME_OVER:
            self.menu.draw_game_over(self.screen, self.score.points)

        pygame.display.flip()

    def draw_playing(self) -> None:
        self.background.draw(self.screen)
        self.all_sprites.draw(self.screen)

        # HUD de score e vidas
        score_surf = self.font_text.render(
            f"Score {self.score.points}",
            True,
            WHITE,
        )
        lives_surf = self.font_text.render(
            f"Vidas {self.score.lives}",
            True,
            GREEN,
        )

        self.screen.blit(score_surf, (10, 10))
        self.screen.blit(lives_surf, (10, 40))
