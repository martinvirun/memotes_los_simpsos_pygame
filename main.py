import pygame
from constantes import *
import tablero


def terminar_partida(cronometro: int, cantidad_movimientos: int, tablero: dict):
    '''
    Verifico si el usuario ganó o perdio la partida
    si se queda sin movimientos o sin tiempo perdió 
    si todos las tarjetas del tablero están descubiertas el jugador gano
    Recibe el cronometro, los movimientos actuales del jugador y el tablero
    Si el jugador gano cambia la pantalla y muestra (VICTORIA O DERROTA DEPENDIENDO DE LO QUE HAYA PASADO)
    Retorna True si la partida termino y False si no lo terminó.
    '''
    pass
imagen = pygame.image.load("/home/martin/Documentos/programacion_1/Juego memotest - alumnes/recursos/nubes02.jpeg")
imagen = pygame.transform.scale(imagen,(ANCHO_PANTALLA,ALTO_PANTALLA))

# Configuración inicial de pygame
pygame.init()
pantalla_juego = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption('Los Simpsons Memotest')
clock_fps = pygame.time.Clock() # Creamos un Clock para poder fijar los FPS

# Creamos eventos de tiempo
evento_1000ms = pygame.USEREVENT
pygame.time.set_timer(evento_1000ms, 1000)

# Configuracion inicial del juego
tablero_juego = tablero.crear_tablero()
cronometro = TIEMPO_JUEGO
cantidad_movimientos = CANTIDAD_INTENTOS
cantidad_tarjetas_cubiertas = CANTIDAD_TARJETAS_UNICAS * 2
cantidad_tarjetas_descubiertas = 0

esta_corriendo = True

while esta_corriendo:
    
    # Fijamos un valor de FPS
    clock_fps.tick(FPS)
    
    # Verificamos si el juego termino
    if terminar_partida(cronometro, cantidad_movimientos, tablero_juego):
        pass

    # Manejamos los eventos
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            esta_corriendo = False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos
            SONIDO_CLICK.play()
            if tablero.detectar_colision(tablero_juego, pos) != None:
                SONIDO_VOLTEAR.play()

        
        # Cada vez que pase un segundo restamos uno al tiempo del cronometro
        if event.type == evento_1000ms:
            cronometro -= 1

        
        tablero.actualizar_tablero(tablero_juego) 
        

    
    # Dibujar pantalla
    pantalla_juego.blit(imagen,(0,0))
    #pantalla_juego.fill(COLOR_BLANCO) # Pintamos el fondo de color blanco
    tablero.dibujar_tablero(tablero_juego, pantalla_juego)
    
    # Mostramos los cambios hechos
    pygame.display.flip()

pygame.quit()
