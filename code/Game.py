"""
Lógica principal do jogo: loop, estados, colisões.
"""

from __future__ import annotations

import sys
import random

import pygame

# Imports do boss e do projétil do boss
from .BossZombie import BossZombie
from .Brain import Brain

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
    STATE_GAME_WIN,
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
    HEART_IMG,
    ASSET_DIR,
    STATE_PAUSED
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

        # ----- Carrega assets -----
        background_image = self.load_image(BACKGROUND_IMG)
        self.background = Background(background_image)

        self.player_image = self.load_image(PLAYER_IMG, scale=(72, 72))
        self.zombie_image = self.load_image(ZOMBIE_IMG, scale=(72, 72))
        self.bullet_image = self.load_image(BULLET_IMG, scale=(28, 12))
        self.heart_image = self.load_image(HEART_IMG, scale=(24, 24))

        # Imagens do chefe e do cérebro
        self.boss_image = self.load_image(f"{ASSET_DIR}/boss.png", scale=(150, 150))
        self.brain_image = self.load_image(f"{ASSET_DIR}/brain.png", scale=(32, 32))

        # Menu
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

        # Grupos do chefe
        self.boss_group = pygame.sprite.Group()
        self.brain_group = pygame.sprite.Group()
        self.boss_spawned = False
        self.boss_dead = False

        self.player: Player | None = None

        if self.music_loaded:
            pygame.mixer.music.set_volume(0.4)

        # ----- Dificuldade -----
        self.difficulty_timer = 0
        self.difficulty_level = 1
        self.difficulty_interval = 20000  # 8 segundos

        # ----- Animação de LEVEL UP -----
        self.levelup_effect_time = 0
        self.levelup_text_alpha = 0
        self.levelup_scale = 1.0
        self.LEVELUP_DURATION = 1200
        self.LEVELUP_FLASH_TIME = 180

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
        self.boss_group.empty()
        self.brain_group.empty()

        self.boss_spawned = False
        self.boss_dead = False

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
                elif self.state == STATE_GAME_WIN:
                    self.handle_game_over_events(event)
                elif self.state == STATE_PAUSED:
                    self.handle_paused_events(event)

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
            elif event.key == pygame.K_p:
                self.state = STATE_PAUSED

    def handle_paused_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.state = STATE_PLAYING
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
        """Atualiza fundo, sprites, IA, chefe e colisões."""

        self.background.update()
        self.all_sprites.update()

        # ----- LEVEL UP Animation -----
        self.difficulty_timer += self.clock.get_time()

        if self.levelup_effect_time > 0:
            dt = self.clock.get_time()
            self.levelup_effect_time -= dt
            self.levelup_scale = 1.0 + (self.levelup_effect_time / self.LEVELUP_DURATION) * 0.4
            self.levelup_text_alpha = max(0, self.levelup_text_alpha - dt * 0.5)

        # ----- Dificuldade -----
        if self.difficulty_timer >= self.difficulty_interval:
            self.difficulty_timer = 0
            self.difficulty_level += 1

            # Iniciar efeitos de LEVEL UP
            self.levelup_effect_time = self.LEVELUP_DURATION
            self.levelup_text_alpha = 255
            self.levelup_scale = 1.4

            # Deixar zumbis mais rápidos
            for z in self.zombie_group:
                z.speed_x += 0.3

            # Criar mais zumbis
            for _ in range(self.difficulty_level):
                zombie = Zombie(self.zombie_image)
                self.all_sprites.add(zombie)
                self.zombie_group.add(zombie)

            print(f"[DEBUG] Level aumentado para {self.difficulty_level}")

            # ----- Spawn do Boss -----
            if self.difficulty_level == 5 and not self.boss_spawned:
                boss = BossZombie(self.boss_image, life=20)
                self.boss_group.add(boss)
                self.all_sprites.add(boss)
                self.boss_spawned = True

        # ----- Update Boss (movimento + ataque) -----
        for boss in self.boss_group:
            action = boss.update()
            if action == "ATTACK":
                brain = Brain(self.brain_image, boss.rect.left, boss.rect.centery)
                self.brain_group.add(brain)
                self.all_sprites.add(brain)

        # ----- Colisão tiro x zumbi -----
        hits = pygame.sprite.groupcollide(
            self.zombie_group,
            self.bullet_group,
            True,
            True,
        )

        for _ in hits:
            self.score.add_points(POINTS_PER_ZOMBIE)
            self.score.add_kill(1)

            if self.hit_sound:
                self.hit_sound.play()

            zombie = Zombie(self.zombie_image)
            self.all_sprites.add(zombie)
            self.zombie_group.add(zombie)

        # ----- Colisão tiro x Boss -----
        if self.boss_spawned and not self.boss_dead:
            for boss in self.boss_group:
                hits = pygame.sprite.spritecollide(boss, self.bullet_group, True)
                for _ in hits:
                    died = boss.take_damage(1)
                    if died:
                        boss.kill()
                        self.boss_dead = True
                        self.state = STATE_GAME_WIN
                        if self.music_loaded:
                            pygame.mixer.music.stop()

        # ----- Colisão zumbi x player -----
        if self.player:
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

        # ----- Colisão cérebro x player -----
        if self.player:
            brain_hits = pygame.sprite.spritecollide(
                self.player, self.brain_group, True
            )
            if brain_hits:
                self.score.lose_life(1)
                if self.score.is_game_over():
                    self.state = STATE_GAME_OVER
                    if self.music_loaded:
                        pygame.mixer.music.stop()

        # GAME OVER por vidas
        if self.score.is_game_over() and self.state != STATE_GAME_WIN:
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
        elif self.state == STATE_GAME_WIN:
            self.draw_game_win()
        elif self.state == STATE_PAUSED:
            self.draw_pause()

        pygame.display.flip()

    def draw_playing(self) -> None:
        # Fundo
        self.background.draw(self.screen)

        # Sprites normais
        self.all_sprites.draw(self.screen)

        # ===== HUD =====

        # Corações (vidas)
        heart_spacing = 6
        base_x = 10
        base_y = 10

        if self.heart_image:
            w = self.heart_image.get_width()
            for i in range(self.score.lives):
                x = base_x + i * (w + heart_spacing)
                self.screen.blit(self.heart_image, (x, base_y))

        # SCORE
        score_text = self.font_text.render(
            f"SCORE {self.score.points}", True, WHITE
        )
        self.screen.blit(score_text, (10, base_y + 30))

        # ZUMBIS mortos
        kills_text = self.font_text.render(
            f"ZUMBIS {self.score.kills}", True, GREEN
        )
        self.screen.blit(kills_text, (10, base_y + 60))

        # LEVEL (animação com zoom + flash)
        level_str = f"LEVEL {self.difficulty_level}"
        level_surface = self.font_text.render(level_str, True, WHITE)

        scaled_w = int(level_surface.get_width() * self.levelup_scale)
        scaled_h = int(level_surface.get_height() * self.levelup_scale)
        level_surface = pygame.transform.scale(level_surface, (scaled_w, scaled_h))

        level_x = SCREEN_WIDTH - scaled_w - 10
        level_y = 10

        if self.levelup_effect_time > (self.LEVELUP_DURATION - self.LEVELUP_FLASH_TIME):
            flash_rect = pygame.Rect(level_x - 10, level_y - 5, scaled_w + 20, scaled_h + 10)
            pygame.draw.rect(self.screen, (255, 255, 255), flash_rect)

        self.screen.blit(level_surface, (level_x, level_y))

        # Texto LEVEL UP centralizado
        if self.levelup_text_alpha > 0:
            text = self.font_text.render("LEVEL UP!", True, (255, 215, 0))
            text.set_alpha(self.levelup_text_alpha)
            x = SCREEN_WIDTH // 2 - text.get_width() // 2
            y = SCREEN_HEIGHT // 2 - text.get_height() // 2
            self.screen.blit(text, (x, y))

    def draw_game_win(self):
        self.screen.fill((0, 0, 0))

        trophy = self.font_title.render("🏆 GAME WIN!", True, (255, 215, 0))
        points = self.font_text.render(f"Pontuação: {self.score.points}", True, (255, 255, 255))

        x = SCREEN_WIDTH // 2

        self.screen.blit(trophy, (x - trophy.get_width() // 2, 200))
        self.screen.blit(points, (x - points.get_width() // 2, 280))
    def draw_pause(self):
        # manter o fundo congelado
        self.draw_playing()

        # sobreposição escura
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # texto
        pause_text = self.font_title.render("PAUSADO", True, (255, 255, 255))
        sub_text = self.font_text.render("Pressione P para continuar", True, (200, 200, 200))

        x = SCREEN_WIDTH // 2

        self.screen.blit(pause_text, (x - pause_text.get_width() // 2, 220))
        self.screen.blit(sub_text, (x - sub_text.get_width() // 2, 300))
