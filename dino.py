import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
MAX_JUMPS = 2  # Limit for multiple jumps (e.g., 2 allows double jump)

# Load assets (placeholders for now)
dino_image = pygame.Surface((50, 50))  # Replace with actual dino graphic
dino_image.fill((100, 100, 100))       # Grey box placeholder

obstacle_image = pygame.Surface((30, 60))  # Replace with actual obstacle graphic
obstacle_image.fill((255, 0, 0))           # Red box placeholder

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dinosaur Endless Runner")

# Player (Dinosaur) Class
class Dinosaur:
    def __init__(self):
        self.image = dino_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.vel_y = 0
        self.gravity = 0.8
        self.jumps_remaining = MAX_JUMPS  # Track how many jumps are left

    def jump(self):
        if self.jumps_remaining > 0:
            self.vel_y = -15  # Jump force
            self.jumps_remaining -= 1  # Reduce available jumps

    def update(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Check if the dino is on the ground
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height:
            self.rect.y = SCREEN_HEIGHT - self.rect.height
            self.jumps_remaining = MAX_JUMPS  # Reset jumps when landing

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Obstacle Class
class Obstacle:
    def __init__(self, speed):
        self.image = obstacle_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = SCREEN_HEIGHT - self.rect.height
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:
            self.rect.x = SCREEN_WIDTH + random.randint(100, 300)  # Reset position

    def draw(self, screen):
        screen.blit(self.image, self.rect)

# Game loop
def game():
    clock = pygame.time.Clock()
    dino = Dinosaur()
    obstacles = [Obstacle(10)]  # Start with one obstacle
    score = 0
    game_speed = 10
    difficulty_timer = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                dino.jump()

        # Update the dinosaur and obstacles
        dino.update()
        for obstacle in obstacles:
            obstacle.update()

            # Check for collision
            if dino.rect.colliderect(obstacle.rect):
                print(f"Game Over! Final Score: {score}")
                running = False

        # Draw everything
        dino.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Dynamic difficulty adjustment (increase speed over time)
        difficulty_timer += 1
        if difficulty_timer % 500 == 0:
            game_speed += 1
            for obstacle in obstacles:
                obstacle.speed = game_speed
            # Add new obstacles over time
            if len(obstacles) < 3:
                obstacles.append(Obstacle(game_speed))

        # Update score
        score += 1
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Refresh the display
        pygame.display.flip()

    pygame.quit()

# Start the game
if __name__ == "__main__":
    game()
