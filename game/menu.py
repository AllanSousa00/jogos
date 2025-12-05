import sys
import pygame
import math
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Paleta de cores moderna e clean
DARK_SLATE = (40, 44, 52)
SLATE_GRAY = (58, 63, 74)
STEEL_BLUE = (70, 130, 180)
CORAL = (255, 127, 80)
MINT = (72, 209, 204)
LIGHT_GRAY = (220, 220, 220)
OFF_WHITE = (248, 248, 248)
SOFT_BLACK = (30, 30, 30)

tela = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Menu de Jogos")

relogio = pygame.time.Clock()

# Fontes clean
try:
    fonte_titulo = pygame.font.Font(None, 64)
    fonte_subtitulo = pygame.font.Font(None, 36)
    fonte_botoes = pygame.font.Font(None, 32)
    fonte_pequena = pygame.font.Font(None, 20)
except:
    fonte_titulo = pygame.font.SysFont("segoeui", 64, bold=True)
    fonte_subtitulo = pygame.font.SysFont("segoeui", 36)
    fonte_botoes = pygame.font.SysFont("segoeui", 32)
    fonte_pequena = pygame.font.SysFont("segoeui", 20)

# Efeitos mínimos
dots = []

class Dot:
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(-50, -10)
        self.speed = random.uniform(0.3, 1.5)
        self.size = random.uniform(1, 2)
        self.color = (100, 100, 120, 100)
    
    def update(self):
        self.y += self.speed
        return self.y < SCREEN_HEIGHT + 20
    
    def draw(self, surface):
        alpha_surface = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(alpha_surface, self.color, (int(self.size), int(self.size)), int(self.size))
        surface.blit(alpha_surface, (int(self.x - self.size), int(self.y - self.size)))

def criar_dots():
    if len(dots) < 20 and random.random() < 0.2:
        dots.append(Dot())
    
    for i in range(len(dots) - 1, -1, -1):
        if not dots[i].update():
            dots.pop(i)

def desenhar_fundo_clean():
    # Gradiente sutil
    for y in range(SCREEN_HEIGHT):
        ratio = y / SCREEN_HEIGHT
        r = int(DARK_SLATE[0] * (1 - ratio) + SLATE_GRAY[0] * ratio)
        g = int(DARK_SLATE[1] * (1 - ratio) + SLATE_GRAY[1] * ratio)
        b = int(DARK_SLATE[2] * (1 - ratio) + SLATE_GRAY[2] * ratio)
        pygame.draw.line(tela, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    # Dots mínimos
    criar_dots()
    for dot in dots:
        dot.draw(tela)

def desenhar_texto_clean(texto, fonte, cor, posicao, centro=True):
    if centro:
        texto_surface = fonte.render(texto, True, cor)
        pos = (posicao[0] - texto_surface.get_width() // 2, posicao[1])
        tela.blit(texto_surface, pos)
        return texto_surface.get_rect(topleft=pos)
    else:
        texto_surface = fonte.render(texto, True, cor)
        tela.blit(texto_surface, posicao)
        return texto_surface.get_rect(topleft=posicao)

def desenhar_botao_moderno(texto, posicao_y, cor_base, cor_destaque, tecla, mouse_pos=None):
    texto_completo = f"{tecla}. {texto}"
    texto_surface = fonte_botoes.render(texto_completo, True, OFF_WHITE)
    
    # Retângulo do botão estilo moderno
    rect = pygame.Rect(0, 0, texto_surface.get_width() + 60, texto_surface.get_height() + 20)
    rect.center = (SCREEN_WIDTH // 2, posicao_y)
    
    # Verificar se o mouse está sobre o botão
    mouse_sobre = rect.collidepoint(mouse_pos) if mouse_pos else False
    
    # Cor do botão baseado no estado
    cor_atual = cor_destaque if mouse_sobre else cor_base
    
    # Botão principal
    pygame.draw.rect(tela, cor_atual, rect, border_radius=10)
    
    # Efeito de hover sutil
    if mouse_sobre:
        highlight = pygame.Surface(rect.size, pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 30))
        tela.blit(highlight, rect.topleft)
    
    # Texto do botão
    tela.blit(texto_surface, (rect.centerx - texto_surface.get_width() // 2, 
                             rect.centery - texto_surface.get_height() // 2))
    
    return rect

def desenhar_menu(mouse_pos=None):
    # Fundo clean
    desenhar_fundo_clean()
    
    # Título principal
    titulo_rect = desenhar_texto_clean(
        "JOGOS", fonte_titulo, OFF_WHITE, 
        (SCREEN_WIDTH // 2, 100)
    )
    
    # Linha divisória sutil
    line_y = titulo_rect.bottom + 20
    pygame.draw.line(tela, STEEL_BLUE, 
                    (SCREEN_WIDTH // 2 - 80, line_y), 
                    (SCREEN_WIDTH // 2 + 80, line_y), 2)
    
    # Subtítulo
    desenhar_texto_clean(
        "Menu Principal", fonte_subtitulo, LIGHT_GRAY,
        (SCREEN_WIDTH // 2, line_y + 30)
    )
    
    # Botões modernos
    botoes = [
        {"texto": "Pong", "y": 280, "cor_base": STEEL_BLUE, "cor_destaque": (90, 160, 220), "tecla": "1"},
        {"texto": "Jogo de Luta", "y": 360, "cor_base": CORAL, "cor_destaque": (255, 147, 100), "tecla": "2"},
        {"texto": "Sair", "y": 440, "cor_base": SLATE_GRAY, "cor_destaque": (78, 83, 94), "tecla": "Q"}
    ]
    
    rects_botoes = []
    for botao in botoes:
        rect = desenhar_botao_moderno(
            botao["texto"], botao["y"], 
            botao["cor_base"], botao["cor_destaque"], 
            botao["tecla"], mouse_pos
        )
        rects_botoes.append(rect)
    
    # Instruções
    desenhar_texto_clean(
        "Pressione o número correspondente ou clique para selecionar", 
        fonte_pequena, LIGHT_GRAY,
        (SCREEN_WIDTH // 2, 530)
    )
    
    pygame.display.flip()
    return rects_botoes

def iniciar_pong():
    try:
        import pong01
        pong01.main()
    except ImportError:
        print("Erro: módulo pong não encontrado")
    except Exception as erro:
        print(f"Erro ao executar pong: {erro}")

def iniciar_luta():
    try:
        import main as jogo_luta
        jogo_luta.main()
    except ImportError:
        print("Erro: módulo do jogo de luta não encontrado")
    except Exception as erro:
        print(f"Erro ao executar jogo de luta: {erro}")

def executar_menu():
    executando = True
    mouse_pos = None
    
    while executando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                executando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    pygame.quit()
                    iniciar_pong()
                    pygame.init()
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                elif evento.key == pygame.K_2:
                    pygame.quit()
                    iniciar_luta()
                    pygame.init()
                    pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                elif evento.key == pygame.K_q:
                    executando = False
            elif evento.type == pygame.MOUSEMOTION:
                mouse_pos = evento.pos
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.button == 1:  # Botão esquerdo do mouse
                    mouse_pos = evento.pos
                    
                    # Verificar clique nos botões
                    rects_botoes = desenhar_menu(mouse_pos)
                    for i, rect in enumerate(rects_botoes):
                        if rect.collidepoint(mouse_pos):
                            if i == 0:  # Pong
                                pygame.quit()
                                iniciar_pong()
                                pygame.init()
                                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                            elif i == 1:  # Luta
                                pygame.quit()
                                iniciar_luta()
                                pygame.init()
                                pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                            elif i == 2:  # Sair
                                executando = False
        
        rects_botoes = desenhar_menu(mouse_pos)
        relogio.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    executar_menu()