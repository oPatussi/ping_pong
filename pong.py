import random
from pygame import mixer
import pygame
import sys

# (O código de inicialização e variáveis globais permanecem o mesmo)

WHITE = (255,255,255)
BLACK = (0,0,0)

#Prepara o ambiente para receber comandos do PyGame
pygame.init()
#Inicializa o módulo responsável pelo processamento de áudio
mixer.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
cor = WHITE

#Inicialização das variáveis
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
PADDLE_WIDTH = 10
PADDLE_HEIGHT = 60
PADDLE_SPEED = 5
BALL_SIZE = 10
BALL_SPEED = 2

traces = 0
score_a = 0
score_b = 0
total_score = 0
var_score = 0
max_score = 10

mixer.music.load('sounds/som_musica_fundo.mp3')
collision_souds = mixer.Sound("sounds/som_colisao.mp3")
point_sound = mixer.Sound("sounds/som_ponto.mp3")

mixer.music.set_volume(0)
mixer.Sound.set_volume(collision_souds,0)
mixer.Sound.set_volume(point_sound,0)

#Faz o som "setado" como music em loop contínuo
mixer.music.play(-1)

screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))#Cria os parâmetros janela do jogo
pygame.display.set_caption("Pong")#Da título à janela do jogo

font_file = "font/PressStart2P-Regular.ttf"
font = pygame.font.Font("font/PressStart2P-Regular.ttf",30)

#Cria os parâmetros das raquetes A e B, e da bola
paddle_a = pygame.Rect(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
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
        title_font = pygame.font.Font(font_file,36) #Configuração da fonte
        title_text = title_font.render("Pong", True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//4))

        # Nome
        title_font2 = pygame.font.Font(font_file, 10)
        title_text2 = title_font2.render("Otávio Patussi", True, WHITE)
        title_rect2 = title_text2.get_rect(center=(SCREEN_WIDTH-80,SCREEN_HEIGHT - 30))

        # Insta
        title_text3 = title_font2.render("@opatussi", True, WHITE)
        title_rect3 = title_text3.get_rect(center=(SCREEN_WIDTH-55,SCREEN_HEIGHT - 15))

        #O "blit" copia o "title_text" e copia ele no "title_rect", respeitando as coordenadas
        screen.blit(title_text, title_rect)
        screen.blit(title_text2,title_rect2)
        screen.blit(title_text3,title_rect3)

        title_font = pygame.font.Font(font_file,16)
        concurrent_time = pygame.time.get_ticks() #Pega o tempo decorrido do jogo em milissegundos

        #Cria o texto do "title_text" no menu, e fazendo com que pisque a cada 1 segundo
        if concurrent_time % 2000 < 1000:
            title_text1 = title_font.render("Pressione espaço para iniciar", True, WHITE)
            title_rect1 = title_text1.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4+60))
            screen.blit(title_text1,title_rect1)

        # Desenhe o título e as instruções aqui
        pygame.display.flip()


def game_loop():
    #inicializa as variáveis dentro do método
    global score_a, score_b, ball_dx,ball_dy,BALL_SPEED,total_score, var_score, cor


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        #Desenha a tela
        screen.fill(BLACK)
        pygame.draw.rect(screen,WHITE,paddle_a)
        pygame.draw.rect(screen,WHITE,paddle_b)
        pygame.draw.ellipse(screen,WHITE,ball)

        #Inicializa e "seta" uma palavra chave para detectar quando teclas são pressionadas
        keys = pygame.key.get_pressed()
        #movimento da vertical raquete A
        if keys[pygame.K_w] and paddle_a.top > 0:
            paddle_a.y -= PADDLE_SPEED
        if keys[pygame.K_s] and paddle_a.bottom < SCREEN_HEIGHT:
            paddle_a.y += PADDLE_SPEED

        # movimento da horizontal raquete A
        if keys[pygame.K_a] and paddle_a.left > 20:
            paddle_a.x -= PADDLE_SPEED
        if keys[pygame.K_d] and paddle_a.left < SCREEN_WIDTH//2 -70:
            paddle_a.x += PADDLE_SPEED

        #movimento da vertical raquete B
        if keys[pygame.K_UP] and paddle_b.top > 0:
            paddle_b.y -= PADDLE_SPEED
        if keys[pygame.K_DOWN] and paddle_b.bottom < SCREEN_HEIGHT:
            paddle_b.y += PADDLE_SPEED

        # movimento da horizontal raquete B
        if keys[pygame.K_LEFT] and paddle_b.left > SCREEN_WIDTH//2 +70:
            paddle_b.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle_b.left < SCREEN_WIDTH -20:
            paddle_b.x += PADDLE_SPEED

        #Gera uma direção aleatória para a bola iniciar a cada rodada
        numero_aleatorio = random.random()
        if numero_aleatorio < 0.5:
            numero_aleatorio = -1
        else:
            numero_aleatorio = 1

        #Movimento da bola
        ball.x += ball_dx
        ball.y += ball_dy
        direcao = numero_aleatorio

        #Colisão da bola com a raquete A
        if ball.colliderect(paddle_a):
            ball.left = paddle_a.right
            ball_dx = - ball_dx
            collision_souds.play()
        elif ball.colliderect(paddle_a):
            ball.right = paddle_a.left
            ball_dx = - ball_dx
            collision_souds.play()
        elif ball.colliderect(paddle_a):
            ball.top = paddle_a.bottom
            ball_dy = - ball_dy
            collision_souds.play()
        elif ball.colliderect(paddle_a):
            ball.bottom = paddle_a.top
            ball_dy = - ball_dy
            collision_souds.play()

        # Colisão da bola com a raquete A
        if ball.colliderect(paddle_b):
            ball.right = paddle_b.left
            ball_dx = - ball_dx
            collision_souds.play()
        elif ball.colliderect(paddle_b):
            ball.left = paddle_b.right
            ball_dx = - ball_dx
            collision_souds.play()
        elif ball.colliderect(paddle_b):
            ball.top = paddle_b.bottom
            ball_dy = - ball_dy
            collision_souds.play()
        elif ball.colliderect(paddle_b):
            ball.bottom = paddle_b.top
            ball_dy = - ball_dy
            collision_souds.play()

        #bola bate nas extremidades de cima e de baixo e retorna
        if ball.top <= 0 or ball.bottom >=SCREEN_HEIGHT:
            ball_dy = -ball_dy
            collision_souds.play()

        #bola passa pela extremidade esquerda e jogador B pontua
        if ball.left <= 0:
            total_score +=1
            score_b += 1
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE//2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE//2
            ball_dx = direcao*ball_dx
            point_sound.play()

        # bola passa pela extremidade direita e jogador A pontua
        if ball.right >= SCREEN_WIDTH:
            total_score += 1
            score_a += 1
            ball.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
            ball.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
            ball_dx = direcao * ball_dx
            point_sound.play()

        #texto da pontuação
        score_text = font.render(f"{score_a}     {score_b}",True,WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2,30))
        screen.blit(score_text,score_rect)

        #Desenha a linha pontilhada no meio da tela
        for i in range(7,SCREEN_HEIGHT,15):
            pygame.draw.line(screen, cor, (SCREEN_WIDTH//2,i),(SCREEN_WIDTH//2,SCREEN_HEIGHT),5)
            if (cor ==WHITE):
                cor = BLACK
            else: cor = WHITE

        #Atualiza o display da tela
        pygame.display.flip()

        #Controla o FPS
        clock = pygame.time.Clock()
        clock.tick(60)

        #A cada ponto, a velocidade da bola aumenta em 20%
        if total_score > var_score:
            ball_dy += ball_dy / 10
            ball_dx += ball_dx / 10
            var_score +=1

        if (score_a >= max_score):
            end_game("A")
        elif (score_b >= max_score):
            end_game("B")

def end_game(winner):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    reset_game()
                    game_loop()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Renderização da tela de fim de jogo
        screen.fill(BLACK)
        # Desenhe o texto de vitória e instruções aqui
        title_font = pygame.font.Font(font_file, 20)
        title_text4 = title_font.render("Jogador "+winner+" ganhou !!!", True, WHITE) # Verifica qual jogador e escreve na tela
        title_rect4 = title_text4.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 60))
        screen.blit(title_text4, title_rect4)
        pygame.display.flip()

def reset_game():
    global paddle_a, paddle_b, ball, ball_dx, ball_dy, score_a, score_b

    #retorna os valores e coordenadas iniciais
    paddle_a = pygame.Rect(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
    paddle_b = pygame.Rect(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH,
                           PADDLE_HEIGHT)
    ball = pygame.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
    ball_dx, ball_dy = BALL_SPEED, BALL_SPEED
    score_a, score_b = 0, 0


# Inicie a FSM no estado do menu principal
main_menu()