import pygame , sys
from numpy import random

pygame.mixer.init(44100, -16,2,2048)
pygame.init()

screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
gameFont = pygame.font.Font('04B_19.TTF',30)
font2 = pygame.font.Font('04B_19.TTF',20)

bgImage = pygame.image.load('assets/background-day.png').convert()
baseSurface = pygame.image.load('assets/base.png').convert()
birdImages = [pygame.image.load('assets/bluebird-downflap.png').convert_alpha(),pygame.image.load('assets/bluebird-midflap.png').convert_alpha(),pygame.image.load('assets/bluebird-upflap.png').convert_alpha()]
pipeImage = pygame.image.load('assets/pipe-green.png').convert()
pipeHeights = [150,175,200,225,250,275,300,325,350,375,400,425,450]
birdImageNum = 0
birdImage = birdImages[birdImageNum]
birdRect = birdImage.get_rect(center = (50,256))
gameOverImage = pygame.image.load('assets/gameover.png')
startImage = pygame.image.load('assets/message.png')

SPAWNPIPE = pygame.USEREVENT
SPAWNFLAP = pygame.USEREVENT + 1

base_x_pos = 0
gravity = 0.065
birdMovement = 0
pipeList = []
pygame.time.set_timer(SPAWNPIPE,1200)
pygame.time.set_timer(SPAWNFLAP,200)
score = 0
highScore = 0
gameActive = True

flapSound = pygame.mixer.Sound('sound/sfx_wing.wav')
flapSound.set_volume(0.2)
scoreSound = pygame.mixer.Sound('sound/sfx_point.wav')
scoreSound.set_volume(0.05)
collisionSound = pygame.mixer.Sound('sound/sfx_die.wav')


def drawBase():
    screen.blit(baseSurface , (base_x_pos,450))
    screen.blit(baseSurface , (base_x_pos+288,450))







def scoreDisplay():
    if not gameActive:
        highScoreSurface = gameFont.render('High Score : '+str(int(highScore)),True , (255,255,255))
        highScoreRect = highScoreSurface.get_rect(center = (144,155))
        screen.blit(highScoreSurface,highScoreRect)

        restartSurface = font2.render('Press Spacebar to restart',True , (0,0,0))
        restartRect = restartSurface.get_rect(center = (144,490))
        screen.blit(restartSurface,restartRect)

    scoreSurface = gameFont.render('Score : ' + str(int(score)) , True , (255,255,255))
    scoreRect = scoreSurface.get_rect(center = (144,50))
    screen.blit(scoreSurface,scoreRect)







def createPipe():
    height = random.choice(pipeHeights)
    bottomPipe = pipeImage.get_rect(midtop = (315,height))
    topPipe = pipeImage.get_rect(midbottom = (315,height-160))
    return bottomPipe,topPipe

def movePipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 2
    return pipes

def drawPipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 462:
            screen.blit(pipeImage,pipe)
        else:
            flipImage = pygame.transform.flip(pipeImage,False,True)
            screen.blit(flipImage,pipe)







def detectCollision(pipeRects):
    for pipeRect in pipeRects:
        if birdRect.colliderect(pipeRect):
            print("collision detected")
            collisionSound.play()
            return True
    if birdRect.top <= 0 or birdRect.bottom >= 450:
        print("collision detected")
        collisionSound.play()
        return True
    return False

def rotateBird(birdImage):
    rotatedImage = pygame.transform.rotozoom(birdImage , -birdMovement*9,1)
    return rotatedImage

def birdAnimation():
    newBird = birdImages[birdImageNum]
    newBirdRect =  newBird.get_rect(center = (50,birdRect.centery))
    return newBird,newBirdRect








start = False




while True:
    while not start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Start")
                    start = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    start = True

        screen.blit(bgImage,(0,0))
        screen.blit(startImage,(52,30))

        startSurface = font2.render('Press Spacebar or',True , (255,255,255))
        startRect = startSurface.get_rect(center = (144,390))
        screen.blit(startSurface,startRect)

        startSurface1 = font2.render('right click to start',True , (255,255,255))
        startRect1 = startSurface1.get_rect(center = (144,413))
        screen.blit(startSurface1,startRect1)

        pygame.display.update()
        clock.tick(120)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and gameActive:
                    flapSound.play()
                    birdMovement-=0
                    birdMovement -= 4.5
                if event.key == pygame.K_SPACE and not gameActive:
                    gameActive = True
                    score = 0
                    pipeList.clear()
                    birdRect.center = (50,256)
                    birdMovement = 0;
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and gameActive:
                    flapSound.play()
                    birdMovement-=0
                    birdMovement -= 4.5
                if event.button == 1 and not gameActive:
                    gameActive = True
                    score = 0
                    pipeList.clear()
                    birdRect.center = (50,256)
                    birdMovement = 0;
            if event.type == SPAWNPIPE:
                pipeList.extend(createPipe())
                if gameActive:
                    scoreSound.play()
                    score+=1
            if event.type == SPAWNFLAP:
                if birdImageNum <  2:
                    birdImageNum+=1
                else:
                    birdImageNum = 0

        birdImage,birdRect = birdAnimation()
        screen.blit(bgImage,(0,0))

        if gameActive:
            pipeList = movePipes(pipeList)
            drawPipes(pipeList)
            base_x_pos-=1
            drawBase()
            if base_x_pos == -288:
                base_x_pos = 0

            birdMovement+=gravity
            rotatedBird = rotateBird(birdImage)
            birdRect.centery += birdMovement
            screen.blit(rotatedBird,birdRect)
            scoreDisplay()

            gameActive = not detectCollision(pipeList)
        else:
            drawPipes(pipeList)
            drawBase()
            screen.blit(birdImages[1],birdRect)
            scoreDisplay()
            screen.blit(gameOverImage,(48,240))


        if score>highScore:
            highScore = score


        pygame.display.update()
        clock.tick(120)
