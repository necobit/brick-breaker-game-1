import pygame
import random
import math

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

def draw_paddle(x, y, angle=0):
    # Create a paddle surface
    paddle_surface = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
    paddle_surface.fill(BLUE)
    
    # Rotate the surface
    rotated = pygame.transform.rotate(paddle_surface, math.degrees(angle))
    
    # Calculate position to keep center at (x + PADDLE_WIDTH/2, y + PADDLE_HEIGHT/2)
    rect = rotated.get_rect(center=(x + PADDLE_WIDTH//2, y + PADDLE_HEIGHT//2))
    
    # Draw the rotated paddle
    screen.blit(rotated, rect.topleft)

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
        # Initialize paddle angle
        paddle_angle = 0

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
            # 物理法則通りの反射（入射角=反射角）
            normal_x, normal_y = 0, -1
            speed = math.hypot(ball_dx, ball_dy)
            in_dx = ball_dx / speed
            in_dy = ball_dy / speed
            dot = in_dx * normal_x + in_dy * normal_y
            ref_dx = in_dx - 2 * dot * normal_x
            ref_dy = in_dy - 2 * dot * normal_y

            # パドル中心からの相対位置を計算（-1:左端, 0:中心, +1:右端）
            center_x = paddle_x + PADDLE_WIDTH / 2
            offset = (ball_x - center_x) / (PADDLE_WIDTH / 2)
            offset = max(-1, min(1, offset))  # 念のためクリップ

            # 傾き角度（最大±15度）
            max_tilt_deg = 30
            tilt_angle = math.radians(max_tilt_deg) * offset

            # 反射ベクトルを傾き角度分だけ回転
            cos_t = math.cos(tilt_angle)
            sin_t = math.sin(tilt_angle)
            rot_dx = ref_dx * cos_t - ref_dy * sin_t
            rot_dy = ref_dx * sin_t + ref_dy * cos_t

            # デバッグ用ログ
            print(f"[DEBUG] 入射: dx={ball_dx:.2f}, dy={ball_dy:.2f} → 反射: dx={ref_dx*speed:.2f}, dy={ref_dy*speed:.2f} → 傾き補正: dx={rot_dx*speed:.2f}, dy={rot_dy*speed:.2f} (offset={offset:.2f}, tilt={math.degrees(tilt_angle):.2f}度)")

            # 速度を維持して反射ベクトルを適用
            ball_dx = rot_dx * speed
            ball_dy = rot_dy * speed

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
        draw_paddle(paddle_x, paddle_y, paddle_angle)
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
