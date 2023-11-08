import pygame
from config import *
from math import sqrt
from pygame.locals import *
from random import *

playing_music = True

def crear_bloque(imagen = None, left=0, top=0, ancho=50, alto=50, color=(255, 255, 255), dir=3, borde=0, radio=-1, speed_x=5, speed_y=5):
    rec = pygame.Rect(left, top, ancho, alto)
    if imagen:
        imagen = pygame.transform.scale(imagen, (ancho, alto))
    return {"rect": rec, "color": color, "dir": dir, "borde": borde, "radio": radio, "speed_x": speed_x, "speed_y": speed_y, "imagen": imagen}

def crear_enemigo(imagen = None, left=0, top=0, ancho=50, alto=50, color=(255, 255, 255), dir=3, borde=0, radio=-1, speed_x=5, speed_y=5):
    rec = pygame.Rect(left, top, ancho, alto)
    if imagen:
        imagen = pygame.transform.scale(imagen, (ancho, alto))
    return {"rect": rec, "color": color, "dir": dir, "borde": borde, "radio": radio, "speed_x": speed_x, "speed_y": speed_y, "imagen": imagen}
                    
def load_fires_list(coins, cantidad, imagen = None):
    for i in range(cantidad):
        size_coin = randint(size_min_coin, size_max_coin)
        speed_coin = randint(speed_min_coin, speed_max_coin)
        coins.append(crear_bloque(imagen, randint(0, width - size_coin), randint(-height, -size_coin), 50, 80, YELLOW, speed_y= speed_coin))
        
def load_enemies_list(enemies, cantidad, imagen=None):
    start_x = width
    for i in range(cantidad):
        start_x += BLOCK_WIDTH + BLOCK_WIDTH
        enemies.append(crear_bloque(imagen, start_x, 560, ENEMY_WIDTH, ENEMY_HEIGHT, YELLOW, speed_y=6))
        
def dibujar_asteroides(superficie, fires):
    for fire in fires:
        if fire["imagen"]:
            superficie.blit(fire["imagen"], fire["rect"])
        else:
            pygame.draw.rect(superficie, fire["color"], fire["rect"], fire["borde"], fire["radio"])
            
def dibujar_enemigos(superficie, enemies):
    for enemy in enemies:
        if enemy["imagen"]:
            superficie.blit(enemy["imagen"], enemy["rect"])
        else:
            pygame.draw.rect(superficie, enemy["color"], enemy["rect"])
            
def mostrar_texto(superficie, texto, fuente, coordenadas, color_fuente):
    sup_texto = fuente.render(texto, True, color_fuente)
    rect_texto = sup_texto.get_rect()
    rect_texto.center = coordenadas
    superficie.blit(sup_texto, rect_texto)
    
def mostrar_texto_2(superficie, texto, x, y, font_size = 36, color = (0, 0, 0)):
    fuente = pygame.font.SysFont("Minecraft", font_size)
    render = fuente.render(texto, True, color)
    rect_texto = render.get_rect(center = (x, y))
    superficie.blit(render, rect_texto)

def terminar():
    pygame.quit()
    exit()

def crear_boton (screen, rect, texto, color_normal, color_hover):
    posicion_mouse = pygame.mouse.get_pos()

    if rect.collidepoint(posicion_mouse) :
        pygame.draw.rect(screen, color_hover, rect, border_radius = 0)
    else:
        pygame.draw.rect(screen, color_normal, rect, border_radius = 0)
    mostrar_texto_2(screen, texto, rect.centerx, rect.centery)

def wait_user_click(screen, button_comenzar, button_salir, button_musica_on, button_musica_off):
    while True:
        crear_boton(screen, button_comenzar, "Comenzar", WHITE, VIOLETA)
        crear_boton(screen, button_musica_on, "Musica On", WHITE, VIOLETA)
        crear_boton(screen, button_musica_off, "Musica Off", WHITE, RED)
        crear_boton(screen, button_salir, "Salir", WHITE, RED)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == QUIT:
                terminar()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminar()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    if button_comenzar.collidepoint(event.pos):
                        return None
                    elif button_salir.collidepoint(event.pos):
                        terminar()
                    elif button_musica_off.collidepoint(event.pos):
                        if playing_music:
                            pygame.mixer.music.pause()
                    elif button_musica_on.collidepoint(event.pos):
                        if playing_music:
                            pygame.mixer.music.unpause()
                    
def wait_user():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminar()

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminar()
                return

            
