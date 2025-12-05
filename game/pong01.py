import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
BALL_SIZE = 10

PADDLE_SPEED = 5
BALL_SPEED_X = 3
BALL_SPEED_Y = 3

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()

left_paddle = pygame.Rect(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)

ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
ball_vel_x = BALL_SPEED_X
ball_vel_y = BALL_SPEED_Y

left_score = 0
right_score = 0

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def draw():
    screen.fill(BLACK)

    for i in range(0, SCREEN_WIDTH, 50):
        pygame.draw.line(screen, (50, 50, 50), (i, 0), (i, SCREEN_HEIGHT), 1)
    for i in range(0, SCREEN_HEIGHT, 50):
        pygame.draw.line(screen, (50, 50, 50), (0, i), (SCREEN_WIDTH, i), 1)

    pygame.draw.rect(screen, BLUE, left_paddle)
    pygame.draw.rect(screen, GREEN, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    left_text = font.render(str(left_score), True, BLUE)
    right_text = font.render(str(right_score), True, GREEN)
    screen.blit(left_text, (SCREEN_WIDTH // 4, 20))
    screen.blit(right_text, (3 * SCREEN_WIDTH // 4, 20))

    left_label = small_font.render("Player 1", True, BLUE)
    right_label = small_font.render("Player 2", True, GREEN)
    screen.blit(left_label, (SCREEN_WIDTH // 4 - 30, 60))
    screen.blit(right_label, (3 * SCREEN_WIDTH // 4 - 30, 60))

    instr_text = small_font.render("ESC to return to menu", True, (128, 128, 128))
    screen.blit(instr_text, (SCREEN_WIDTH // 2 - instr_text.get_width() // 2, SCREEN_HEIGHT - 30))

    pygame.display.flip()

def move_paddles():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < SCREEN_HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < SCREEN_HEIGHT:
        right_paddle.y += PADDLE_SPEED

def move_ball():
    global ball_vel_x, ball_vel_y, left_score, right_score

    ball.x += ball_vel_x
    ball.y += ball_vel_y

    if ball.top <= 0 or ball.bottom >= SCREEN_HEIGHT:
        ball_vel_y = -ball_vel_y

    if ball.colliderect(left_paddle):
        ball_vel_x = abs(ball_vel_x)
        relative_intersect_y = (left_paddle.centery - ball.centery) / (PADDLE_HEIGHT / 2)
        ball_vel_y = -BALL_SPEED_Y * relative_intersect_y

    if ball.colliderect(right_paddle):
        ball_vel_x = -abs(ball_vel_x)
        relative_intersect_y = (right_paddle.centery - ball.centery) / (PADDLE_HEIGHT / 2)
        ball_vel_y = -BALL_SPEED_Y * relative_intersect_y

    if ball.left <= 0:
        right_score += 1
        reset_ball()
    if ball.right >= SCREEN_WIDTH:
        left_score += 1
        reset_ball()

def reset_ball():
    ball.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_vel_x = random.choice([-BALL_SPEED_X, BALL_SPEED_X])
    ball_vel_y = random.choice([-BALL_SPEED_Y, BALL_SPEED_Y])

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        move_paddles()
        move_ball()
        draw()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
    sys.exit()