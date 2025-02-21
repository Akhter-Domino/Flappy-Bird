import random
import sys
import pygame
from pygame.locals import *

fps = 28
screenWidth = 289
screenHeight = 511
screen = pygame.display.set_mode((screenWidth, screenHeight))
groundY = screenHeight * 0.8
gameSprites = {}
gameSounds = {}

player = 'Assets/Images/bird.png'
background = 'Assets/Images/background.png'
pipe = 'Assets/Images/pipe.png'

def welcomeScreen():
    playerX = int(screenWidth/5)
    playerY = int((screenHeight - gameSprites['player'].get_height())/2)
    messageX = int((screenWidth - gameSprites['message'].get_width())/2) 
    messageY = int(screenHeight * 0.13)
    baseX = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            
            else:
                screen.blit(gameSprites['background'], (0,0))
                screen.blit(gameSprites['player'], (playerX, playerY))
                screen.blit(gameSprites['message'], (messageX, messageY))
                screen.blit(gameSprites['base'], (baseX, groundY))
                
                pygame.display.update() 
                fpsClock.tick(fps)


def game():
    score = 0
    playerX = int(screenWidth/5)
    playerY = int(screenHeight/2)
    baseX = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': screenWidth + 200, 'y': newPipe1[0]['y']},
        {'x': screenWidth + 200 + (screenWidth/2), 'y': newPipe2[0]['y']}
    ]

    lowerPipes = [
        {'x': screenWidth + 200, 'y': newPipe1[1]['y']},
        {'x': screenWidth + 200 + (screenWidth/2), 'y': newPipe2[1]['y']}
    ]

    pipeVelX = -4
    playerVelY = -4
    playerMaxVelY = 9
    playerMinVelY = -9
    playerAccY = 1

    playerFlapVel = -8
    playerFlapp = False 

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    playerVelY = playerFlapVel
                    playerFlapp = True 
                    gameSounds['wing'].play()

        crashTest = isCollide(playerX, playerY, upperPipes, lowerPipes)
        if crashTest:
            return
        
        playerMidPos = playerX + gameSprites['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + gameSprites['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                score += 1
                print(f"Your Score is {score}")
                gameSounds['point'].play()

        if playerVelY < playerMaxVelY and not playerFlapp:
            playerVelY += playerAccY

        if playerFlapp:
            playerFlapp = False

        playerHeight = gameSprites['player'].get_height()
        playerY = playerY + min(playerVelY, groundY - playerY - playerHeight)

        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < upperPipes[0]['x'] < 5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        if upperPipes[0]['x'] < -gameSprites['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        screen.blit(gameSprites['background'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            screen.blit(gameSprites['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(gameSprites['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(gameSprites['base'], (baseX, groundY))
        screen.blit(gameSprites['player'], (playerX, playerY))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += gameSprites['numbers'][digit].get_width()
        Xoffset = (screenWidth - width)/2

        for digit in myDigits:
            screen.blit(gameSprites['numbers'][digit], (Xoffset, screenHeight*0.12))
            Xoffset += gameSprites['numbers'][digit].get_width()
        pygame.display.update()
        fpsClock.tick(fps)

def isCollide(playerX, playerY, upperPipes, lowerPipes):
    if playerY > groundY - 25 or playerY < 0:
        gameSounds['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = gameSprites['pipe'][0].get_height()
        if (playerY < pipeHeight + pipe['y'] and abs(playerX - pipe['x']) < gameSprites['pipe'][0].get_width()):
            gameSounds['hit'].play()
            return True
    for pipe in lowerPipes:
        if (playerY + gameSprites['player'].get_height() > pipe['y']) and abs(playerX - pipe['x']) < gameSprites['pipe'][0].get_width():
            gameSounds['hit'].play()
            return True

    return False

def getRandomPipe():
    pipeHeight = gameSprites['pipe'][0].get_height()
    offset = screenWidth/2
    y2 = offset + random.randrange(0, int(screenHeight - gameSprites['base'].get_height() - 1.2 * offset))
    y1 = pipeHeight - y2 + offset
    pipeX = screenWidth + 10
    pipe = [
        {'x': pipeX, 'y': -y1},
        {'x': pipeX, 'y': y2}
    ]   
    return pipe

if __name__ == "__main__":
    pygame.init()
    fpsClock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by AkhterDomino')

    gameSprites['numbers'] = (
        pygame.image.load('Assets/Images/0.png').convert_alpha(),
        pygame.image.load('Assets/Images/1.png').convert_alpha(),
        pygame.image.load('Assets/Images/2.png').convert_alpha(),
        pygame.image.load('Assets/Images/3.png').convert_alpha(),
        pygame.image.load('Assets/Images/4.png').convert_alpha(),
        pygame.image.load('Assets/Images/5.png').convert_alpha(),
        pygame.image.load('Assets/Images/6.png').convert_alpha(),
        pygame.image.load('Assets/Images/7.png').convert_alpha(),
        pygame.image.load('Assets/Images/8.png').convert_alpha(),
        pygame.image.load('Assets/Images/9.png').convert_alpha(),
    )

    gameSprites['message'] = pygame.image.load('Assets/Images/message.png')
    gameSprites['base'] = pygame.image.load('Assets/Images/floor.png').convert_alpha()
    gameSprites['pipe'] = (
        pygame.transform.rotate(pygame.image.load(pipe).convert_alpha(), 180),
        pygame.image.load(pipe).convert_alpha()
    )

    gameSounds['wing'] = pygame.mixer.Sound('Assets/Sounds/wing.wav')
    gameSounds['point'] = pygame.mixer.Sound('Assets/Sounds/point.wav')
    gameSounds['hit'] = pygame.mixer.Sound('Assets/Sounds/hit.wav')

    gameSprites['background'] = pygame.image.load(background).convert()
    gameSprites['player'] = pygame.image.load(player).convert_alpha()

    while True:
        welcomeScreen()
        game()