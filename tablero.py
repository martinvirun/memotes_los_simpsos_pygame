import pygame
import time
import random
import tarjeta
from constantes import *
contador = [0]
contador_vidas =[0]
contador_aciertos = [0]
contador_primera_tarjeta = [0]
game_over = pygame.image.load("/home/martin/Documentos/programacion_1/Juego memotest - alumnes/recursos/Game_Over.jpg")
game_over = pygame.transform.scale(game_over,(ANCHO_PANTALLA,ALTO_PANTALLA))
winner = pygame.image.load("/home/martin/Documentos/programacion_1/Juego memotest - alumnes/recursos/winner.jpeg")
winner = pygame.transform.scale(winner,(ANCHO_PANTALLA,ALTO_PANTALLA))


def crear_tablero():
    '''
    Crea una lista de tarjetas
    Retorna un dict tablero
    '''
    tablero = {}
    tablero["tarjetas"] = generar_lista_tarjetas()
    tablero["tiempo_ultimo_destape"] = 0
    tablero["primer_tarjeta_seleccionada"] = None
    tablero["segunda_tarjeta_seleccionada"] = None
    

    # COMPLETAR
    return tablero

def generar_lista_tarjetas()->list:
    '''
    Función que se encarga de generar una lista de tarjetas ordenada aleatoriamente
    El for x me recorre todas las posiciones de x usando de step el ancho de la tarjeta
    El for y me recorre todas las posiciones de x usando de step el alto de la tarjeta
    Por ende me va a generar la cantidad de tarjetas que le especifique anteriormente 
    ajustandose a la resolución de mi pantalla de manera dinámica
    Usa la función random.shuffle para generar de manera aleatoria los identificadores. Genera una lista de identificadores
    en donde se repiten dos veces el mismo ya que en un memotest se repiten dos veces la misma carta
    Retorna la lista de las tarjetas generadas
    '''
    lista_tarjetas = []
    indice = 0
    lista_id = generar_lista_ids_tarjetas() 
    print(lista_id)
    

    for x in range(0, CANTIDAD_TARJETAS_H * ANCHO_TARJETA, ANCHO_TARJETA):
        for y in range(0, CANTIDAD_TARJETAS_V * ALTO_TARJETA, ALTO_TARJETA):
               tarjeta_sipsons = tarjeta.crear_tarjeta("0{0}.png".format(lista_id[indice]),lista_id[indice],"00.png",x,y)
               lista_tarjetas.append(tarjeta_sipsons)
               indice += 1
        pass
            # COMPLETAR
    
    return lista_tarjetas

def generar_lista_ids_tarjetas():
    lista_id = list(range(1,CANTIDAD_TARJETAS_UNICAS+1)) #Creo una lista con todos los identificadores posibles
    lista_id.extend(list(range(1,CANTIDAD_TARJETAS_UNICAS+1))) #Extiendo esa lista con otra lista identica ya que hay dos tarjetas iguales en cada tablero (mismo identificador)
    random.seed(time.time())
    random.shuffle(lista_id) #Esos identificadores los desordeno de forma al azar
    return lista_id
    
def detectar_colision(tablero: dict, pos_xy: tuple) -> int  :
    '''
    verifica si existe una colision alguna tarjetas del tablero y la coordenada recibida como parametro
    Recibe como parametro el tablero y una tupla (X,Y)
    Retorna el identificador de la tarjeta que colisiono con el mouse y sino retorna None

    '''
    for tab  in tablero["tarjetas"]:
        
        if tab["rectangulo"].collidepoint(pos_xy) == True:
            contador[0] += 1
            tab["visible"] = True
            if contador[0] == 1:
                tablero["primer_tarjeta_seleccionada"] = tab
            elif contador[0] == 2:
                tablero["segunda_tarjeta_seleccionada"] = tab
                contador[0] = 0           
            if(tablero["primer_tarjeta_seleccionada"] != None and tablero["segunda_tarjeta_seleccionada"] != None and tablero["segunda_tarjeta_seleccionada"]["identificador"] and tablero["primer_tarjeta_seleccionada"]["rectangulo"] != tablero["segunda_tarjeta_seleccionada"]["rectangulo"] ):
                 if (comprarar_tarjetas(tablero) != True ):
                     contador_vidas[0] += 1 
                     print(contador_vidas[0])    
                     SONIDO_ERROR.play()
                 else:
                        SONIDO_ACIERTO.play()
                        pass                     
                 pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            
        tablero["tiempo_ultimo_destape"] = pygame.time.get_ticks()
                  
    pass
    # COMPLETAR

def actualizar_tablero(tablero: dict) -> None:
    '''
    Verifica si es necesario actualizar el estado de alguna tarjeta, en funcion de su propio estado y el de las otras
    Recibe como parametro el tablero
    '''
    
    tiempo_actual = pygame.time.get_ticks()
    tiempo = tiempo_actual- tablero["tiempo_ultimo_destape"] 
    if(tiempo/1000 >= 1):
        tablero["tiempo_ultimo_destape"] = 0 
        for tab in tablero["tarjetas"]:
                if tab["descubierto"] == False:
                    tab["visible"] = False
                else:
                    tab["visible"] = True              
        tablero["primer_tarjeta_seleccionada"]= None
        tablero["segunda_tarjeta_seleccionada"] = None  
        pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
    if contador_vidas[0] == 8:
        return False
        
    # COMPLETAR

def comprarar_tarjetas(tablero: dict) -> bool | None:
    '''
    Funcion que se encarga de encontrar un match en la selección de las tarjetas del usuario.
    Si el usuario selecciono dos tarjetas está función se encargara de verificar si el identificador 
    de las mismas corresponde si es así retorna True, sino False. 
    En caso de que no hayan dos tarjetas seleccionadas retorna None
    '''
    retorno = None
    if tablero["primer_tarjeta_seleccionada"] != None and tablero["segunda_tarjeta_seleccionada"] != None:
        retorno = False
        if tablero["primer_tarjeta_seleccionada"]["identificador"] == tablero["segunda_tarjeta_seleccionada"]["identificador"] and tablero["primer_tarjeta_seleccionada"]["rectangulo"] != tablero["segunda_tarjeta_seleccionada"]["rectangulo"]:
            tarjeta.descubrir_tarjetas(tablero["tarjetas"], tablero["primer_tarjeta_seleccionada"]["identificador"])
            contador_aciertos[0] += 1
            retorno = True

    return retorno

def dibujar_tablero(tablero: dict, pantalla_juego: pygame.Surface):
    '''
    Dibuja todos los elementos del tablero en la superficie recibida como parametro
    Recibe como parametro el tablero y la ventana principal
    '''
    lista = tablero["tarjetas"]
    for tarjeta in lista:
        if (tarjeta["visible"] == True): 
            pantalla_juego.blit(tarjeta["superficie"],(tarjeta["rectangulo"].x,tarjeta["rectangulo"].y))
        else:
             pantalla_juego.blit(tarjeta["superficie_escondida"],(tarjeta["rectangulo"].x,tarjeta["rectangulo"].y))
        if contador_vidas[0] == 8 :
            pantalla_juego.blit(game_over,(0,0))
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
            #SONIDO_OUCH.play()
            break
        if contador_aciertos[0] == 6:
            pantalla_juego.blit(winner,(0,0))
            pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
        
    pass
    # COMPLETAR
   