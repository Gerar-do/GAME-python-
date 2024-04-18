import pygame
import random
import threading
import time
from network import Network

# Definir colores
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

# Tamaño de la pantalla
ANCHO = 800
ALTO = 600

# Tamaño de los bloques
TAM_BLOQUE = 20

class Gusano(threading.Thread):
    def __init__(self, id, start_pos):
        threading.Thread.__init__(self)
        self.id = id
        self.segmentos = [start_pos]
        self.direccion = 'RIGHT'
        self.score = 0

    def mover(self):
        cabeza = self.segmentos[0]
        if self.direccion == 'UP':
            nueva_cabeza = (cabeza[0], (cabeza[1] - TAM_BLOQUE) % ALTO)
        elif self.direccion == 'DOWN':
            nueva_cabeza = (cabeza[0], (cabeza[1] + TAM_BLOQUE) % ALTO)
        elif self.direccion == 'LEFT':
            nueva_cabeza = ((cabeza[0] - TAM_BLOQUE) % ANCHO, cabeza[1])
        elif self.direccion == 'RIGHT':
            nueva_cabeza = ((cabeza[0] + TAM_BLOQUE) % ANCHO, cabeza[1])
        self.segmentos.insert(0, nueva_cabeza)
        self.segmentos.pop()

    def dibujar(self, pantalla):
        color = VERDE if self.id == 0 else AZUL
        for segmento in self.segmentos:
            pygame.draw.rect(pantalla, color, [segmento[0], segmento[1], TAM_BLOQUE, TAM_BLOQUE])

class Manzana:
    def __init__(self):
        self.posicion = (random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE), random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE))

    def dibujar(self, pantalla):
        pygame.draw.rect(pantalla, ROJO, [self.posicion[0], self.posicion[1], TAM_BLOQUE, TAM_BLOQUE])

def main():
    pygame.init()

    pantalla = pygame.display.set_mode([ANCHO, ALTO])

    n = Network()
    id = int(n.id)
    gusano = Gusano(id, (ANCHO / 2, ALTO / 2))
    gusano_oponente = Gusano(1 - id, (ANCHO / 2, ALTO / 2 + TAM_BLOQUE))
    gusano.start()
    gusano_oponente.start()

    manzana = Manzana()

    reloj = pygame.time.Clock()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            elif evento.type == pygame.KEYDOWN:
                if id == 0:
                    if evento.key == pygame.K_w:
                        gusano.direccion = 'UP'
                    elif evento.key == pygame.K_s:
                        gusano.direccion = 'DOWN'
                    elif evento.key == pygame.K_a:
                        gusano.direccion = 'LEFT'
                    elif evento.key == pygame.K_d:
                        gusano.direccion = 'RIGHT'
                else:
                    if evento.key == pygame.K_UP:
                        gusano.direccion = 'UP'
                    elif evento.key == pygame.K_DOWN:
                        gusano.direccion = 'DOWN'
                    elif evento.key == pygame.K_LEFT:
                        gusano.direccion = 'LEFT'
                    elif evento.key == pygame.K_RIGHT:
                        gusano.direccion = 'RIGHT'

        pantalla.fill(NEGRO)

        gusano.mover()
        gusano_oponente.mover()
        gusano.dibujar(pantalla)
        gusano_oponente.dibujar(pantalla)

        if gusano.segmentos[0] == manzana.posicion:
            gusano.segmentos.append(gusano.segmentos[-1])
            gusano.score += 1
            manzana.posicion = (random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE), random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE))

        if gusano_oponente.segmentos[0] == manzana.posicion:
            gusano_oponente.segmentos.append(gusano_oponente.segmentos[-1])
            gusano_oponente.score += 1
            manzana.posicion = (random.randrange(0, ANCHO - TAM_BLOQUE, TAM_BLOQUE), random.randrange(0, ALTO - TAM_BLOQUE, TAM_BLOQUE))

        manzana.dibujar(pantalla)

        # Enviar información de la posición de ambos jugadores al servidor
        n.send(f"{gusano.id}:{gusano.segmentos[0][0]},{gusano.segmentos[0][1]}|{gusano_oponente.id}:{gusano_oponente.segmentos[0][0]},{gusano_oponente.segmentos[0][1]}")

        pygame.display.flip()
        reloj.tick(10)

if __name__ == "__main__":
    main()
