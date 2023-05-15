import random
from pygame import mixer
import pygame
import sys

# (O código de inicialização e variáveis globais permanecem o mesmo)

WHITE = (255,255,255)
BLACK = (0,0,0)

pygame.init()
mixer.init()

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

mixer.music.load('sounds/TrepadaEmCuiaba.mp3')
mixer.music.set_volume(0.8)
collision_souds = mixer.Sound("sounds/rojao-super-estourado.mp3")
point_sound = mixer.Sound("sounds/owwn-ze-da-manga.mp3")

mixer.music.play(-1)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

font_file = "font/PressStart2P-Regular.ttf"
font = pygame.font.Font("font/PressStart2P-Regular.ttf",30)

paddle_a = pygame.Rect(20,SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2,PADDLE_WIDHT, PADDLE_HEIGHT)
paddle_b = pygame.Rect(SCREEN_WIDTH -20 - PADDLE_WIDHT,SCREEN_HEIGHT//2 - PADDLE_HEIGHT//2 ,PADDLE_WIDHT, PADDLE_HEIGHT)

ball = pygame.Rect(SCREEN_WIDTH //2 -BALL_SIZE//2, SCREEN_HEIGHT//2-BALL_SIZE//2,BALL_SIZE,BALL_SIZE)
ball_dx, ball_dy = BALL_SPEED, BALL_SPEED

# Funções de estado
def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Renderização do menu principal
        screen.fill(BLACK)
        title_font = pygame.font.Font(font_file,36)
        title_text = title_font.render("Pong", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//4))

        # Nome
        title_font2 = pygame.font.Font(font_file, 10)
        title_text2 = title_font2.render("Otávio Patussi", True, WHITE)
        title_rect2 = title_text2.get_rect(center=(SCREEN_WIDTH-80,SCREEN_HEIGHT - 30))

        # Insta
        title_text3 = title_font2.render("@opatussi", True, WHITE)
        title_rect3 = title_text3.get_rect(center=(SCREEN_WIDTH-55,SCREEN_HEIGHT - 15))

        screen.blit(title_text, title_rect)
        screen.blit(title_text2,title_rect2)
        screen.blit(title_text3,title_rect3)

        title_font = pygame.font.Font(font_file,16)
        concurrent_time = pygame.time.get_ticks()

        if concurrent_time % 2000 < 1000:
            title_text1 = title_font.render("Pressione espaço para iniciar", True, WHITE)
            title_rect1 = title_text1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4+60))
            screen.blit(title_text1,title_rect1)

        # Desenhe o título e as instruções aqui
        pygame.display.flip()


def game_loop():
    global score_a
    global score_b
    global ball_dx
    global ball_dy
    global cor

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return


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

        numero_aleatorio = random.random()
        if numero_aleatorio < 0.5:
            numero_aleatorio = -1
        else:
            numero_aleatorio = 1

        ball.x += ball_dx
        ball.y += ball_dy
        direcao = numero_aleatorio

        if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
            ball_dx = - ball_dx
            collision_souds.play()
        if ball.top <= 0 or ball.bottom >=SCREEN_HEIGHT:
            ball_dy = -ball_dy
            collision_souds.play()

        if ball.left <= 0:
            score_b += 1
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE//2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE//2
            ball_dx = direcao*ball_dx
            point_sound.play()

        if ball.right >= SCREEN_WIDTH:
            score_a += 1
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
            ball_dx = direcao * ball_dx
            point_sound.play()

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

def end_game(winner):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Renderização da tela de fim de jogo
        screen.fill(BLACK)
        # Desenhe o texto de vitória e instruções aqui
        pygame.display.flip()

def reset_game():
    global paddle_a, paddle_b, ball, ball_dx, ball_dy, score_a, score_b



# Inicie a FSM no estado do menu principal
main_menu()