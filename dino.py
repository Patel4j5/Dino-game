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

    # Game state variables
    game_state = "start"  # Can be "start", "running", or "paused"

    running = True
    while running:
        clock.tick(FPS)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                # Handle starting the game from the start screen
                if game_state == "start":
                    if event.key == pygame.K_SPACE:
                        game_state = "running"  # Start the game

                # Handle pausing the game
                if game_state == "running":
                    if event.key == pygame.K_SPACE:
                        dino.jump()
                    if event.key == pygame.K_p:  # Press 'P' to pause
                        game_state = "paused"

                # Handle resuming the game from pause
                elif game_state == "paused":
                    if event.key == pygame.K_p:  # Press 'P' again to unpause
                        game_state = "running"

        # Start Screen
        if game_state == "start":
            screen.fill(WHITE)
            font = pygame.font.Font(None, 48)
            start_text = font.render("Press SPACE to Start", True, BLACK)
            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2))

        # Paused Screen
        elif game_state == "paused":
            screen.fill(WHITE)
            font = pygame.font.Font(None, 48)
            pause_text = font.render("Paused - Press 'P' to Resume", True, BLACK)
            screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))

        # Running game state
        elif game_state == "running":
            screen.fill(WHITE)

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

            # Display the "Press P to Pause" message
            pause_font = pygame.font.Font(None, 24)  # Smaller font for the pause message
            pause_text = pause_font.render("Press P to Pause", True, BLACK)
            screen.blit(pause_text, (SCREEN_WIDTH - pause_text.get_width() - 10, 10))  # Top-right corner

        # Refresh the display
        pygame.display.flip()

    pygame.quit()

# Start the game
if __name__ == "__main__":
    game()
