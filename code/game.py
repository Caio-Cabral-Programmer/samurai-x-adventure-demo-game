"""Main game module — manages state machine, game loop, and rendering."""

import random
from enum import Enum, auto

import pygame

from .core.config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    FPS,
    GAME_TITLE,
    SKY_BLUE,
    ASSETS_DIR,
    DB_PATH,
    GROUND_Y,
    INITIAL_SPEED,
    SPEED_INCREMENT,
    SPEED_INCREASE_INTERVAL,
    ENEMY_SPAWN_INTERVAL,
    ENEMY_INTERVAL_DECREASE,
    MIN_ENEMY_INTERVAL,
    CLOUD_Y_RANGE,
    TREE_BASE_Y,
    CLOUD_SPEED_FACTOR,
    TREE_SPEED_FACTOR,
    MAX_NAME_LENGTH,
)
from .core.database import Database
from .assets.loader import AssetLoader
from .entities.ground import Ground
from .entities.player import Player
from .entities.cloud import Cloud
from .entities.tree import Tree
from .systems.audio import AudioManager
from .systems.spawner import Spawner
from .systems.scoring import ScoreManager
from .systems.collision import CollisionSystem
from .ui.menu import MenuRenderer
from .ui.hud import HUDRenderer
from .ui.game_over import GameOverRenderer


class GameState(Enum):
    MENU = auto()
    NAME_SELECT = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    SCOREBOARD = auto()


class Game:
    """Top-level game class that owns the loop and orchestrates all systems."""

    def __init__(self) -> None:
        pygame.init()
        pygame.mixer.init()

        self._screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        self._clock = pygame.time.Clock()

        # Core systems
        self._asset_loader = AssetLoader(ASSETS_DIR)
        self._database = Database(DB_PATH)
        self._audio = AudioManager(self._asset_loader)
        self._score_manager = ScoreManager()
        self._spawner = Spawner(self._asset_loader)
        self._collision = CollisionSystem()

        # UI renderers
        self._menu_renderer = MenuRenderer(self._asset_loader)
        self._hud_renderer = HUDRenderer()
        self._game_over_renderer = GameOverRenderer()

        # Game entities
        self._ground = Ground(self._asset_loader, GROUND_Y)
        self._player = Player(self._asset_loader)
        self._obstacle_group = pygame.sprite.Group()
        self._bird_group = pygame.sprite.Group()
        self._cloud_group = pygame.sprite.Group()
        self._tree_group = pygame.sprite.Group()

        # State
        self._state = GameState.MENU
        self._running = True
        self._speed: float = INITIAL_SPEED
        self._frame_counter = 0
        self._enemy_interval: float = ENEMY_SPAWN_INTERVAL

        # Input
        self._jump_pressed = False
        self._duck_pressed = False

        # Menu / name selection
        self._menu_selection = 0
        self._player_name = ""
        self._name_input = ""
        self._existing_names: list[str] = []
        self._name_list_index = -1

        # Score persistence
        self._high_score = self._fetch_high_score()
        self._score_saved = False

        # Start menu music
        self._audio.play_menu_music()

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _fetch_high_score(self) -> int:
        top = self._database.get_top_scores(1)
        return top[0][1] if top else 0

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    def run(self) -> None:
        while self._running:
            self._handle_events()
            self._update()
            self._render()
            self._clock.tick(FPS)

        self._database.close()
        pygame.quit()

    # ------------------------------------------------------------------
    # Event handling
    # ------------------------------------------------------------------

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                return

            if self._state == GameState.MENU:
                self._handle_menu_event(event)
            elif self._state == GameState.NAME_SELECT:
                self._handle_name_select_event(event)
            elif self._state == GameState.PLAYING:
                self._handle_playing_event(event)
            elif self._state == GameState.GAME_OVER:
                self._handle_game_over_event(event)
            elif self._state == GameState.SCOREBOARD:
                self._handle_scoreboard_event(event)

    def _handle_menu_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key in (pygame.K_ESCAPE, pygame.K_q):
            self._running = False
        elif event.key == pygame.K_UP:
            self._menu_selection = (self._menu_selection - 1) % 3
        elif event.key == pygame.K_DOWN:
            self._menu_selection = (self._menu_selection + 1) % 3
        elif event.key == pygame.K_RETURN:
            if self._menu_selection == 0:
                self._existing_names = self._database.get_player_names()
                self._name_input = ""
                self._name_list_index = -1
                self._state = GameState.NAME_SELECT
            elif self._menu_selection == 1:
                self._state = GameState.SCOREBOARD
            elif self._menu_selection == 2:
                self._running = False

    def _handle_name_select_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_ESCAPE:
            self._state = GameState.MENU
        elif event.key == pygame.K_RETURN:
            name = self._name_input.strip()
            if name:
                self._player_name = name
                self._start_game()
        elif event.key == pygame.K_BACKSPACE:
            self._name_input = self._name_input[:-1]
            self._name_list_index = -1
        elif event.key == pygame.K_UP:
            if self._existing_names:
                if self._name_list_index <= 0:
                    self._name_list_index = 0
                else:
                    self._name_list_index -= 1
                self._name_input = self._existing_names[self._name_list_index]
        elif event.key == pygame.K_DOWN:
            if self._existing_names:
                if self._name_list_index < len(self._existing_names) - 1:
                    self._name_list_index += 1
                    self._name_input = self._existing_names[
                        self._name_list_index
                    ]
        else:
            char = event.unicode
            if char and char.isprintable() and len(self._name_input) < MAX_NAME_LENGTH:
                self._name_input += char
                self._name_list_index = -1

    def _handle_playing_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_ESCAPE, pygame.K_q):
                self._audio.stop_music()
                self._audio.play_menu_music()
                self._state = GameState.MENU
            elif event.key in (pygame.K_SPACE, pygame.K_UP):
                self._jump_pressed = True
                if self._player.alive:
                    self._audio.play_jump()
            elif event.key == pygame.K_DOWN:
                self._duck_pressed = True

        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_SPACE, pygame.K_UP):
                self._jump_pressed = False
            elif event.key == pygame.K_DOWN:
                self._duck_pressed = False

    def _handle_game_over_event(self, event: pygame.event.Event) -> None:
        if event.type != pygame.KEYDOWN:
            return
        if not self._player.is_death_animation_done:
            return

        if event.key == pygame.K_SPACE:
            self._restart_game()
        elif event.key in (pygame.K_ESCAPE, pygame.K_q):
            self._audio.stop_music()
            self._audio.play_menu_music()
            self._state = GameState.MENU

    def _handle_scoreboard_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            self._state = GameState.MENU

    # ------------------------------------------------------------------
    # Game lifecycle
    # ------------------------------------------------------------------

    def _start_game(self) -> None:
        self._reset_game()
        self._audio.stop_music()
        self._audio.play_game_music()
        self._state = GameState.PLAYING

    def _restart_game(self) -> None:
        self._reset_game()
        self._audio.play_game_music()
        self._state = GameState.PLAYING

    def _reset_game(self) -> None:
        self._speed = INITIAL_SPEED
        self._frame_counter = 0
        self._enemy_interval = ENEMY_SPAWN_INTERVAL
        self._score_manager.reset()
        self._player.reset()
        self._score_saved = False

        self._obstacle_group.empty()
        self._bird_group.empty()
        self._cloud_group.empty()
        self._tree_group.empty()

        self._jump_pressed = False
        self._duck_pressed = False

        self._spawn_initial_scenery()

    def _spawn_initial_scenery(self) -> None:
        for _ in range(5):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(*CLOUD_Y_RANGE)
            cloud = Cloud(x, y, self._asset_loader)
            self._cloud_group.add(cloud)

        for _ in range(3):
            x = random.randint(100, SCREEN_WIDTH)
            tree = Tree(x, TREE_BASE_Y, self._asset_loader)
            self._tree_group.add(tree)

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def _update(self) -> None:
        if self._state == GameState.PLAYING:
            self._update_playing()
        elif self._state == GameState.GAME_OVER:
            self._update_game_over()

    def _update_playing(self) -> None:
        if not self._player.alive:
            return

        self._frame_counter += 1

        # Spawning
        self._spawner.tick(
            self._frame_counter,
            self._enemy_interval,
            self._obstacle_group,
            self._bird_group,
            self._cloud_group,
            self._tree_group,
        )

        # Progressive difficulty
        if self._frame_counter % SPEED_INCREASE_INTERVAL == 0:
            self._speed += SPEED_INCREMENT
            self._enemy_interval = max(
                MIN_ENEMY_INTERVAL,
                self._enemy_interval - ENEMY_INTERVAL_DECREASE,
            )

        # Update entities
        self._ground.update(self._speed)
        self._cloud_group.update(self._speed * CLOUD_SPEED_FACTOR)
        self._tree_group.update(self._speed * TREE_SPEED_FACTOR)
        self._obstacle_group.update(self._speed)
        self._bird_group.update(self._speed - 1)
        self._player.update(self._jump_pressed, self._duck_pressed)

        # Collision detection
        if self._collision.check(
            self._player, self._obstacle_group, self._bird_group
        ):
            self._player.die()
            self._speed = 0
            self._audio.play_die()
            self._state = GameState.GAME_OVER
            return

        # Scoring — award points when enemies pass the player
        self._check_scoring()

    def _check_scoring(self) -> None:
        for obstacle in self._obstacle_group:
            if not obstacle.scored and obstacle.rect.right < self._player.rect.left:
                obstacle.scored = True
                self._score_manager.add_obstacle_points()

        for bird in self._bird_group:
            if not bird.scored and bird.rect.right < self._player.rect.left:
                bird.scored = True
                self._score_manager.add_bird_points()

        if self._score_manager.check_checkpoint():
            self._audio.play_checkpoint()

        if self._score_manager.score > self._high_score:
            self._high_score = self._score_manager.score

    def _update_game_over(self) -> None:
        self._player.update(False, False)

        if self._player.is_death_animation_done and not self._score_saved:
            self._database.save_score(
                self._player_name, self._score_manager.score
            )
            self._high_score = max(
                self._high_score, self._score_manager.score
            )
            self._score_saved = True

    # ------------------------------------------------------------------
    # Render
    # ------------------------------------------------------------------

    def _render(self) -> None:
        self._screen.fill(SKY_BLUE)

        if self._state == GameState.MENU:
            self._menu_renderer.render_menu(self._screen, self._menu_selection)

        elif self._state == GameState.NAME_SELECT:
            self._menu_renderer.render_name_select(
                self._screen,
                self._name_input,
                self._existing_names,
                self._name_list_index,
            )

        elif self._state in (GameState.PLAYING, GameState.GAME_OVER):
            self._render_game_scene()
            self._hud_renderer.render(
                self._screen,
                self._score_manager.score,
                self._high_score,
            )
            if (
                self._state == GameState.GAME_OVER
                and self._player.is_death_animation_done
            ):
                self._game_over_renderer.render(
                    self._screen, self._score_manager.score
                )

        elif self._state == GameState.SCOREBOARD:
            scores = self._database.get_top_scores(10)
            self._menu_renderer.render_scoreboard(self._screen, scores)

        pygame.display.update()

    def _render_game_scene(self) -> None:
        # Draw order: sky (filled), clouds, trees, ground, obstacles, birds, player
        self._cloud_group.draw(self._screen)
        self._tree_group.draw(self._screen)
        self._ground.draw(self._screen)
        self._obstacle_group.draw(self._screen)
        self._bird_group.draw(self._screen)
        self._player.draw(self._screen)
