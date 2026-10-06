import math
import random
import pygame

from game.basket import Basket
from game.fruit import Fruit


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.5, 4.5)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed - 1.5

        self.life = random.randint(20, 35)
        self.max_life = self.life

        self.size = random.randint(2, 5)
        self.color = color

    def update(self):
        self.x += self.vx
        self.y += self.vy

        # Gravity
        self.vy += 0.15

        self.life -= 1

    def render(self, surface):
        if self.life <= 0:
            return

        # Particle gradually becomes smaller
        size = max(
            1,
            int(self.size * (self.life / self.max_life))
        )

        pygame.draw.circle(
            surface,
            self.color,
            (int(self.x), int(self.y)),
            size
        )

    def is_dead(self):
        return self.life <= 0


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.basket = Basket(width, height)

        self.fruits = []
        self.particles = []

        self.score = 0
        self.lives = 3

        # Initial spawn delay
        self.spawn_delay = 750

        self.last_spawn_time = pygame.time.get_ticks()

        self.game_state = "PLAYING"

        self.font_big = pygame.font.SysFont(None, 48)
        self.font_medium = pygame.font.SysFont(None, 28)

    def handle_event(self, event):
        if self.game_state == "GAME_OVER":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()

    def create_splash(self, x, y, color):
        """
        Create a small burst of particles.
        """
        for _ in range(12):
            self.particles.append(
                Particle(x, y, color)
            )

    def update_difficulty(self):
        """
        Increase difficulty as score increases.

        Higher score:
        - decreases spawn delay
        - increases falling speed of newly spawned fruits
        """

        difficulty_level = self.score // 5

        # Spawn faster as score increases.
        # Never go below 300 milliseconds.
        self.spawn_delay = max(
            300,
            750 - difficulty_level * 50
        )

    def update(self):
        if self.game_state != "PLAYING":
            return

        # -------------------------
        # Basket movement
        # -------------------------

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.basket.move_left()

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.basket.move_right()

        # -------------------------
        # Difficulty
        # -------------------------

        self.update_difficulty()

        # Speed bonus increases with score
        speed_bonus = min(
            5.0,
            self.score * 0.08
        )

        # -------------------------
        # Spawn fruits
        # -------------------------

        now = pygame.time.get_ticks()

        if now - self.last_spawn_time >= self.spawn_delay:

            self.fruits.append(
                Fruit(
                    self.width,
                    speed_bonus
                )
            )

            self.last_spawn_time = now

        # -------------------------
        # Update particles
        # -------------------------

        for particle in self.particles[:]:

            particle.update()

            if particle.is_dead():
                self.particles.remove(particle)

        # -------------------------
        # Fruit collision / misses
        # -------------------------

        basket_rect = self.basket.rect

        for fruit in self.fruits[:]:

            fruit.update()

            # -------------------------
            # Basket collision
            # -------------------------

            if basket_rect.colliderect(fruit.rect):

                # Hazard caught
                if fruit.is_hazard:

                    self.lives -= 1

                    # Red splash for hazard
                    self.create_splash(
                        fruit.x,
                        fruit.y,
                        (220, 60, 60)
                    )

                # Normal fruit caught
                else:

                    self.score += 1

                    # Fruit-colored splash
                    self.create_splash(
                        fruit.x,
                        fruit.y,
                        fruit.color
                    )

                self.fruits.remove(fruit)

                # Check Game Over
                if self.lives <= 0:
                    self.lives = 0
                    self.game_state = "GAME_OVER"

                continue

            # -------------------------
            # Fruit reaches the ground
            # -------------------------

            if fruit.is_missed(self.height):

                # Only normal fruits penalize the player
                # when they are missed.
                if not fruit.is_hazard:

                    self.lives -= 1

                    # Ground splash
                    self.create_splash(
                        fruit.x,
                        self.height - 25,
                        fruit.color
                    )

                else:

                    # A missed bomb causes no penalty.
                    self.create_splash(
                        fruit.x,
                        self.height - 25,
                        (80, 80, 80)
                    )

                self.fruits.remove(fruit)

                # Check Game Over
                if self.lives <= 0:
                    self.lives = 0
                    self.game_state = "GAME_OVER"

        # -------------------------
        # Keep game stopped after
        # Game Over
        # -------------------------

        if self.lives <= 0:
            self.lives = 0
            self.game_state = "GAME_OVER"

    def reset(self):
        self.basket = Basket(
            self.width,
            self.height
        )

        self.fruits.clear()
        self.particles.clear()

        self.score = 0
        self.lives = 3

        self.spawn_delay = 750

        self.last_spawn_time = pygame.time.get_ticks()

        self.game_state = "PLAYING"

    def render(self, screen):

        # -------------------------
        # Background
        # -------------------------

        screen.fill(
            (28, 32, 40)
        )

        # -------------------------
        # Ground
        # -------------------------

        ground_y = self.height - 25

        pygame.draw.rect(
            screen,
            (45, 50, 60),
            (0, ground_y, self.width, 25)
        )

        # -------------------------
        # Basket
        # -------------------------

        self.basket.render(screen)

        # -------------------------
        # Fruits
        # -------------------------

        for fruit in self.fruits:
            fruit.render(screen)

        # -------------------------
        # Particles
        # -------------------------

        for particle in self.particles:
            particle.render(screen)

        # -------------------------
        # Score
        # -------------------------

        score_surf = self.font_medium.render(
            f"Score: {self.score}",
            True,
            (255, 220, 80)
        )

        screen.blit(
            score_surf,
            (25, 20)
        )

        # -------------------------
        # Lives
        # -------------------------

        lives_surf = self.font_medium.render(
            f"Lives: {self.lives}",
            True,
            (240, 80, 80)
        )

        screen.blit(
            lives_surf,
            (
                self.width - lives_surf.get_width() - 25,
                20
            )
        )

        # -------------------------
        # Game Over
        # -------------------------

        if self.game_state == "GAME_OVER":

            overlay = pygame.Surface(
                (self.width, self.height),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 190)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            over_surf = self.font_big.render(
                "GAME OVER",
                True,
                (235, 70, 70)
            )

            screen.blit(
                over_surf,
                (
                    self.width // 2
                    - over_surf.get_width() // 2,
                    self.height // 2 - 40
                )
            )

            final_surf = self.font_medium.render(
                f"Final Score: {self.score}",
                True,
                (255, 255, 255)
            )

            screen.blit(
                final_surf,
                (
                    self.width // 2
                    - final_surf.get_width() // 2,
                    self.height // 2 + 10
                )
            )

            restart_surf = self.font_medium.render(
                "Press [R] to Play Again",
                True,
                (200, 200, 200)
            )

            screen.blit(
                restart_surf,
                (
                    self.width // 2
                    - restart_surf.get_width() // 2,
                    self.height // 2 + 50
                )
            )