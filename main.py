import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 500
SCREENHEIGHT = 500
SCREEN = pygame.display.set_mode(( SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT*0.9
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER ='images/bird.png'
BACKGROUND ='images/bg.jpg'
PIPE ='images/pipe.png'

def welcomeScreen():

    playerx=int(SCREENWIDTH/5)
    playery=int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex=int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey=int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type==KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'], (0, 0))
                SCREEN.blit(GAME_SPRITES['player'], (playerx,playery ))
                SCREEN.blit(GAME_SPRITES['message'], (messagex,messagey ))
                SCREEN.blit(GAME_SPRITES['base'], (basex, GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes= [
        {'x': SCREENWIDTH+200, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[0]['y']}
    ]
    lowerPipes= [
        {'x': SCREENWIDTH+200, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+200+(SCREENWIDTH/2), 'y':newPipe2[1]['y']}
    ]

    pipeVelX = -4

    playerVely= -9
    playerMaxVely= 10
    playerMinVely= -8
    playerAccy= 1

    playerFlapAccv= -8
    playerFlapped= False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key==K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key==K_SPACE or event.key==K_UP):
                if playery>0:
                    playerVely = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['wings'].play()

        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
        if crashTest:
            return 

        playerMidPos= playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos+4:
                score +=1
                print(f"Your score is {score}")            
                GAME_SOUNDS['point'].play()

        if playerVely <playerMaxVely and not playerFlapped:
            playerVely += playerAccy
        if playerFlapped:
            playerFlapped=False
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVely, GROUNDY - playery - playerHeight)

        for upperPipe, lowePipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelX
            lowePipe['x'] =+ pipeVelX
        
        if 0<upperPipes[0]['x']<5:
            newPipe=getRandomPipe()
            upperPipes.append(newPipe[0])
            lowerPipes.append(newPipe[1])


        if upperPipes[0]['x']< -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe, lowePipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowePipe['x'],lowePipe['y']))

        SCREEN.blit(GAME_SPRITES['base'], (basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'], (playerx,playery))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digits in myDigits:
            width += GAME_SPRITES['numbers'][digits].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery<pipeHeight+pipe['y'] and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
    for pipe in lowerPipes:
        if (playery+GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx-pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            pass
    return False

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2= offset + random.randrange(0, int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipex = SCREENWIDTH +10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipex, 'y': -y1},
        {'x': pipex, 'y': y2}
    ]
    return pipe

if __name__ == "__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha(),
    )

GAME_SPRITES['message'] =pygame.image.load('images/msg.webp').convert_alpha()
GAME_SPRITES['base'] =pygame.image.load('images/base.webp').convert_alpha()
GAME_SPRITES['pipe'] =((pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180)),
   (pygame.image.load(PIPE).convert_alpha())
)

GAME_SOUNDS['die']= pygame.mixer.Sound('sounds/die.mp3')
GAME_SOUNDS['swoosh']= pygame.mixer.Sound('sounds/swoosh.mp3')
GAME_SOUNDS['hit']= pygame.mixer.Sound('sounds/hit.mp3')
GAME_SOUNDS['wings']= pygame.mixer.Sound('sounds/wings.mp3')
GAME_SOUNDS['point']= pygame.mixer.Sound('sounds/point.mp3')

GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()

while True:
    welcomeScreen()
    mainGame()
 