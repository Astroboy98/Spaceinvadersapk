
import sys
sys.path.append("modules") 
import thread
import time
import random

import pygame
from pygame.locals import *



class Callable:
    def __init__(self, anycallable):
        self.__call__ = anycallable
    
class Video:
    SCREEN = None
    FULLSCREEN = None
    def SetDisplay(self, Width, Height, FullScreen):
        #Set tamanio pantalla
        if FullScreen == False:
            self.SCREEN = pygame.display.set_mode((Width, Height), DOUBLEBUF)
            self.FULLSCREEN = False
        else:
            self.SCREEN = pygame.display.set_mode((Width, Height), FULLSCREEN | DOUBLEBUF)
            self.FULLSCREEN = True

        #Set Nombre ventana
        pygame.display.set_caption("Invasores del Espacio - Joel Juarez")

        #llena pantalla con color negro
        self.SCREEN.fill((0,0,0))
        
        #actualiza pantalla
        pygame.display.flip()

    def getFullscreen(self):
        #retorna el valor de pantalla completa
        return self.FULLSCREEN

class FPS:
    FRAMES_PER_SEC = None
    CLOCK = None
    def __init__(self):
        #Fija variables
        self.FRAMES_PER_SEC = 60
        self.CLOCK = pygame.time.Clock()

    def Tick(self):
        #Ajusta el timer en fps
        return self.CLOCK.tick(self.FRAMES_PER_SEC)

class AlienType:
    
    def Type0(self):
        return -1
    
    #Tipo de alien 1
    def Type1(self):
        return 0
    
    #Tipo de alien 2
    def Type2(self):
        return 1
    
    #Tipo de alien 3
    def Type3(self):
        return 2
    
    #Alien nodriza
    def MotherShip(self):
        return 3

    #Setup Static Methods
    Type0 = Callable(Type0)
    Type1 = Callable(Type1)
    Type2 = Callable(Type2)
    Type3 = Callable(Type3)
    MotherShip = Callable(MotherShip)

class EnemyManagement:
    
    NUM_ACROSS = 11
    NUM_ROWS = 5
    
    ENEMY_LIST = []
    
    tmpSurface = pygame.Surface(((NUM_ACROSS*45),(NUM_ROWS*45)))
    tmpSurface.set_colorkey((0,0,0))
    tmpSurface.fill(tmpSurface.get_colorkey())

    #Moviemiento aumenta cuando baja 
    MOVEMENT = "INCREASE"
    MoveX = 0
    MoveY = 0

##################################
    class EnemyAlien:
        HEALTH = None
        TYPE = None
        SPRITE = None
        FRAME = None
        XPOS = None
        YPOS = None
        STOP_THREADS = None

        FIRE_SPRITE = None
        FIRE_XPOS = None
        FIRE_YPOS = None
        FIRE_SPEED = None
        FIRE_DISPLAY = None
    
        def __init__(self, Health, Type):
            #Pone variables
            self.HEALTH = Health
            self.TYPE = Type
            self.SPRITE = []
            self.FRAME = 0
            self.STOP_THREADS = False
            
            if self.TYPE == AlienType.Type0:
                tmpSurface = pygame.Surface((27,20))
                tmpSurface.fill((0,0,0))
                self.SPRITE.append(tmpSurface)
                self.SPRITE.append(tmpSurface)
                                   
            elif self.TYPE == AlienType.Type1:
                self.SPRITE.append(pygame.image.load("data/images/Alien1a.png"))
                self.SPRITE.append(pygame.image.load("data/images/Alien1b.png"))
                 
            elif self.TYPE == AlienType.Type2:
                self.SPRITE.append(pygame.image.load("data/images/Alien2a.png"))
                self.SPRITE.append(pygame.image.load("data/images/Alien2b.png"))
                
            elif self.TYPE == AlienType.Type3:
                self.SPRITE.append(pygame.image.load("data/images/Alien3a.png"))
                self.SPRITE.append(pygame.image.load("data/images/Alien3b.png"))
                
            elif self.TYPE == AlienType.MotherShip:
                self.SPRITE.append(pygame.image.load("data/images/Mothership.png"))
                self.SPRITE.append(pygame.image.load("data/images/Mothership.png"))
            else:
                self.SPRITE = None
                print "[Error]: Enemy Alien type was not set correctly!"
                sys.exit(0)
            self.XPOS = 0
            self.YPOS = 0

            self.FIRE_SPRITE = pygame.image.load("data/images/Missile_Alien.png")
            self.FIRE_XPOS = self.XPOS
            self.FIRE_YPOS = self.YPOS
            self.FIRE_SPEED = 4
            self.FIRE_DISPLAY = False

        def Fire(self):
            #Funcion de disparo
            if self.TYPE != AlienType.Type0:
                #Se asegura que no estamos disparando
                if self.FIRE_DISPLAY == False:
                    #ACtualiza varibale
                    self.FIRE_XPOS = self.XPOS
                    self.FIRE_YPOS = self.YPOS

                    
                    self.FIRE_DISPLAY = True
                

        def Animate_Thread(self): 
            #Actualiza framde de animacion
            while self.STOP_THREADS == False:
                if self.FRAME == 0:
                    self.FRAME = 1
                elif self.FRAME == 1:
                    self.FRAME = 0

                
                time.sleep(0.3)

        def Render(self):
            
            EnemyManagement.tmpSurface.blit(self.SPRITE[self.FRAME], (self.XPOS, self.YPOS))
        
        def getHP(self):
            
            return self.HEALTH
    
        def getType(self):
            
            return self.TYPE

        def getX(self):
            
            return self.XPOS

        def getY(self):
            
            return self.YPOS

        def setX(self, xpos):
            
            self.XPOS = xpos

        def setY(self, ypos):
            
            self.YPOS = ypos

        def setType(self, Type):
            
            self.TYPE = Type

        def stopThreads(self):
            
            self.STOP_THREADS = False
##################################
            

    def __init__(self):
        
        self.ENEMY_LIST = []

    def Generate(self):
        
        for i in range(0, self.NUM_ROWS):             
          
            for i2 in range(0, self.NUM_ACROSS):
                
                if i == 0:
                    tmpEnemy = self.EnemyAlien(100, AlienType.Type1)
                    self.ENEMY_LIST.append(tmpEnemy)
                    tmpEnemy = None #Garbage Collection
                elif i == 1 or i == 2:
                    tmpEnemy = self.EnemyAlien(100, AlienType.Type2)
                    self.ENEMY_LIST.append(tmpEnemy)
                    tmpEnemy = None #Garbage Collection
                elif i == 3 or i == 4:
                    tmpEnemy = self.EnemyAlien(100, AlienType.Type3)
                    self.ENEMY_LIST.append(tmpEnemy)
                    tmpEnemy = None #Garbage Collection

        
        for i in range(0, len(self.ENEMY_LIST)):
            #Inicia animacion
            thread.start_new_thread(self.ENEMY_LIST[i].Animate_Thread, ())

    def Render(self):
        #Sigue el rastro de columna y fila
        currentRow = 0
        currentAcross = 0

        
        for i in range(0, len(self.ENEMY_LIST)):
            #pone lugar en x y a alientype
            self.ENEMY_LIST[i].setX((currentAcross * (27+13)))
            self.ENEMY_LIST[i].setY((currentRow * (20+13)))
            
            
            #Renderiza el alien
            self.ENEMY_LIST[i].Render()
            
            #Actualiza posicion de enemigos cuando se mueven
            self.ENEMY_LIST[i].setX(self.ENEMY_LIST[i].getX() + self.MoveX)
            self.ENEMY_LIST[i].setY(self.ENEMY_LIST[i].getY() + self.MoveY)
            
            
            if currentAcross < self.NUM_ACROSS:
                currentAcross += 1 

                
                if currentAcross == self.NUM_ACROSS:
                   
                    currentAcross = 0

                    
                    currentRow += 1

            #Renderiza misiles
            if self.ENEMY_LIST[i].FIRE_DISPLAY == True:
                
                pygame.display.get_surface().blit(self.ENEMY_LIST[i].FIRE_SPRITE, (self.ENEMY_LIST[i].FIRE_XPOS, self.ENEMY_LIST[i].FIRE_YPOS))

                #Actualiza la posicion del misil enemigo
                if self.ENEMY_LIST[i].FIRE_YPOS < 450:
                    self.ENEMY_LIST[i].FIRE_YPOS += self.ENEMY_LIST[i].FIRE_SPEED
                else:
                    self.ENEMY_LIST[i].FIRE_DISPLAY = False
                    
        
        pygame.display.get_surface().blit(self.tmpSurface, (self.MoveX, self.MoveY))

        #Mueve los enemigos hacia abajo
        if self.MOVEMENT == "INCREASE":
            if self.MoveX < 350:
                self.MoveX += 0.5
            else:
                self.MoveY += (20+13)
                self.MOVEMENT = "DECREASE"
                
        if self.MOVEMENT == "DECREASE":
            if self.MoveX > 0:
                self.MoveX -=  0.5
            else:
                self.MoveY += (20+13)
                self.MOVEMENT = "INCREASE"

        
            
    def Kill(self, ID):
        self.ENEMY_LIST[ID] = self.EnemyAlien(0, AlienType.Type0)

class Player:
    SPRITE = None
    HEALTH = None
    XPOS = None
    YPOS = None
    MOVE_SPEED = None
    LIFE = None
    SCORE = None
    
    FIRE_SPRITE = None
    FIRE_DISPLAY = None
    FIRE_XPOS = None
    FIRE_YPOS = None
    FIRE_SPEED = None

    def __init__(self):
        
        self.SPRITE = pygame.image.load("data/images/Player.png")
        self.HEALTH = 100
        self.XPOS = 400
        self.YPOS = 450
        self.MOVE_SPEED = 4
        self.LIFE = 3 #3 Lives
        self.SCORE = 0

        self.FIRE_SPRITE = pygame.image.load("data/images/Missile_Player.png")
        self.FIRE_DISPLAY = False
        self.FIRE_XPOS = self.XPOS + (self.SPRITE.get_width() / 2)
        self.FIRE_YPOS = self.YPOS
        self.FIRE_SPEED = 6

    def MoveRight(self):
        #Mueve el jugador a la derecha
        self.XPOS += self.MOVE_SPEED

    def MoveLeft(self):
        #Mueve el jugador a la izquierda
        self.XPOS -= self.MOVE_SPEED

    def Fire_Thread(self):

        #FPS
        fps = FPS()
        
        while (self.FIRE_DISPLAY == True) and (-1*(self.FIRE_YPOS) < 0):
            #Actualiza posicion del disparo
            self.FIRE_YPOS -= self.FIRE_SPEED
            
            fps.Tick()
            
            
        self.FIRE_DISPLAY = False
        self.FIRE_XPOS = self.XPOS + (self.SPRITE.get_width() / 2)
        self.FIRE_YPOS = self.YPOS

    def Fire(self):
        
        if self.FIRE_DISPLAY != True:
            
            self.FIRE_XPOS = self.XPOS+ (self.SPRITE.get_width() / 2)
            self.FIRE_YPOS = self.YPOS

            self.FIRE_DISPLAY = True

            
            thread.start_new_thread(self.Fire_Thread, ())

    def Render(self):
        
        pygame.display.get_surface().blit(self.SPRITE, (self.XPOS, self.YPOS))
        if self.FIRE_DISPLAY == True:
            pygame.display.get_surface().blit(self.FIRE_SPRITE, (self.FIRE_XPOS, self.FIRE_YPOS))
        

#Variables de juego
START_GAME = False
GAME_OVER = False

#DEfine clases
video = Video()
fps = FPS()
enemy_man = EnemyManagement()
player = Player()

#Inicia pygame
pygame.init()

#ESconde puntero
pygame.mouse.set_visible(0)

#Deja esccribir
pygame.key.set_repeat(10,10)

#define video res
video.SetDisplay(800, 600, False)

#genera lista de enemigos
enemy_man.Generate()

#fuente
Player_Info_Font = pygame.font.Font("data/fonts/VeraMoBd.ttf", 14)
GameOver_Font = pygame.font.Font("data/fonts/VeraMoBd.ttf", 20)

#Decide que enemigo dispara
def EnemyFire_Monitor():
    
    Old_Rnd = 0
    Enemy_Can_Fire = [] 
    while True:
        for i in range(1, len(enemy_man.ENEMY_LIST)):
            try:
                
                if enemy_man.ENEMY_LIST[i + enemy_man.NUM_ACROSS].TYPE == AlienType.Type0:
                    
                    Enemy_Can_Fire.append(int(i))
            except: 
                
                Enemy_Can_Fire.append(int(i))

            #aleatoriente decide quien dispara
            try:
                
                Rnd = random.randrange(int(min(Enemy_Can_Fire)), int(max(Enemy_Can_Fire)))

                #El mismo enemigo no puede disparar
                if Rnd != Old_Rnd:
                    
                    Old_Rnd = Rnd

                    
                    enemy_man.ENEMY_LIST[Rnd].Fire()

                    
                    break
                else:
                    
                    Rnd = random.randrange(int(min(Enemy_Can_Fire)), int(max(Enemy_Can_Fire)))
            except:
                
                None

        
        Enemy_Can_Fire = None
        Enemy_Can_Fire = []
        
        time.sleep(1)


thread.start_new_thread(EnemyFire_Monitor, ())


Loop_Count = 0 
Loop_Count_GameOver = 0 
while 1:
   
        
    if START_GAME == True and GAME_OVER == False:
        #Actualiza las vidas del jugador
        if player.LIFE <= 0:
            #Cuado no quedan vidas el juego acaba
            GAME_OVER = True

        #FPS
        fps.Tick()
    
        #Eventos
        for event in pygame.event.get():
            #Keydown
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == K_RIGHT:
                    player.MoveRight()
                if event.key == K_LEFT:
                    player.MoveLeft()
                if event.key == K_SPACE:
                    player.Fire()
                if event.key == K_BACKSLASH:
                    if video.getFullscreen() == False:
                        video.SetDisplay(800, 600, True)
                    else:
                        video.SetDisplay(800, 600, False)

                

        #actualiza colision de misil
        for i in range(0, len(enemy_man.ENEMY_LIST)):
            
            if enemy_man.ENEMY_LIST[i].getType() != AlienType.Type0:
                if(player.FIRE_SPRITE.get_rect( center=(player.FIRE_XPOS, player.FIRE_YPOS) ).colliderect\
                   (enemy_man.ENEMY_LIST[i].SPRITE[enemy_man.ENEMY_LIST[i].FRAME].get_rect\
                    ( center=(enemy_man.ENEMY_LIST[i].getX(), enemy_man.ENEMY_LIST[i].getY()) ))) == True:
            
                    
                    player.FIRE_DISPLAY = False 

                    #ACtualiza puntuacion
                    if enemy_man.ENEMY_LIST[i].getType() == AlienType.Type1:
                        player.SCORE += 50
                    elif enemy_man.ENEMY_LIST[i].getType() == AlienType.Type2:
                        player.SCORE += 40
                    elif enemy_man.ENEMY_LIST[i].getType() == AlienType.Type3:
                        
                        index = random.randrange(0,10)
                        if index <= 5:
                            player.SCORE += 20
                        else:
                            player.SCORE += 30     
                    elif enemy_man.ENEMY_LIST[i].getType() == AlienType.MotherShip:
                        player.SCORE += 250

                    enemy_man.Kill(i) #mata un enemigo golpeado

                    
                    break

        #actualiza colision de misil enemigo
        for i in range(0, len(enemy_man.ENEMY_LIST)):
            if(enemy_man.ENEMY_LIST[i].FIRE_SPRITE.get_rect(center=(enemy_man.ENEMY_LIST[i].FIRE_XPOS, enemy_man.ENEMY_LIST[i].FIRE_YPOS) ).colliderect\
                (player.SPRITE.get_rect(center=(player.XPOS, player.YPOS)))) == True:

                    if enemy_man.ENEMY_LIST[i].FIRE_DISPLAY == True:
                        #saca una vida a jugador
                        player.LIFE -= 1

                    
                    enemy_man.ENEMY_LIST[i].FIRE_DISPLAY = False
                    enemy_man.ENEMY_LIST[i].FIRE_XPOS = 0
                    enemy_man.ENEMY_LIST[i].FIRE_YPOS = 0

                    
                    break
                
        #limpia pantalla
        video.SCREEN.fill((0,0,0))

        
        enemy_man.Render()
        player.Render()

        
        Score_Str = "Puntaje: " + str(player.SCORE)
        Score_Surface = Player_Info_Font.render(str(Score_Str), False, (255,255,255))
        Life_Str = "Vidas: x" + str(player.LIFE)
        Life_Surface = Player_Info_Font.render(str(Life_Str), False, (255,255,255))
        for i in range(0, int(player.LIFE)):
            
            pygame.display.get_surface().blit(player.SPRITE, (90 + (i*(player.SPRITE.get_width()+10)), 548))
    
        pygame.draw.line(pygame.display.get_surface(), (0,255,0), (0, 500), (900, 500), 2)
        pygame.display.get_surface().blit(Score_Surface, (10, 500))
        pygame.display.get_surface().blit(Life_Surface, (10, 550))

        #actualiza pantalla
        pygame.display.flip()

    #cosas de menu

    elif START_GAME == False:
        if Loop_Count < 1:
            Menu_Logo = pygame.image.load("data/images/Logo.png")
            Start_Game_Text = Player_Info_Font.render("Presiona enter para empezar", False, (0,255,0))
            Exit_Game_Text = Player_Info_Font.render("Presiona ESC para salir", False, (255,0,0))
            video.SetDisplay(420, 400, False)
        
            #FPS
            fps.Tick()
        
        #eventos
        for event in pygame.event.get():
            #Keydown
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == K_RETURN:
                    START_GAME = True
                    video.SetDisplay(800, 600, video.getFullscreen())
                    break
                if event.key == K_BACKSLASH:
                    if video.getFullscreen() == False:
                        video.SetDisplay(420, 400, True)
                        Loop_Count = 0 
                    else:
                        video.SetDisplay(420, 400, False)
                        Loop_Count = 0 

        pygame.display.get_surface().blit(Menu_Logo, (0,0))
        pygame.display.get_surface().blit(Start_Game_Text, (10,250))
        pygame.display.get_surface().blit(Exit_Game_Text, (10,300))

        if Loop_Count < 1:
            #actualiza screen
            pygame.display.flip()

    #JUEGO TERMINADP
    elif GAME_OVER == True:
        if Loop_Count_GameOver < 1:
            
            GameOver_Image = pygame.image.load("data/images/GameOver.png")
            Score_Str = str(player.SCORE)
            Score_Surface = Player_Info_Font.render(str(Score_Str), False, (255,255,255))
            Life_Str = str(player.LIFE)
            Life_Surface = Player_Info_Font.render(str(Life_Str), False, (255,255,255))

        #FPS
        fps.Tick()

        #EventOs
        for event in pygame.event.get():
            #Keydown
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == K_BACKSLASH:
                    if video.getFullscreen() == False:
                        video.SetDisplay(800, 600, True)
                        Loop_Count_GameOver = 0
                    else:
                        video.SetDisplay(800, 600, False)
                        Loop_Count_GameOver = 0


        enemy_man.Render()
        video.SCREEN.fill((0,0,0))
        
        
        pygame.display.get_surface().blit(GameOver_Image, (0,0))
        pygame.display.get_surface().blit(Score_Surface, (425, 344))
        pygame.display.get_surface().blit(Life_Surface, (425, 382))
        pygame.display.get_surface().blit(enemy_man.tmpSurface, (0,65))

        
        pygame.display.flip()

        if Loop_Count_GameOver < 1:
            pygame.display.flip()

        
        Loop_Count_GameOver += 1

    ##################################
    Loop_Count += 1 