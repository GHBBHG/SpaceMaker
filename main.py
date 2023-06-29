import pygame
import tkinter as tk
from tkinter import simpledialog, filedialog
import os

# Configurações da tela
largura = 1000
altura = 563
branco = (255, 255, 255)
vermelho = (255, 0, 0)
azul = (30, 144, 255)

marcadores = []

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Space Marker")

# Carregar imagens
icone = pygame.image.load("nave.png")
pygame.display.set_icon(icone)

imagem_fundo = pygame.image.load("bg.jpg")
imagem_fundo = pygame.transform.scale(imagem_fundo, (largura, altura))
largura_imagem, altura_imagem = imagem_fundo.get_size()

estrela = pygame.image.load("estrela.png")

# Função para obter o nome da estrela do usuário, caixa desconhecida
def obter_nome_estrela():
    root = tk.Tk()
    root.withdraw()

    nome_estrela = simpledialog.askstring("Nome da Estrela", "Digite o nome da estrela ou escolha 'desconhecida':",
                                          parent=root, initialvalue="desconhecida")
    return nome_estrela

estrela_personalizada = pygame.image.load("estrela.png")
estrela_personalizada = pygame.transform.scale(estrela_personalizada, (50, 50))

font = pygame.font.SysFont(None, 20)

def informacoes():
    text = font.render("Pressione F9 para salvar", True, branco)
    tela.blit(text, (10, 10))
    text = font.render("Pressione F10 para carregar", True, branco)
    tela.blit(text, (10, 25))
    text = font.render("Pressione F11 para Limpar a tela", True, branco)
    tela.blit(text, (10, 40))

    pygame.display.flip()

# Carregar dados das estrelas (se existir)
dados_estrelas = []
if os.path.exists("estrelas.txt"):
    with open("estrelas.txt", "r") as arquivo:
        dados_estrelas = arquivo.read().splitlines()

# Carregar trilha de música em loop
pygame.mixer.init()
pygame.mixer.music.load("Space_sound.mp3")
pygame.mixer.music.play(-1)  # "-1" indica que a música será reproduzida em loop

# Funções do informações
def salvar_estrela():
    with open("estrelas.txt", "w") as arquivo:
        arquivo.write('\n'.join(dados_estrelas))

# limpar tela
def limpar_marcadores():
    tela.blit(imagem_fundo, (0, 0))
    informacoes()
    coordenadas_estrelas.clear()

def linhas():
      if len(coordenadas_estrelas) >= 2:
                for i in range(len(coordenadas_estrelas) - 1):
                    x1, y1 = coordenadas_estrelas[i]
                    x2, y2 = coordenadas_estrelas[i + 1]
                    pygame.draw.line(tela, branco, (x1, y1), (x2, y2), 2)
                    dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
                    texto_dist = font.render(f"{dist:.2f}", True, azul)
                    tela.blit(texto_dist, ((x1 + x2) // 2, (y1 + y2) // 2))

def salvar():
    dados_estrelas.append(f"{nome_estrela},{x},{y}")

tela.blit(imagem_fundo, (0, 0))
informacoes()

coordenadas_estrelas = []
# Loop principal do jogo
rodando = True
while rodando:
    clock = pygame.time.Clock()
    linhas()
    try:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    running = False
                elif evento.key == pygame.K_F9:
                    salvar_estrela()
                elif evento.key == pygame.K_F10:
                    pass
                elif evento.key == pygame.K_F11:
                    limpar_marcadores()
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos_mouse = pygame.mouse.get_pos()
                x, y = pos_mouse

                clock.tick(60)

                if 0 <= x < largura_imagem and 0 <= y < altura_imagem:
                    nome_estrela = obter_nome_estrela()
                    print("Nome da estrela:", nome_estrela)

                    if nome_estrela != "desconhecida":
                        x_estrela = x - estrela_personalizada.get_width() // 2
                        y_estrela = y - estrela_personalizada.get_height() // 2
                        tela.blit(estrela_personalizada, (x_estrela, y_estrela))

                        # Armazenar informações da estrela
                        salvar()

                        coordenadas_estrelas.append((x, y))

                        # Exibir nome da estrela ao lado do PNG
                        fonte = pygame.font.Font(None, 20)
                        texto_surface = fonte.render(nome_estrela, True, (255, 255, 255))
                        tela.blit(texto_surface, (x_estrela + estrela_personalizada.get_width() + 5, y_estrela))

                    else:
                        x_estrela = x - estrela_personalizada.get_width() // 2
                        y_estrela = y - estrela_personalizada.get_height() // 2
                        tela.blit(estrela_personalizada, (x_estrela, y_estrela))

                        # Armazenar informações da estrela desconhecida
                        salvar()

                        coordenadas_estrelas.append((x, y))

                        # Exibir nome da estrela ao lado do PNG
                        fonte = pygame.font.Font(None, 20)
                        texto_surface = fonte.render(f"Desconhecida ({x}, {y})", True, (255, 255, 255))
                        tela.blit(texto_surface, (x_estrela + estrela_personalizada.get_width() + 5, y_estrela))

        pygame.display.flip()

    except pygame.error as e:
        print("Ocorreu um erro no Pygame:", e)