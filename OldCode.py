import pygame
import sys
import random

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

PADDLE_WIDHT = 10
PADDLE_HEIGHT = 60
PADDLE_SPEED = 5

traces = 0
cor = WHITE

BALL_SIZE = 10
BALL_SPEED = 3

score_a = 0
score_b = 0

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

font_file = "font/PressStart2P-Regular.ttf"
font = pygame.font.Font("font/PressStart2P-Regular.ttf",30)

paddle_a = pygame.Rect(20,SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2,PADDLE_WIDHT, PADDLE_HEIGHT)
paddle_b = pygame.Rect(SCREEN_WIDTH -20 - PADDLE_WIDHT,SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2 ,PADDLE_WIDHT, PADDLE_HEIGHT)

ball = pygame.Rect(SCREEN_WIDTH //2 -BALL_SIZE//2, SCREEN_HEIGHT//2-BALL_SIZE//2,BALL_SIZE,BALL_SIZE)
ball_dx, ball_dy = BALL_SPEED, BALL_SPEED


#running = True

def game_loop():
    global score_a
    global score_b
    global ball_dx
    global ball_dy

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(BLACK)
    pygame.draw.rect(screen,WHITE,paddle_a)
    pygame.draw.rect(screen,WHITE,paddle_b)
    pygame.draw.ellipse(screen,WHITE,ball)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and paddle_a.top > 0:
        paddle_a.y -= PADDLE_SPEED
    if keys[pygame.K_s] and paddle_a.bottom < SCREEN_HEIGHT:
        paddle_a.y += PADDLE_SPEED
    if keys[pygame.K_UP] and paddle_b.top > 0:
        paddle_b.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and paddle_b.bottom < SCREEN_HEIGHT:
        paddle_b.y += PADDLE_SPEED


    ball.x += ball_dx
    ball.y += ball_dy
    direcao = random.randrange(-1, 2, 2)

    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_dx = - ball_dx
    if ball.top <= 0 or ball.bottom >=SCREEN_HEIGHT:
        ball_dy = -ball_dy

    if ball.left <= 0:
        score_b += 1
        ball.x = SCREEN_WIDTH // 2 - BALL_SIZE//2
        ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE//2
        ball_dx = direcao*ball_dx

    if ball.right >= SCREEN_WIDTH:
        score_a += 1
        ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        ball_dx = direcao * ball_dx

    score_text = font.render(f"{score_a}     {score_b}",True,WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2,30))
    screen.blit(score_text,score_rect)

    for i in range(7,SCREEN_HEIGHT,15):
        pygame.draw.line(screen, cor, (SCREEN_WIDTH//2,i),(SCREEN_WIDTH//2,SCREEN_HEIGHT),5)
        if (cor ==WHITE):
            cor = BLACK
        else: cor = WHITE

    pygame.display.flip()

    clock = pygame.time.Clock()
    clock.tick(60)