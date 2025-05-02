import pygame
import random

#QWEN3をClineで実行するテスト

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ブロック崩しゲーム")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10

# Ball settings
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_radius = 10
ball_dx, ball_dy = 5, -5

# Brick settings
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 20
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = col * BRICK_WIDTH
        brick_y = row * BRICK_HEIGHT
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Score
score = 0
font = pygame.font.SysFont(None, 36)

def draw_paddle(x, y):
    pygame.draw.rect(screen, BLUE, (x, y, PADDLE_WIDTH, PADDLE_HEIGHT))

def draw_ball(x, y):
    pygame.draw.circle(screen, RED, (x, y), ball_radius)

def draw_bricks(bricks):
    for brick in bricks:
        pygame.draw.rect(screen, GREEN, brick)

def display_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

# Main game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= 10
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - PADDLE_WIDTH:
            paddle_x += 10

        # Ball movement
        ball_x += ball_dx
        ball_y += ball_dy

        # Collision with walls
        if ball_x - ball_radius < 0 or ball_x + ball_radius > WIDTH:
            ball_dx *= -1
        if ball_y - ball_radius < 0:
            ball_dy *= -1

        # Collision with paddle
        if (paddle_x < ball_x < paddle_x + PADDLE_WIDTH and
            paddle_y < ball_y + ball_radius < paddle_y + PADDLE_HEIGHT):
            # Calculate offset from center
            center_x = paddle_x + PADDLE_WIDTH / 2
            offset = ball_x - center_x
            max_offset = PADDLE_WIDTH / 2
            normalized_offset = offset / max_offset  # -1 to 1
            
            # Calculate reflection angle based on hit position
            ball_dx = normalized_offset * 5  # Adjust multiplier for desired speed
            ball_dy *= -1
            
            # Maintain incident angle reflection
            if abs(normalized_offset) < 0.1:
                ball_dx = 0

        # Collision with bricks
        for brick in bricks[:]:
            if brick.collidepoint(ball_x, ball_y):
                bricks.remove(brick)
                ball_dy *= -1
                score += 10
                break

        # Check game over conditions
        if ball_y + ball_radius > HEIGHT:
            game_over = True
        if not bricks:
            game_over = True

        # Draw everything
        draw_paddle(paddle_x, paddle_y)
        draw_ball(ball_x, ball_y)
        draw_bricks(bricks)
        display_score(score)
    else:
        # Draw game over screen
        font = pygame.font.SysFont(None, 48)
        text = font.render("Game Over!", True, RED)
        screen.blit(text, (WIDTH//2 - 100, HEIGHT//2 - 50))
        
        # Draw press R instruction
        font = pygame.font.SysFont(None, 36)
        text = font.render("Press R", True, RED)
        screen.blit(text, (WIDTH//2 - 50, HEIGHT//2 + 25))
        
        # Check for retry with R key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game
            paddle_x = (WIDTH - PADDLE_WIDTH) // 2
            paddle_y = HEIGHT - PADDLE_HEIGHT - 10
            ball_x, ball_y = WIDTH // 2, HEIGHT // 2
            ball_dx, ball_dy = 5, -5
            bricks = []
            for row in range(BRICK_ROWS):
                for col in range(BRICK_COLS):
                    brick_x = col * BRICK_WIDTH
                    brick_y = row * BRICK_HEIGHT
                    bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))
            score = 0
            game_over = False


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
