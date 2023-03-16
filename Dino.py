import os, sys
dirpath = os.getcwd()
sys.path.append(dirpath)
if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)
###
    
import pygame
from pygame.locals import *
from random import *
from engine import *
 

class Dinos(RigidyBory):
    def __init__(self, pos, size, image, gravity_acceleration, jump_force, debug):
        super().__init__(pos, size, image, debug, gravity_acceleration)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        if image != '':
            self.rect2 = image.get_rect()
        self.jump_force = jump_force
        self.jumping = False
        self.image = image
        self.debug = debug
        self.has_animations = False
        self.gravity_acceleration = gravity_acceleration
        self.gravity = 0
        self.neuronio1 = Neuronio()
        self.neuronio2 = Neuronio()
        self.neuronio_pulo = Neuronio()


    def update(self, colliders_list, list_cactus, velocidade):
        distancia = 0
        for cactu in list_cactus:
            if cactu[0] > self.rect.x:
                distancia = cactu[0] - self.rect.x
                break

        self.update_gravity(colliders_list)
        self.pular(distancia, velocidade)
        if self.rect.collidelist(list_cactus) != -1:
            self.kill()
        

    def update_gravity(self, colliders_list):
        self.rect.y += self.gravity
        if self.gravity < self.rect.h:
            self.gravity += self.gravity_acceleration
            if self.gravity > 0:
                colliders = test_collision_list(colliders_list, self)
                collision_2d(colliders, self, 'bottom')

    def rede_neural(self, distancia, velocidade):
        resultado_neuronio1 = self.neuronio1.processar(self.neuronio1.pesar(self.neuronio1.peso1, distancia), self.neuronio1.pesar(self.neuronio1.peso2, velocidade))
        resultado_neuronio2 = self.neuronio2.processar(self.neuronio2.pesar(self.neuronio2.peso1, distancia), self.neuronio2.pesar(self.neuronio2.peso2, velocidade))
        resultado_pulo = self.neuronio_pulo.processar(self.neuronio_pulo.pesar(self.neuronio_pulo.peso1, resultado_neuronio1), self.neuronio_pulo.pesar(self.neuronio_pulo.peso2, resultado_neuronio2))

        if resultado_pulo > 0:
            return True
        else:
            return False
        

    def pular(self, distancia, velocidade):
        if self.jumping:
            if self.rede_neural(distancia, velocidade):
                self.jumping = False
                self.gravity = -self.jump_force  
        


class Neuronio():
    def __init__(self):
        self.peso1 = randint(-1000,1000)
        self.peso2 = randint(-1000,1000)
        
        
    def pesar(self, peso, info):
        return peso*info


    def processar(self,info1,info2):
        resultado = info1 + info2
        if resultado < 0:
            return 0
        else:
            return resultado

                 

def nuvens(lista, tempo, tempo_limite, pos_x, pos_y, velocidade_min, velocidade_max):
    if tempo == tempo_limite:
        numero = random()
        if numero > 0.4:
            pos_y = randint(0, 150)
            nuvem = pygame.Rect(pos_x, pos_y, randint(100, 200), randint(30,70))
            velocidade = randint(velocidade_min, velocidade_max)
            nuvem_list = [nuvem, velocidade]
            lista.append(nuvem_list)
    return lista


def cactus(lista, tempo, tempo_limite, pos_x, pos_y):
    if tempo == tempo_limite:
        numero = random()
        if numero > 0.25:
            altura = randint(40,50)
            pos_y = (screen_height-50) - altura
            cactu = pygame.Rect(pos_x, pos_y, 20, altura)
            cactu_2 = cactu[:]
            lista.append(cactu)
            if numero > 0.8:
                cactu_2[0] += 25
                cactu_2[3] = randint(40, 50)
                cactu_2[1] = (screen_height-50) - cactu_2[3]
                lista.append(cactu_2)
    return lista


pygame.init()
screen = pygame.display.set_mode((800, 600))
fullscreen = False
screen_width = screen.get_width()
screen_height = screen.get_height()
fonte = pygame.font.SysFont('Arial',34)
clock = pygame.time.Clock()
lista_nuvens = list()
lista_cactus = list()
chao = pygame.Rect(0, screen_height-50, screen_width, 50)
colliders_list = []
colliders_list.append(chao)
segundos = 0
tempo_limite_nuvem = 30
tick_nuvem = 20
tempo_limite_cactu = 30
tick_cactu = 20
tick_pontos = 0
contador_45 =0
contador_300 = 0
velocidade_cactus = -10
velocidade_nuvem_max = 2
velocidade_nuvem_min = 1
pontos = 0
run = True
gameover = False
paused = True
group = pygame.sprite.Group()

for i in range(10000):
    dino = Dinos((randint(0,100), screen_height-300), (20, 40), '', 1, 15, True)
    dino.color = (randint(0,255), randint(0,255), randint(0,255))


while run:
    cont = 0
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
        if event.type == KEYDOWN :
                
            if event.key == K_ESCAPE:
                run = False

            elif event.key == K_p:
                if not paused:
                    paused = True
                else:
                    paused = False

            elif event.key == K_m:
                if fullscreen:
                    screen = pygame.display.set_mode((800, 600))
                    screen_width = screen.get_width()
                    screen_height = screen.get_height()
                    dino = pygame.Rect(100, screen_height-40, 20, 40)
                    chao = pygame.Rect(0, screen_height-50, screen_width, 50)
                    fullscreen = False
                else:
                    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                    screen_width = screen.get_width()
                    screen_height = screen.get_height()
                    dino = pygame.Rect(100, screen_height-40, 20, 40)
                    chao = pygame.Rect(0, screen_height-50, screen_width, 50)
                    fullscreen = True
                    
            elif event.key == K_s:
                for dino in group:
                    print('='*5)
                    print(dino.neuronio1.peso1)
                    print(dino.neuronio1.peso2)
                    print(dino.neuronio2.peso1)
                    print(dino.neuronio2.peso2)
                    print(dino.neuronio_pulo.peso1)
                    print(dino.neuronio_pulo.peso2)
                    print('='*5)
                pygame.quit()
       
                
    #update

    if (not gameover) and (not paused):

        if len(group) < 0:
            gameover =True
        
        group.update(colliders_list, lista_cactus, velocidade_cactus)
            

        tick_nuvem += 1
        if tick_nuvem > tempo_limite_nuvem:
            tick_nuvem = 0
        
        tick_cactu += 1
        if tick_cactu > tempo_limite_cactu:
            tempo_limite_cactu = randint(30,45)
            if tempo_limite_cactu >= 40:
                contador_45 += 1
            else:
                contador_45 = 0
            tick_cactu = 0
            
        tick_pontos += 1
        if tick_pontos == 2:
            pontos += 1
            tick_pontos = 0
            contador_300 += 1
            if contador_300 == 300:
                contador_300 = 0
                velocidade_nuvem_min += 1
                velocidade_nuvem_max += 1
                #if velocidade_cactus !=  -40:
                velocidade_cactus -= 10
                print(velocidade_cactus)
                for nuvem in lista_nuvens:
                    nuvem[1] += 1
                if tempo_limite_nuvem > 15:
                    tempo_limite_nuvem -= 5

                    
        lista_nuvens = nuvens(lista_nuvens, tick_nuvem, tempo_limite_nuvem, screen_width+10 ,0, velocidade_nuvem_min, velocidade_nuvem_max)
        lista_cactus = cactus(lista_cactus, tick_cactu, tempo_limite_cactu, screen_width+10, 0)
        
        for cactu in lista_cactus:
            cactu[0] += velocidade_cactus

            
        if contador_45 == 2:
            contador_cactu = 0
            for cactu in lista_cactus:
                if cactu[0]+cactu[2] < 0:
                    lista_cactus.pop(contador_cactu)
                contador_cactu += 1

        contador_nuvem = 0 
        for nuvem in lista_nuvens:
            nuvem[0][0] -= nuvem[1]
            if nuvem[0][0]+nuvem[0][2] < 0:
                del lista_nuvens[contador_nuvem]           
            contador_nuvem += 1

    #draw 
    screen.fill((56, 176, 222))
    print(len(group))

    for nuvem in lista_nuvens:
        pygame.draw.rect(screen, (255, 255, 255), nuvem[0])
 
    for cactu in lista_cactus:
        pygame.draw.rect(screen, (49, 79, 49), cactu)

    pygame.draw.rect(screen, (153, 204, 50), chao)
    pontuacao = fonte.render(f'Score: {pontos}',1,(0, 0, 0))
    screen.blit(pontuacao, (0, 0))

    for dino in group:
        dino.draw(screen,color=dino.color)
    
    pygame.display.update()
    

pygame.quit()
