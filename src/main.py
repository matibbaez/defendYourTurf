import sys
import csv
import pygame
from config import *
from functions.colisiones import *
from juego import crear_bloque, wait_user
from juego import *
from functions.random import *
from random import randint, randrange
from pygame import display, time, draw, event
from pygame.locals import *       

# Inicializar todos los modulos
try:
    pygame.init()
except pygame.error:
    print("Error al inicializar pygame.")
    sys.exit()

# Tamaño de pantalla (superficie)
screen = pygame.display.set_mode(size_screen)
# Duración de cada iteración
clock = pygame.time.Clock()
# Nombre del juego
pygame.display.set_caption("Defend your turf!")
# Cambiar color
screen.fill(CUSTOM)
# Fuente
fuente = pygame.font.SysFont("Minecraft", 30)
# Draw
draw = pygame.draw

tiempo_transcurrido = 0

# Sonidos
playing_music = True

count_fires = 10
count_enemies = 6
max_contador = 0

speed_y_rapidos = 8

invulnerable = False
mostrar_mensaje_invulnerabilidad = False
tiempo_mensaje_invulnerabilidad = 0
tiempo_invulnerable = 0

enemigos_rapidos = False
tiempo_enemigos_rapidos = 0
mensaje_enemigos_rapidos = False
tiempo_mensaje_enemigos_rapidos = 0
tiempo_transcurrido_enemigos_rapidos = 0  

laser_rapido = False
tiempo_laser_rapido = 0
mensaje_laser_rapido = False
tiempo_mensaje_laser_rapido = 0
tiempo_transcurrido_laser_rapido = 0  

# Volumen sonidos
pygame.mixer.music.load("./src/assets/sounds/musica_cyber.mp3")
game_over_sound = pygame.mixer.Sound("./src/assets/sounds/game_over_final.mp3")
laser_sound = pygame.mixer.Sound("./src/assets/sounds/laser.mp3")
pygame.mixer.music.set_volume(0.1)
game_over_sound.set_volume(0.1)
laser_sound.set_volume(0.1)
playing_music = True

# Cargo imagenes
background = pygame.transform.scale(pygame.image.load("./src/assets/images/AdobeStock_216900207.jpeg"), size_screen)
background_2 = pygame.transform.scale(pygame.image.load("./src/assets/images/background2.jpg"), size_screen)
background_inicio = pygame.transform.scale(pygame.image.load("./src/assets/images/DYTbackground.jpg"), size_screen)
background_pause = pygame.transform.scale(pygame.image.load("./src/assets/images/PAUSE.jpg"), size_screen)
background_menu = pygame.transform.scale(pygame.image.load("./src/assets/images/main_menu_2.jpg"), size_screen)
background_fin = pygame.transform.scale(pygame.image.load("./src/assets/images/gameoverbackground.jpg"), size_screen)

player = pygame.transform.scale(pygame.image.load("./src/assets/images/character3.png"), (50, 50))
rect_player = player.get_rect()
mask_player = pygame.mask.from_surface(player)
mask_image = mask_player.to_surface()

enemy_1 = pygame.transform.scale(pygame.image.load("./src/assets/images/enemy3.gif"), (50, 50))
rect_enemy = enemy_1.get_rect()
mask_enemie = pygame.mask.from_surface(enemy_1)
mask_image_enemy = mask_enemie.to_surface()

image_boss_2 = pygame.image.load("./src/assets/images/boss3.png")

image_fire = pygame.image.load("./src/assets/images/metfinal.png")
rect_fire = image_fire.get_rect()
mask_fire = pygame.mask.from_surface(image_fire)
mask_image_fire = mask_fire.to_surface()

image_boss = pygame.image.load("./src/assets/images/boss3.png")

bullet = pygame.image.load("./src/assets/images/bullet.png")
bullet_2 = pygame.image.load("./src/assets/images/bullet2.png")
bullet_3 = pygame.image.load("./src/assets/images/bullet3.png")

# Creo el rectangulo
character = crear_bloque(player, character_x, character_y, BLOCK_WIDTH, BLOCK_HEIGHT, RED, radio= 25)

laser = None

# Variable de control
is_running = True
message_shown = False

button_comenzar = pygame.Rect(0, 0, button_width, button_height)
button_comenzar.center = center_screen

button_musica_on = pygame.Rect(0, 0, button_width, button_height)
button_musica_on.center = (center_screen[0], center_screen[1] + 100)

button_musica_off = pygame.Rect(0, 0, button_width, button_height)
button_musica_off.center = (center_screen[0], center_screen[1] + 200)

button_salir = pygame.Rect(0, 0, button_width, button_height)
button_salir.center = (center_screen[0], center_screen[1] + 300)

pygame.mixer.music.play(-1) 

while True:
    # Pantalla inicio
    screen.fill(BLACK)
    screen.blit(background_inicio, origin)
    wait_user_click(screen, button_comenzar, button_musica_on, button_musica_off, button_salir)
    
    pygame.display.flip()
    
    # Inicializacion del juego
    puntos = 0
    lives = 5
    tiempo_transcurrido = 0
    
    texto = fuente.render(f"Puntos: {puntos}", True, WHITE)
    rect_texto = texto.get_rect(topleft = (30, 40))
    
    texto_lives = fuente.render(f"Lives: {lives}", True, WHITE)
    rect_texto_lives = texto_lives.get_rect(topright = (width - 30, 40))
    
    is_running = True    
    
    fires = []
    load_fires_list(fires, count_fires, image_fire) 
    
    enemies = []
    load_enemies_list(enemies, count_enemies, enemy_1)
    
    while is_running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                is_running = False
                
            if event.type == KEYDOWN:
                
                if event.key == K_f:
                    if not laser:
                        character_rect = character["rect"]
                        character_center = character_rect.center 
                        laser_w, laser_h = size_laser
                        laser_x = character_rect.right  
                        laser_y = character_center[1] - laser_h // 8 
                        laser = crear_bloque(bullet_3, laser_x, laser_y, 20, 7, CUSTOM, speed_x=speed_laser)
                        if playing_music:
                            laser_sound.play()

                if event.key == K_RIGHT or event.key == K_d:
                    move_right = True
                    move_left = False
                if event.key == K_LEFT or event.key == K_a:
                    move_left = True
                    move_right = False
                    
                if event.key == K_m:
                    if playing_music:
                        pygame.mixer.music.pause()
                    else:                        
                        pygame.mixer.music.unpause()
                    playing_music = not playing_music
                    
                if event.key == K_p:
                    if playing_music:
                        pygame.mixer.music.pause()
                    screen.blit(background_pause, origin)
                    pygame.display.flip()
                    wait_user()
                    if playing_music:
                        pygame.mixer.music.unpause()
                    
            elif event.type == KEYUP:
                if event.key == K_RIGHT or event.key == K_d:
                    move_right = False
                if event.key == K_LEFT or event.key == K_a:
                    move_left = False
                # Para cerrar el juego con ESC
                if event.key == K_ESCAPE:
                    is_running = False
          
        # ---> Actualizar los elementos
        tiempo_transcurrido = pygame.time.get_ticks() // 1000

        mensaje_temporizador = fuente.render(f"Tiempo: {tiempo_transcurrido} s", True, WHITE)

        rect_mensaje_temporizador = mensaje_temporizador.get_rect(midtop = (width // 2, 40))  
        
        # Movimiento del bloque de acuerdo a su direccion
        if move_right and character["rect"].right <= (width - SPEED):
            # Derecha
            character["rect"].left += SPEED
        if move_left and character["rect"].left >= (0 + SPEED):
            # Izquierda
            character["rect"].left -= SPEED
            
        if laser:
            if laser["rect"].bottom > 0 and laser["rect"].right < width:
                laser["rect"].move_ip(laser["speed_x"], 0)
            else:
                laser = None

        for enemy in enemies:
            enemy["rect"].move_ip(-enemy["speed_y"], 0)    
            
        for enemy in enemies[:]:
            if enemy["rect"].right < 0:
                enemies.remove(enemy)
                
        for enemy in enemies[:]:
            if not invulnerable or (pygame.time.get_ticks() - tiempo_invulnerable) >= 10000:
                if detectar_colision(enemy["rect"], character["rect"]):
                    enemies.remove(enemy)
                    if lives > 1:
                        lives -= 1
                        texto_lives = fuente.render(f"Lives: {lives}", True, WHITE)
                        rect_texto_lives = texto_lives.get_rect(topright = (width - 30, 40))
                    else:
                        is_running = False
        
        try:
        
            if puntos > 5:
                for fire in fires:
                    fire["rect"].move_ip(0, fire["speed_y"])
                        
            for fire in fires:
                if fire["rect"].top > 700:
                    fire["rect"].move_ip(0, - (height + fire["rect"].height))
            
            for fire in fires[:]:
                if fire["rect"].top > height:
                    fires.remove(fire)
                    
            for fire in fires[:]:
                if not invulnerable or (pygame.time.get_ticks() - tiempo_invulnerable) >= 10000:
                    if character["rect"].colliderect(fire["rect"]):
                        fires.remove(fire)
                        if lives > 1:
                            lives -= 1
                            texto_lives = fuente.render(f"Lives: {lives}", True, WHITE)
                            rect_texto_lives = texto_lives.get_rect(topright=(width - 30, 40))
                        else:
                            is_running = False
            if len(fires) == 0:
                load_fires_list(fires, count_fires, image_fire)         
                        
            if laser:   
                colision = False    
                for enemy in enemies[ : ]:
                    if detectar_colision_circ(enemy["rect"], laser["rect"]):
                        enemies.remove(enemy)
                        puntos += 1
                        texto = fuente.render(f"Puntos: {puntos}", True, WHITE)
                        rect_texto = texto.get_rect(topleft = (30, 40))
    
                        colision = True
                if colision == True:
                    laser = None
                        
            if len(enemies) == 0:
                load_enemies_list(enemies, count_enemies, image_boss)
                
            # Verificar puntos y poderes --->
                    
            if puntos == 50 and count_fires < 15:
                count_fires += 5
                load_fires_list(fires, count_fires, image_fire)
                
                mensaje_nuevos_fuegos = fuente.render("¡Nuevos fuegos, ten cuidado!", True, RED)
                rect_mensaje_nuevos_fuegos = mensaje_nuevos_fuegos.get_rect(center=(width // 2, height // 2))
                screen.blit(mensaje_nuevos_fuegos, rect_mensaje_nuevos_fuegos)
                pygame.display.flip()
                pygame.time.delay(2000)
                
            if puntos == 70:
                count_fires += 5
                load_fires_list(fires, count_fires, image_fire)
                
                mensaje_nuevos_fuegos = fuente.render("¡Nuevos fuegos, ten cuidado!", True, RED)
                rect_mensaje_nuevos_fuegos = mensaje_nuevos_fuegos.get_rect(center=(width // 2, height // 2))
                screen.blit(mensaje_nuevos_fuegos, rect_mensaje_nuevos_fuegos)
                pygame.display.flip()
                pygame.time.delay(2000)
                    
            if puntos == 20 and not enemigos_rapidos:
                enemigos_rapidos = True
                tiempo_enemigos_rapidos = pygame.time.get_ticks()
                mensaje_enemigos_rapidos = True
                
            if puntos == 40 and not laser_rapido:
                laser_rapido = True
                tiempo_laser_rapido = pygame.time.get_ticks() 
                mensaje_laser_rapido = True


            if enemigos_rapidos and tiempo_transcurrido_enemigos_rapidos >= 10000:  
                enemigos_rapidos = False
                mensaje_enemigos_rapidos = False
                
            if laser_rapido:
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido_laser_rapido = tiempo_actual - tiempo_laser_rapido

            if tiempo_transcurrido_laser_rapido >= 10000:
                laser_rapido = False
                mensaje_laser_rapido = False

            velocidad_enemigos = speed_y
            if enemigos_rapidos:
                velocidad_enemigos = speed_y_rapidos 
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido_enemigos_rapidos = tiempo_actual - tiempo_enemigos_rapidos
                for enemy in enemies:
                    enemy["rect"].move_ip(-velocidad_enemigos, 0)
                    
            velocidad_character = speed_y
            if laser_rapido:
                velocidad_laser = speed_y_rapidos 
                tiempo_actual = pygame.time.get_ticks()
                tiempo_transcurrido_laser_rapido = tiempo_actual - tiempo_laser_rapido
                if laser:
                    laser["speed_x"] += 1
    
            if puntos == 10 and not invulnerable:
                invulnerable = True
                tiempo_invulnerable = pygame.time.get_ticks()
                mostrar_mensaje_invulnerabilidad = True

            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = tiempo_actual - tiempo_invulnerable

            if tiempo_transcurrido >= 10000:
                invulnerable = False
                
        except ZeroDivisionError:
            print("Se ha producido una división por cero.")
        
        except FileNotFoundError as e:
            print(f"Se ha producido un error de archivo: {e}")
            
        except pygame.error:
            print("Se ha producido un error de Pygame.")
            
        # Dibujar mensajes en la pantalla --->

        screen.blit(background, origin)
        dibujar_asteroides(screen, fires)
        dibujar_enemigos(screen, enemies)
        screen.blit(character["imagen"], character["rect"])
        
        screen.blit(mensaje_temporizador, rect_mensaje_temporizador)
        if laser:
            pygame.draw.rect(screen, laser["color"], laser["rect"])
        
        if invulnerable:
            mensaje = fuente.render(f"¡Invulnerabilidad! Tiempo restante: {10 - tiempo_transcurrido // 1000} s", True, YELLOW)
            rect_mensaje = mensaje.get_rect(center=(width // 2, height // 2))
            screen.blit(mensaje, rect_mensaje)

        if mensaje_enemigos_rapidos:
            mensaje = fuente.render(f"¡Enemigos rapidos! Tiempo restante: {10 - tiempo_transcurrido_enemigos_rapidos // 1000} s", True, RED)
            rect_mensaje = mensaje.get_rect(center=(width // 2, height // 2))
            screen.blit(mensaje, rect_mensaje)
            
        if mensaje_laser_rapido:
            mensaje = fuente.render(f"¡Laser aumentado! Tiempo restante: {10 - tiempo_transcurrido_laser_rapido // 1000} s", True, YELLOW)
            rect_mensaje = mensaje.get_rect(center=(width // 2, height // 2))
            screen.blit(mensaje, rect_mensaje)
            
        screen.blit(texto, rect_texto)
        screen.blit(texto_lives, rect_texto_lives)

        pygame.display.flip()
    
    if puntos > max_contador:
        max_contador = puntos
    
    screen.fill(WHITE)
    pygame.mixer.music.stop()
    game_over_sound.play()
    screen.blit(background_fin, origin)
    mostrar_texto(screen, f"Max score: {max_contador}", fuente, (width // 2, 50), WHITE)
    pygame.display.flip()
    wait_user()
            
terminar()