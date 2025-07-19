"""
파일명: Ex25-01-Snake.py

pip install pygame

"""

import pygame
import random
import sys
from enum import Enum

"""
Pygame Snake Game
-----------------
Features:
- Grid based movement
- Arrow / WASD control
- Pause (P), Restart (R), Quit (ESC)
- Increasing speed as snake grows
- Score + High score (session)
- Simple state machine (MENU, RUNNING, PAUSED, GAME_OVER)
- Optional wall wrap toggle (press W during menu to toggle)
- Fruit types: normal (1 point), golden (5 points, appears occasionally, timed)
- Basic sound placeholders (you can add .wav files) handled gracefully if missing

Author: ChatGPT
"""

# ---------------- Configuration ---------------- #
CELL_SIZE = 24
GRID_WIDTH = 25   # number of cells horizontally
GRID_HEIGHT = 20  # number of cells vertically
INITIAL_SNAKE_LENGTH = 4
INITIAL_SPEED = 8            # frames per second baseline
SPEED_INCREMENT_EVERY = 4    # increase speed every N eaten fruits
MAX_SPEED = 25
GOLDEN_FRUIT_CHANCE = 0.12   # probability when spawning a fruit
GOLDEN_FRUIT_TIME = 6.0      # seconds before golden fruit expires
FONT_NAME = "consolas"
WINDOW_MARGIN = 80           # for HUD area at top
BG_COLOR = (16, 18, 24)
GRID_COLOR = (35, 40, 50)
SNAKE_HEAD_COLOR = (0, 220, 140)
SNAKE_BODY_COLOR = (0, 150, 100)
FRUIT_COLOR = (230, 60, 60)
GOLDEN_FRUIT_COLOR = (255, 200, 0)
TEXT_COLOR = (230, 230, 240)
SHADOW_COLOR = (0, 0, 0)

SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = WINDOW_MARGIN + CELL_SIZE * GRID_HEIGHT

class GameState(Enum):
    MENU = 0
    RUNNING = 1
    PAUSED = 2
    GAME_OVER = 3

class FruitType(Enum):
    NORMAL = 1
    GOLDEN = 2

class Fruit:
    def __init__(self, position, fruit_type=FruitType.NORMAL, lifetime=None):
        self.position = position
        self.type = fruit_type
        self.lifetime = lifetime  # seconds remaining (for golden)

    def update(self, dt):
        if self.type == FruitType.GOLDEN and self.lifetime is not None:
            self.lifetime -= dt
            if self.lifetime <= 0:
                return False
        return True

class Snake:
    def __init__(self, start_length=INITIAL_SNAKE_LENGTH):
        self.reset(start_length)

    def reset(self, start_length=INITIAL_SNAKE_LENGTH):
        cx = GRID_WIDTH // 2
        cy = GRID_HEIGHT // 2
        self.direction = (1, 0)
        self.next_direction = (1, 0)
        self.body = [(cx - i, cy) for i in range(start_length)]  # head first
        self.grow_segments = 0

    def set_direction(self, dx, dy):
        # Prevent reversing directly
        if (-dx, -dy) == self.direction:
            return
        self.next_direction = (dx, dy)

    def move(self, wrap_walls):
        self.direction = self.next_direction
        head_x, head_y = self.body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)

        if wrap_walls:
            new_head = (new_head[0] % GRID_WIDTH, new_head[1] % GRID_HEIGHT)
        else:
            if not (0 <= new_head[0] < GRID_WIDTH and 0 <= new_head[1] < GRID_HEIGHT):
                return False  # collision with wall

        if new_head in self.body:
            return False  # self collision

        self.body.insert(0, new_head)
        if self.grow_segments > 0:
            self.grow_segments -= 1
        else:
            self.body.pop()
        return True

    def grow(self, amount=1):
        self.grow_segments += amount

    def head(self):
        return self.body[0]

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game (Pygame)")
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.SysFont(FONT_NAME, 18)
        self.font = pygame.font.SysFont(FONT_NAME, 24, bold=True)
        self.font_large = pygame.font.SysFont(FONT_NAME, 46, bold=True)
        self.state = GameState.MENU
        self.snake = Snake()
        self.wrap_walls = False
        self.fruit = None
        self.score = 0
        self.high_score = 0
        self.eaten_count = 0
        self.speed = INITIAL_SPEED
        self.elapsed = 0
        self.load_sounds()
        self.spawn_fruit()

    def load_sounds(self):
        self.snd_eat = self.safe_sound("eat.wav")
        self.snd_gameover = self.safe_sound("gameover.wav")
        self.snd_golden = self.safe_sound("golden.wav")

    @staticmethod
    def safe_sound(path):
        try:
            return pygame.mixer.Sound(path)
        except Exception:
            return None

    def play_sound(self, snd):
        if snd:
            snd.play()

    def spawn_fruit(self):
        empty = [(x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT) if (x, y) not in self.snake.body]
        if not empty:
            return
        pos = random.choice(empty)
        # Decide fruit type
        if random.random() < GOLDEN_FRUIT_CHANCE:
            self.fruit = Fruit(pos, FruitType.GOLDEN, GOLDEN_FRUIT_TIME)
        else:
            self.fruit = Fruit(pos, FruitType.NORMAL)

    def eat_fruit(self):
        if self.fruit.type == FruitType.GOLDEN:
            self.score += 5
            self.snake.grow(3)
            self.play_sound(self.snd_golden)
        else:
            self.score += 1
            self.snake.grow(1)
            self.play_sound(self.snd_eat)
        self.eaten_count += 1
        if self.eaten_count % SPEED_INCREMENT_EVERY == 0 and self.speed < MAX_SPEED:
            self.speed += 1
        self.spawn_fruit()

    def reset_game(self):
        self.snake.reset()
        self.score = 0
        self.eaten_count = 0
        self.speed = INITIAL_SPEED
        self.spawn_fruit()
        self.state = GameState.RUNNING

    def update(self, dt):
        if self.state != GameState.RUNNING:
            return
        self.elapsed += dt
        # Update fruit lifetime if golden
        if self.fruit and not self.fruit.update(dt):
            self.spawn_fruit()
        moved = self.snake.move(self.wrap_walls)
        if not moved:
            self.game_over()
            return
        # Check fruit collision
        if self.fruit and self.snake.head() == self.fruit.position:
            self.eat_fruit()

    def game_over(self):
        self.play_sound(self.snd_gameover)
        if self.score > self.high_score:
            self.high_score = self.score
        self.state = GameState.GAME_OVER

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            key = event.key
            if self.state == GameState.MENU:
                if key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.reset_game()
                elif key == pygame.K_w:  # toggle wrap
                    self.wrap_walls = not self.wrap_walls
                elif key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
            elif self.state == GameState.RUNNING:
                if key in (pygame.K_UP, pygame.K_w):
                    self.snake.set_direction(0, -1)
                elif key in (pygame.K_DOWN, pygame.K_s):
                    self.snake.set_direction(0, 1)
                elif key in (pygame.K_LEFT, pygame.K_a):
                    self.snake.set_direction(-1, 0)
                elif key in (pygame.K_RIGHT, pygame.K_d):
                    self.snake.set_direction(1, 0)
                elif key == pygame.K_p:
                    self.state = GameState.PAUSED
                elif key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
            elif self.state == GameState.PAUSED:
                if key == pygame.K_p:
                    self.state = GameState.RUNNING
                elif key == pygame.K_ESCAPE:
                    self.state = GameState.MENU
            elif self.state == GameState.GAME_OVER:
                if key in (pygame.K_r, pygame.K_RETURN, pygame.K_SPACE):
                    self.reset_game()
                elif key == pygame.K_ESCAPE:
                    self.state = GameState.MENU

    def draw_grid(self):
        for x in range(GRID_WIDTH):
            for y in range(GRID_HEIGHT):
                rect = pygame.Rect(x * CELL_SIZE, WINDOW_MARGIN + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)

    def draw_snake(self):
        for i, (x, y) in enumerate(self.snake.body):
            rect = pygame.Rect(x * CELL_SIZE + 2, WINDOW_MARGIN + y * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            color = SNAKE_HEAD_COLOR if i == 0 else SNAKE_BODY_COLOR
            pygame.draw.rect(self.screen, color, rect, border_radius=5)

    def draw_fruit(self):
        if not self.fruit:
            return
        x, y = self.fruit.position
        rect = pygame.Rect(x * CELL_SIZE + 4, WINDOW_MARGIN + y * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        if self.fruit.type == FruitType.GOLDEN:
            pygame.draw.rect(self.screen, GOLDEN_FRUIT_COLOR, rect, border_radius=6)
            # Draw shrinking lifetime bar
            if self.fruit.lifetime is not None:
                ratio = max(0, self.fruit.lifetime / GOLDEN_FRUIT_TIME)
                bar_width = int((CELL_SIZE - 8) * ratio)
                bar_rect = pygame.Rect(x * CELL_SIZE + 4, WINDOW_MARGIN + y * CELL_SIZE + CELL_SIZE - 6, bar_width, 3)
                pygame.draw.rect(self.screen, (255, 255, 255), bar_rect)
        else:
            pygame.draw.rect(self.screen, FRUIT_COLOR, rect, border_radius=6)

    def text(self, surface, txt, font, x, y, center=False, color=TEXT_COLOR, shadow=True):
        if shadow:
            sh = font.render(txt, True, SHADOW_COLOR)
            rect = sh.get_rect()
            if center:
                rect.center = (x + 2, y + 2)
            else:
                rect.topleft = (x + 2, y + 2)
            surface.blit(sh, rect)
        img = font.render(txt, True, color)
        rect = img.get_rect()
        if center:
            rect.center = (x, y)
        else:
            rect.topleft = (x, y)
        surface.blit(img, rect)

    def draw_hud(self):
        self.text(self.screen, f"Score: {self.score}", self.font, 10, 10)
        self.text(self.screen, f"High: {self.high_score}", self.font, 10, 40)
        self.text(self.screen, f"Speed: {self.speed}", self.font_small, 270, 18)
        wrap_text = "WRAP ON" if self.wrap_walls else "WRAP OFF"
        self.text(self.screen, wrap_text, self.font_small, 270, 42, color=(200,200,120))

    def draw_menu(self):
        self.text(self.screen, "SNAKE", self.font_large, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 140, center=True, color=(0, 255, 200))
        self.text(self.screen, "Press ENTER / SPACE to Start", self.font, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, center=True)
        self.text(self.screen, "Arrow Keys / WASD to Move", self.font_small, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10, center=True)
        self.text(self.screen, "P: Pause | ESC: Menu | R: Restart (Game Over)", self.font_small, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40, center=True)
        self.text(self.screen, "W (here) Toggle Wall Wrap", self.font_small, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70, center=True, color=(200,200,120))
        self.text(self.screen, "Golden Fruit = +5 & Timed", self.font_small, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100, center=True, color=GOLDEN_FRUIT_COLOR)

    def draw_game_over(self):
        self.text(self.screen, "GAME OVER", self.font_large, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80, center=True, color=(255, 80, 80))
        self.text(self.screen, f"Score: {self.score}", self.font, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20, center=True)
        self.text(self.screen, f"High Score: {self.high_score}", self.font_small, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, center=True)
        self.text(self.screen, "Press R / ENTER to Restart", self.font_small, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60, center=True)
        self.text(self.screen, "ESC to Menu", self.font_small, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90, center=True)

    def draw_paused(self):
        self.text(self.screen, "PAUSED", self.font_large, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40, center=True, color=(255, 255, 120))
        self.text(self.screen, "Press P to Resume", self.font_small, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20, center=True)
        self.text(self.screen, "ESC to Menu", self.font_small, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50, center=True)

    def draw(self):
        self.screen.fill(BG_COLOR)
        # Playfield background
        playfield_rect = pygame.Rect(0, WINDOW_MARGIN, SCREEN_WIDTH, SCREEN_HEIGHT - WINDOW_MARGIN)
        pygame.draw.rect(self.screen, (22, 26, 34), playfield_rect)
        self.draw_grid()
        if self.state in (GameState.RUNNING, GameState.PAUSED):
            self.draw_snake()
            self.draw_fruit()
            self.draw_hud()
        if self.state == GameState.MENU:
            self.draw_menu()
        elif self.state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.state == GameState.PAUSED:
            self.draw_paused()
        pygame.display.flip()

    def run(self):
        accumulator = 0.0
        time_step = 1.0 / self.speed
        while True:
            dt_ms = self.clock.tick(60)
            dt = dt_ms / 1000.0
            # Update fixed time step based on dynamic speed
            time_step = 1.0 / self.speed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                self.handle_input(event)
            if self.state == GameState.RUNNING:
                accumulator += dt
                while accumulator >= time_step:
                    self.update(time_step)
                    accumulator -= time_step
            self.draw()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
