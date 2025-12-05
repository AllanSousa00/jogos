import pygame
import sys
import random
import math

pygame.init()

LARGURA = 1000
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Street Fight")

PRETO = (25, 30, 35)
BRANCO = (255, 255, 255)
VERMELHO = (230, 70, 70)
VERDE = (70, 190, 110)
AZUL = (80, 140, 210)
AMARELO = (255, 210, 70)
LARANJA = (245, 160, 80)
MARROM = (160, 110, 70)
VERDE_ESCURO = (50, 110, 70)
AZUL_CEU = (140, 200, 240)
CINZA_CLARO = (190, 190, 200)

LARGURA_P = 75
ALTURA_P = 135

VELOCIDADE = 6
PULO = 16
GRAVIDADE = 0.8
FORCA_SOCO = 20
FORCA_CHUTE = 25

relogio = pygame.time.Clock()
fonte_grande = pygame.font.Font(None, 52)
fonte = pygame.font.Font(None, 34)
fonte_pequena = pygame.font.Font(None, 24)

class Lutador:
    def __init__(self, x, y, cor_principal, cor_secundaria, controles, nome):
        self.rect = pygame.Rect(x, y, LARGURA_P, ALTURA_P)
        self.cor_principal = cor_principal
        self.cor_secundaria = cor_secundaria
        self.vel_y = 0
        self.no_chao = True
        self.vida = 100
        self.controles = controles
        self.socando = False
        self.chutando = False
        self.defendendo = False
        self.tempo_ataque = 0
        self.direita = True if controles["esquerda"] == pygame.K_a else False
        self.nome = nome
        self.animacao = 0

    def mover(self, outro):
        teclas = pygame.key.get_pressed()
        self.defendendo = False

        if teclas[self.controles["defesa"]]:
            self.defendendo = True
            velocidade_atual = VELOCIDADE // 2
        else:
            velocidade_atual = VELOCIDADE

        if teclas[self.controles["esquerda"]] and self.rect.left > 0:
            self.rect.x -= velocidade_atual
            self.direita = False
            self.animacao = (self.animacao + 1) % 30
        if teclas[self.controles["direita"]] and self.rect.right < LARGURA:
            self.rect.x += velocidade_atual
            self.direita = True
            self.animacao = (self.animacao + 1) % 30

        if teclas[self.controles["pulo"]] and self.no_chao:
            self.vel_y = -PULO
            self.no_chao = False

        if teclas[self.controles["soco"]] and not self.socando and not self.chutando:
            self.socando = True
            self.tempo_ataque = 12

        if teclas[self.controles["chute"]] and not self.chutando and not self.socando:
            self.chutando = True
            self.tempo_ataque = 15

        self.vel_y += GRAVIDADE
        self.rect.y += self.vel_y

        if self.rect.bottom >= ALTURA - 70:
            self.rect.bottom = ALTURA - 70
            self.vel_y = 0
            self.no_chao = True

        if self.socando or self.chutando:
            self.tempo_ataque -= 1
            if self.tempo_ataque <= 0:
                self.socando = False
                self.chutando = False

        if (self.socando or self.chutando) and self.rect.colliderect(outro.rect):
            dano = 8 if self.socando else 12
            forca = FORCA_SOCO if self.socando else FORCA_CHUTE
            
            if self.defendendo:
                dano = dano // 2
                forca = forca // 2
            
            if not outro.defendendo:
                outro.vida = max(0, outro.vida - dano)
                
                if self.direita and self.rect.centerx < outro.rect.centerx:
                    outro.rect.x += forca
                elif not self.direita and self.rect.centerx > outro.rect.centerx:
                    outro.rect.x -= forca

    def desenhar(self):
        offset_y = 0
        if not self.no_chao:
            offset_y = -10
        elif self.animacao > 0:
            offset_y = math.sin(self.animacao * 0.2) * 3

        corpo_rect = pygame.Rect(
            self.rect.centerx - 24, 
            self.rect.y + 30 + offset_y, 
            48, 
            75
        )
        pygame.draw.ellipse(tela, self.cor_principal, corpo_rect)
        pygame.draw.ellipse(tela, self.cor_secundaria, corpo_rect, 3)

        cinto_rect = pygame.Rect(
            self.rect.centerx - 26, 
            self.rect.y + 90 + offset_y, 
            52, 
            10
        )
        pygame.draw.rect(tela, MARROM, cinto_rect)
        pygame.draw.rect(tela, (120, 80, 50), cinto_rect, 2)

        cabeca_rect = pygame.Rect(
            self.rect.centerx - 20, 
            self.rect.y + 8 + offset_y, 
            40, 
            36
        )
        pygame.draw.ellipse(tela, (245, 215, 180), cabeca_rect)
        pygame.draw.ellipse(tela, (205, 175, 140), cabeca_rect, 2)

        cor_cabelo = (45, 35, 25) if self.cor_principal == AZUL else (170, 110, 60)
        cabelo_rect = pygame.Rect(
            self.rect.centerx - 22, 
            self.rect.y + 2 + offset_y, 
            44, 
            22
        )
        pygame.draw.ellipse(tela, cor_cabelo, cabelo_rect)
        
        for i in range(4):
            x_pos = self.rect.centerx - 15 + i * 10
            pygame.draw.ellipse(tela, cor_cabelo, (x_pos, self.rect.y + 6 + offset_y, 8, 12))

        olho_y = self.rect.y + 22 + offset_y
        if self.socando or self.chutando:
            if self.direita:
                pygame.draw.line(tela, (75, 55, 35), (self.rect.centerx - 7, olho_y), (self.rect.centerx + 3, olho_y), 3)
                pygame.draw.line(tela, (75, 55, 35), (self.rect.centerx + 7, olho_y), (self.rect.centerx + 17, olho_y), 3)
            else:
                pygame.draw.line(tela, (75, 55, 35), (self.rect.centerx - 17, olho_y), (self.rect.centerx - 7, olho_y), 3)
                pygame.draw.line(tela, (75, 55, 35), (self.rect.centerx - 3, olho_y), (self.rect.centerx + 7, olho_y), 3)
        else:
            if self.direita:
                pygame.draw.ellipse(tela, BRANCO, (self.rect.centerx - 9, olho_y - 3, 12, 10))
                pygame.draw.ellipse(tela, BRANCO, (self.rect.centerx + 7, olho_y - 3, 12, 10))
                pygame.draw.ellipse(tela, (70, 110, 190), (self.rect.centerx - 5, olho_y, 8, 7))
                pygame.draw.ellipse(tela, (70, 110, 190), (self.rect.centerx + 11, olho_y, 8, 7))
                pygame.draw.circle(tela, PRETO, (self.rect.centerx - 2, olho_y + 3), 2)
                pygame.draw.circle(tela, PRETO, (self.rect.centerx + 14, olho_y + 3), 2)
                pygame.draw.circle(tela, BRANCO, (self.rect.centerx - 4, olho_y + 1), 1)
                pygame.draw.circle(tela, BRANCO, (self.rect.centerx + 12, olho_y + 1), 1)
            else:
                pygame.draw.ellipse(tela, BRANCO, (self.rect.centerx - 13, olho_y - 3, 12, 10))
                pygame.draw.ellipse(tela, BRANCO, (self.rect.centerx + 3, olho_y - 3, 12, 10))
                pygame.draw.ellipse(tela, (190, 90, 90), (self.rect.centerx - 9, olho_y, 8, 7))
                pygame.draw.ellipse(tela, (190, 90, 90), (self.rect.centerx + 7, olho_y, 8, 7))
                pygame.draw.circle(tela, PRETO, (self.rect.centerx - 6, olho_y + 3), 2)
                pygame.draw.circle(tela, PRETO, (self.rect.centerx + 10, olho_y + 3), 2)
                pygame.draw.circle(tela, BRANCO, (self.rect.centerx - 8, olho_y + 1), 1)
                pygame.draw.circle(tela, BRANCO, (self.rect.centerx + 8, olho_y + 1), 1)

        sobrancelha_y = self.rect.y + 18 + offset_y
        if self.direita:
            pygame.draw.line(tela, (65, 45, 25), (self.rect.centerx - 9, sobrancelha_y), (self.rect.centerx - 1, sobrancelha_y), 3)
            pygame.draw.line(tela, (65, 45, 25), (self.rect.centerx + 5, sobrancelha_y), (self.rect.centerx + 13, sobrancelha_y), 3)
        else:
            pygame.draw.line(tela, (65, 45, 25), (self.rect.centerx - 13, sobrancelha_y), (self.rect.centerx - 5, sobrancelha_y), 3)
            pygame.draw.line(tela, (65, 45, 25), (self.rect.centerx - 1, sobrancelha_y), (self.rect.centerx + 7, sobrancelha_y), 3)

        boca_y = self.rect.y + 30 + offset_y
        if self.socando or self.chutando:
            pygame.draw.arc(tela, (170, 70, 70), (self.rect.centerx - 7, boca_y, 14, 10), 0, 3.14, 3)
        else:
            pygame.draw.arc(tela, (150, 90, 90), (self.rect.centerx - 6, boca_y, 12, 8), 0.2, 2.9, 2)

        if self.socando:
            if self.direita:
                braco = pygame.Rect(self.rect.right - 20, self.rect.centery - 10 + offset_y, 32, 16)
            else:
                braco = pygame.Rect(self.rect.left - 12, self.rect.centery - 10 + offset_y, 32, 16)
            pygame.draw.ellipse(tela, (245, 215, 180), braco)
        else:
            braco_esq = pygame.Rect(self.rect.x - 9, self.rect.centery - 8 + offset_y, 22, 14)
            braco_dir = pygame.Rect(self.rect.right - 13, self.rect.centery - 8 + offset_y, 22, 14)
            pygame.draw.ellipse(tela, (245, 215, 180), braco_esq)
            pygame.draw.ellipse(tela, (245, 215, 180), braco_dir)

        perna_esq = pygame.Rect(self.rect.x + 12, self.rect.bottom - 32 + offset_y, 18, 37)
        perna_dir = pygame.Rect(self.rect.right - 30, self.rect.bottom - 32 + offset_y, 18, 37)
        pygame.draw.rect(tela, self.cor_secundaria, perna_esq, border_radius=6)
        pygame.draw.rect(tela, self.cor_secundaria, perna_dir, border_radius=6)

        if self.chutando:
            if self.direita:
                perna_chute = pygame.Rect(self.rect.right - 24, self.rect.bottom - 42 + offset_y, 30, 14)
            else:
                perna_chute = pygame.Rect(self.rect.left - 6, self.rect.bottom - 42 + offset_y, 30, 14)
            pygame.draw.ellipse(tela, self.cor_secundaria, perna_chute)

        if self.defendendo:
            escudo = pygame.Rect(self.rect.centerx - 22, self.rect.y + 25 + offset_y, 44, 55)
            pygame.draw.rect(tela, (190, 210, 240, 130), escudo, 4, border_radius=10)

lutador1 = Lutador(200, ALTURA - 205, AZUL, (60, 100, 160), {
    "esquerda": pygame.K_a,
    "direita": pygame.K_d,
    "pulo": pygame.K_w,
    "soco": pygame.K_s,
    "chute": pygame.K_x,
    "defesa": pygame.K_z
}, "Leo")

lutador2 = Lutador(LARGURA - 275, ALTURA - 205, VERMELHO, (160, 60, 70), {
    "esquerda": pygame.K_LEFT,
    "direita": pygame.K_RIGHT,
    "pulo": pygame.K_UP,
    "soco": pygame.K_DOWN,
    "chute": pygame.K_RIGHT,
    "defesa": pygame.K_LEFT
}, "Kai")

def desenhar_cenario():
    for y in range(ALTURA):
        azul = 190 - y // 6
        verde = 210 - y // 8
        cor_ceu = (130, verde, azul)
        pygame.draw.line(tela, cor_ceu, (0, y), (LARGURA, y))
    
    nuvens = [
        (150, 70, 140, 45),
        (450, 50, 160, 40),
        (750, 90, 120, 35),
        (80, 140, 140, 50)
    ]
    
    for x, y, larg, alt in nuvens:
        pygame.draw.ellipse(tela, (252, 252, 255), (x, y, larg, alt))
        pygame.draw.ellipse(tela, (245, 245, 250), (x, y, larg, alt), 2)
    
    montanhas = [
        [(0, 380), (180, 230), (380, 330), (580, 380)],
        [(350, 380), (550, 260), (750, 300), (1000, 360)]
    ]
    
    for pontos in montanhas:
        pygame.draw.polygon(tela, (90, 120, 80), pontos)
        pygame.draw.polygon(tela, (70, 100, 70), pontos, 2)
    
    for i in range(10):
        x = i * 95 + 30
        pygame.draw.rect(tela, (110, 80, 50), (x, 330, 18, 60))
        pygame.draw.circle(tela, (70, 130, 70), (x + 9, 310), 28)
        pygame.draw.circle(tela, (60, 120, 60), (x + 9, 310), 28, 2)
    
    pygame.draw.rect(tela, (190, 170, 130), (40, ALTURA - 130, LARGURA - 80, 70))
    pygame.draw.rect(tela, (160, 140, 110), (40, ALTURA - 130, LARGURA - 80, 70), 5)
    
    for i in range(0, LARGURA - 80, 45):
        for j in range(0, 70, 45):
            tatami_rect = pygame.Rect(40 + i, ALTURA - 130 + j, 45, 45)
            pygame.draw.rect(tela, (180, 160, 120), tatami_rect, 2)
    
    centro_x, centro_y = LARGURA // 2, ALTURA - 95
    pygame.draw.circle(tela, (210, 70, 70), (centro_x, centro_y), 24)
    pygame.draw.circle(tela, (190, 50, 50), (centro_x, centro_y), 24, 4)
    
    pygame.draw.line(tela, PRETO, (centro_x - 10, centro_y - 6), (centro_x + 10, centro_y + 6), 4)
    pygame.draw.line(tela, PRETO, (centro_x - 10, centro_y + 6), (centro_x + 10, centro_y - 6), 4)

def desenhar_barra_vida(x, y, vida, cor):
    largura_barra = 320
    altura_barra = 28
    
    pygame.draw.rect(tela, (45, 45, 50), (x, y, largura_barra, altura_barra), border_radius=6)
    
    vida_width = max(0, (vida / 100) * largura_barra)
    if vida > 70:
        cor_vida = VERDE
    elif vida > 30:
        cor_vida = AMARELO
    else:
        cor_vida = VERMELHO
    
    pygame.draw.rect(tela, cor_vida, (x, y, vida_width, altura_barra), border_radius=6)
    pygame.draw.rect(tela, BRANCO, (x, y, largura_barra, altura_barra), 3, border_radius=6)
    pygame.draw.rect(tela, (110, 110, 120), (x, y, largura_barra, altura_barra), 1, border_radius=6)

def main():
    rodando = True
    fim_de_jogo = False
    vencedor = None
    
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    rodando = False
                elif fim_de_jogo and evento.key == pygame.K_r:
                    lutador1.vida = 100
                    lutador2.vida = 100
                    lutador1.rect.x = 200
                    lutador2.rect.x = LARGURA - 275
                    lutador1.rect.y = ALTURA - 205
                    lutador2.rect.y = ALTURA - 205
                    fim_de_jogo = False
                    vencedor = None

        if not fim_de_jogo:
            lutador1.mover(lutador2)
            lutador2.mover(lutador1)

            if lutador1.vida <= 0:
                fim_de_jogo = True
                vencedor = lutador2.nome
            elif lutador2.vida <= 0:
                fim_de_jogo = True
                vencedor = lutador1.nome

        desenhar_cenario()
        lutador1.desenhar()
        lutador2.desenhar()

        desenhar_barra_vida(50, 25, lutador1.vida, AZUL)
        desenhar_barra_vida(LARGURA - 370, 25, lutador2.vida, VERMELHO)

        nome1 = fonte.render(lutador1.nome, True, BRANCO)
        nome2 = fonte.render(lutador2.nome, True, BRANCO)
        tela.blit(nome1, (50, 58))
        tela.blit(nome2, (LARGURA - 370, 58))

        controles_texto = fonte_pequena.render("WASD: Mover | S: Soco | X: Chute | Z: Defender", True, BRANCO)
        tela.blit(controles_texto, (LARGURA//2 - controles_texto.get_width()//2, ALTURA - 25))

        if fim_de_jogo:
            overlay = pygame.Surface((LARGURA, ALTURA))
            overlay.set_alpha(170)
            overlay.fill(PRETO)
            tela.blit(overlay, (0, 0))
            
            texto = fonte_grande.render(f"{vencedor} Venceu!", True, AMARELO)
            tela.blit(texto, (LARGURA//2 - texto.get_width()//2, ALTURA//2 - 50))
            
            restart = fonte.render("Pressione R para jogar novamente", True, BRANCO)
            tela.blit(restart, (LARGURA//2 - restart.get_width()//2, ALTURA//2 + 20))
            
            sair = fonte.render("ESC para sair", True, BRANCO)
            tela.blit(sair, (LARGURA//2 - sair.get_width()//2, ALTURA//2 + 65))

        pygame.display.flip()
        relogio.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()