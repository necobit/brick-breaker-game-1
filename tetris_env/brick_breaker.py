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
YELLOW = (255, 255, 128)
BLACK = (0, 0, 0)
GRAY = (120, 120, 120)
BLOCK_SHADOW = (80, 80, 80)
BLOCK_HIGHLIGHT = (200, 255, 200)
BALL_HIGHLIGHT = (255, 255, 255)
BALL_SHADOW = (180, 180, 180)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 120, 20
paddle_x = (WIDTH - PADDLE_WIDTH) // 2
paddle_y = HEIGHT - PADDLE_HEIGHT - 10

# Ball settings
ball_radius = 10

# Brick settings
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 20
BRICK_TOP_OFFSET = 50  # スコア表示分のオフセット
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = col * BRICK_WIDTH
        brick_y = BRICK_TOP_OFFSET + row * BRICK_HEIGHT
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Score
score = 0
lives = 5
font = pygame.font.SysFont(None, 36)

# --- ゲーム状態管理変数 ---
waiting_for_space = True  # Trueならスペース待ち（スタート/リトライ）

# --- ボール初期化ロジック ---
def reset_ball():
    global ball_x, ball_y, ball_dx, ball_dy
    ball_x, ball_y = WIDTH // 2, HEIGHT // 2
    speed = 7
    angle_deg = random.uniform(-135, -45)  # -90±45度（上向き左右）
    angle_rad = math.radians(angle_deg)
    ball_dx = speed * math.cos(angle_rad)
    ball_dy = speed * math.sin(angle_rad)

reset_ball()

# --- 描画関数 ---
def draw_paddle(x, y, angle=0):
    # パドルも立体感を意識してグラデーション風に
    paddle_surface = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT), pygame.SRCALPHA)
    for i in range(PADDLE_HEIGHT):
        shade = 180 + int(60 * (i / PADDLE_HEIGHT))
        color = (shade, shade, 255, 255)
        pygame.draw.line(paddle_surface, color, (0, i), (PADDLE_WIDTH, i))
    rotated = pygame.transform.rotate(paddle_surface, math.degrees(angle))
    rect = rotated.get_rect(center=(x + PADDLE_WIDTH//2, y + PADDLE_HEIGHT//2))
    screen.blit(rotated, rect.topleft)

def draw_ball(x, y):
    # 立体感のある球体を描画
    # ベース
    pygame.draw.circle(screen, RED, (x, y), ball_radius)
    # シャドウ（中心を少しだけ右下、半径も小さめに調整、はみ出さないように）
    pygame.draw.circle(screen, BALL_SHADOW, (x+2, y+2), ball_radius-4)
    # ハイライト
    pygame.draw.circle(screen, BALL_HIGHLIGHT, (x-3, y-3), ball_radius//3)

def draw_bricks(bricks):
    for brick in bricks:
        # メインブロック
        pygame.draw.rect(screen, GREEN, brick)
        # 上部ハイライト
        highlight_rect = pygame.Rect(brick.left+2, brick.top+2, brick.width-4, 5)
        pygame.draw.rect(screen, BLOCK_HIGHLIGHT, highlight_rect)
        # 下部シャドウ
        shadow_rect = pygame.Rect(brick.left+2, brick.bottom-7, brick.width-4, 5)
        pygame.draw.rect(screen, BLOCK_SHADOW, shadow_rect)
        # 境界線
        pygame.draw.rect(screen, BLACK, brick, 2)

def display_score(score, lives):
    # 黒文字＆スコア背景に白帯を追加して視認性UP
    bg_rect = pygame.Rect(5, 5, 260, 38)
    pygame.draw.rect(screen, WHITE, bg_rect, border_radius=8)
    pygame.draw.rect(screen, GRAY, bg_rect, 2, border_radius=8)
    text = font.render(f"Score: {score}  Lives: {lives}", True, BLACK)
    screen.blit(text, (15, 10))

def display_press_space():
    font2 = pygame.font.SysFont(None, 36)
    text2 = font2.render("Press SPACE to Start", True, RED)
    # 位置を画面中央より下に調整
    screen.blit(text2, (WIDTH//2 - 140, HEIGHT//2 + 80))

# Main game loop
running = True
game_over = False
clock = pygame.time.Clock()

while running:
    screen.fill(YELLOW)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if not game_over:
        # --- スペース待ち状態 ---
        if waiting_for_space:
            draw_paddle(paddle_x, paddle_y, 0)
            draw_ball(ball_x, ball_y)
            draw_bricks(bricks)
            display_score(score, lives)
            display_press_space()
            pygame.display.flip()
            clock.tick(60)
            if keys[pygame.K_SPACE]:
                waiting_for_space = False
            continue

        # Initialize paddle angle
        paddle_angle = 0

        # Paddle movement
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

            # 傾き角度（最大±30度）
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

        # 残機ロジック
        if ball_y + ball_radius > HEIGHT:
            lives -= 1
            if lives > 0:
                # リトライ: ボール・パドルのみリセット
                paddle_x = (WIDTH - PADDLE_WIDTH) // 2
                paddle_y = HEIGHT - PADDLE_HEIGHT - 10
                reset_ball()
                waiting_for_space = True
            else:
                game_over = True
        if not bricks:
            game_over = True

        # Draw everything
        draw_paddle(paddle_x, paddle_y, paddle_angle)
        draw_ball(ball_x, ball_y)
        draw_bricks(bricks)
        display_score(score, lives)
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
        if keys[pygame.K_r]:
            # Reset game
            paddle_x = (WIDTH - PADDLE_WIDTH) // 2
            paddle_y = HEIGHT - PADDLE_HEIGHT - 10
            bricks = []
            for row in range(BRICK_ROWS):
                for col in range(BRICK_COLS):
                    brick_x = col * BRICK_WIDTH
                    brick_y = BRICK_TOP_OFFSET + row * BRICK_HEIGHT
                    bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))
            score = 0
            lives = 5
            reset_ball()
            game_over = False
            waiting_for_space = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
