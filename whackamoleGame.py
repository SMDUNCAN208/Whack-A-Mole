import pygame, random, sys
from pygame.locals import *
from pygame.sprite import *

pygame.init()

#Dimensions
windowWidth = 1200
windowHeight = 950
base = 150
catHeight = 185
catWidth = 130
birdHeight = 250
heartHeight = 30

#Colours
green      = ( 31, 112,  21)
blue       = ( 54, 195, 255)
brown      = (122,  87,  18)
lightBrown = (255, 199,  86)
otherBrown = (230, 195, 124)

#Fonts
fontObjFifty = pygame.font.Font('freesansbold.ttf', 50)
fontObjThirty = pygame.font.Font('freesansbold.ttf', 30)

#Music
audioOne = pygame.mixer.Sound("ScreamingBird.wav")
audioTwo = pygame.mixer.Sound("Seagulls.wav")
audioThree = pygame.mixer.Sound("AngryBirds.wav")
audioFour = pygame.mixer.Sound("WoodBirds.wav")
audioFive = pygame.mixer_music.load('CrazyLaPaint.mp3')
pygame.mixer.init(channels = 8)

#Birds and cat
birds = pygame.sprite.Group()
cat = pygame.sprite.Group()
pastX = 0
pastY = 0

SCREEN = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Birds')

class Bird(pygame.sprite.Sprite):
    def __init__ (self):
        super().__init__()
        birdImage = pygame.image.load("bird.png")
        self.image = pygame.Surface((250,250))
        self.image = pygame.transform.scale(birdImage, (birdHeight, birdHeight)).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, x, y):
        self.rect.x = x
        self.rect.y = y

class Cat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        catImage = pygame.image.load("catOne.png")
        self.image = pygame.Surface((catWidth, catHeight))
        self.image = pygame.transform.scale(catImage, (catWidth, catHeight)).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, centre):
        self.rect.center = centre

def main() :
    global points
    points = 0
    lives = 5
    time_difference = 0

    channelNum = 0
    changed = False
    paused = False
    beenThere = False
    ranOnce = False
    started = False
    goodMusic = False
    musicStarted = False

    clock = pygame.time.Clock()
    now = pygame.time.get_ticks()

    newBird = Bird()
    newBird.rect.x = random.randint(0, windowWidth - birdHeight)
    newBird.rect.y = random.randint(0, windowHeight - base - birdHeight)
    birds.add(newBird)

    newCat = Cat()
    newCat.rect.x = windowWidth / 2
    newCat.rect.y = (windowHeight - base) / 2
    cat.add(newCat)
    calculatedTime = 20000

    catPos = (windowWidth / 2, (windowHeight - base) / 2)
    drawBoard(catPos)

    screenTwo = pygame.Surface((windowWidth, windowHeight - base))
    screenTwo.set_alpha(150)
    screenTwo.fill((0, 0, 0))

    SCREEN.blit(screenTwo, (0, 0))

    spaceText = fontObjFifty.render("Press 'space' to start with bird sounds", True, lightBrown, None)
    SCREEN.blit(spaceText, ((windowWidth - spaceText.get_width()) / 2, (windowHeight - base - 105) / 2))
    spaceText = fontObjThirty.render("Press the up arrow to start with music", True, lightBrown, None)
    SCREEN.blit(spaceText, ((windowWidth - spaceText.get_width()) / 2, (windowHeight - base) / 2))
    pygame.display.update()

    while True:
        if started == True:
            if musicStarted == False and goodMusic == True:
                pygame.mixer_music.play(-1, 0.0)
                musicStarted = True
            if lives != 0 :
                if changed == True:
                    if 20000 - (points * 10 ) <= 1000 :
                        calculatedTime = 1000
                    else :
                        calculatedTime = 20000 - (points * 20)
                    changed = False
                    now = pygame.time.get_ticks()

                if paused == False:
                    time_difference = calculatedTime - (pygame.time.get_ticks() - now)

                for event in pygame.event.get():
                    if event.type == MOUSEMOTION and paused == False:
                        mouseX, mouseY = event.pos
                        if mouseY <= windowHeight - base - (catHeight / 2) and mouseY >= catHeight / 2 and mouseX <= windowWidth - (catWidth / 2) and mouseX >= catWidth / 2:
                            pygame.mouse.set_visible(False)
                            mousePos = pygame.mouse.get_pos()
                            moveCat(mousePos)
                        elif mouseY > windowHeight - base:
                            pygame.mouse.set_visible(True)
                    if event.type == MOUSEBUTTONUP and paused == False:
                        changed = True
                        if pygame.sprite.groupcollide(birds, cat, False, False):
                            calculatePoints(True, True)

                            if goodMusic == False :
                                soundNum = random.randint(0, 3)
                                if soundNum == 0:
                                    pygame.mixer.Channel(channelNum).play(audioOne, loops = 0, maxtime = 2000)
                                elif soundNum == 1:
                                    pygame.mixer.Channel(channelNum).play(audioTwo, loops = 0, maxtime = 3000)
                                elif soundNum == 2 :
                                    pygame.mixer.Channel(channelNum).play(audioThree, loops = 0, maxtime = 3000)
                                else :
                                    pygame.mixer.Channel(channelNum).play(audioFour, loops = 0, maxtime = 1000)

                                if channelNum == 7:
                                    channelNum = 0
                                else:
                                    channelNum += 1

                            spawnBird(random.randint(0, windowWidth - birdHeight), random.randint(0, windowHeight - base - birdHeight))

                            mousePos = pygame.mouse.get_pos()
                            moveCat(mousePos)
                        else :
                            calculatePoints(False, True)
                            pygame.draw.rect(SCREEN, brown, ((lives * 40) - heartHeight, windowHeight - 120, heartHeight, heartHeight))
                            lives -= 1
                            spawnBird(random.randint(0, windowWidth - birdHeight), random.randint(0, windowHeight - base - birdHeight))

                            mousePos = pygame.mouse.get_pos()
                            moveCat(mousePos)
                    if event.type == KEYUP and event.key == pygame.K_SPACE and paused == True:
                        paused = False
                        mousePos = pygame.mouse.get_pos()
                        drawBoard(mousePos)
                        beenThere = True
                        clock.tick()
                        addTime = clock.get_time()
                        calculatedTime += addTime
                        pygame.mixer.unpause()
                        pygame.mixer_music.unpause()
                    if event.type == KEYUP and event.key == pygame.K_SPACE and paused == False and beenThere == False:
                        clock.tick()
                        pygame.mixer.pause()
                        pygame.mixer_music.pause()
                        pygame.mouse.set_visible(True)
                        screenTwo = pygame.Surface((windowWidth, windowHeight - base))
                        screenTwo.set_alpha(150)
                        screenTwo.fill((0, 0, 0))

                        SCREEN.blit(screenTwo, (0, 0))

                        spaceText = fontObjFifty.render("Press 'space' to continue", True, lightBrown, None)
                        SCREEN.blit(spaceText, ((windowWidth - spaceText.get_width()) / 2, (windowHeight - base - 50) / 2))
                        pygame.display.update()

                        paused = True
                    if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()

                if time_difference <= 5 and time_difference >= -5 and paused == False:
                    calculatePoints(False, False)
                    pygame.draw.rect(SCREEN, brown, ((lives * 40) - heartHeight, windowHeight - 120, heartHeight, heartHeight))
                    lives -= 1
                    spawnBird(random.randint(0, windowWidth - birdHeight), random.randint(0, windowHeight - base - birdHeight))

                    mousePos = pygame.mouse.get_pos()
                    moveCat(mousePos)
                    changed = True
                if paused == False:
                    timerText = fontObjThirty.render(str(time_difference / 1000), True, lightBrown)
                    pygame.draw.rect(SCREEN, brown, (windowWidth - 250, windowHeight - 120, 250, 30))
                    SCREEN.blit(timerText, (windowWidth - 250, windowHeight - 120))
                    pygame.display.update()

                beenThere = False
            else:
                if ranOnce == False:
                    pygame.mixer_music.stop()
                    pygame.mixer.stop()
                    pygame.mouse.set_visible(True)
                    screenTwo = pygame.Surface((windowWidth, windowHeight - base))
                    screenTwo.set_alpha(150)
                    screenTwo.fill((0, 0, 0))

                    SCREEN.blit(screenTwo, (0, 0))

                    spaceText = fontObjFifty.render("Would you like to play again?", True, lightBrown, None)
                    SCREEN.blit(spaceText, ((windowWidth - spaceText.get_width()) / 2, (windowHeight - base - 50) / 2))

                    yesNoText = fontObjThirty.render("Yes (bird sounds) : Space || Yes (music) : Up arrow || No : Escape", True, lightBrown, None)
                    SCREEN.blit(yesNoText, ((windowWidth - yesNoText.get_width()) / 2, ((windowHeight - base - 50) / 2) + 60))
                    pygame.display.update()
                    ranOnce = True
                for event in pygame.event.get():
                    if event.type == KEYUP and event.key == pygame.K_SPACE :
                        goodMusic = False
                        lives = 5
                        points = 0
                        ranOnce = False
                        changed = True
                        paused = False
                        beenThere = False
                        ranOnce = False
                        now = pygame.time.get_ticks()
                        catPos = (windowWidth / 2, (windowHeight - base) / 2)
                        drawBoard(catPos)
                    if event.type == KEYUP and event.key == pygame.K_UP:
                        goodMusic = True
                        pygame.mixer_music.play(-1, 0.0)
                        lives = 5
                        points = 0
                        ranOnce = False
                        changed = True
                        paused = False
                        beenThere = False
                        ranOnce = False
                        now = pygame.time.get_ticks()
                        catPos = (windowWidth / 2, (windowHeight - base) / 2)
                        drawBoard(catPos)
                    if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
        elif started == False :
            for event in pygame.event.get():
                if event.type == KEYUP and event.key == pygame.K_SPACE :
                    started = True
                    drawBoard(catPos)
                    changed = True
                    goodMusic = False
                if event.type == KEYUP and event.key == pygame.K_UP:
                    started = True
                    drawBoard(catPos)
                    changed = True
                    goodMusic = True
                if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()


def drawBoard(centre):
    SCREEN.fill(blue)
    pygame.draw.rect(SCREEN, brown, (0, windowHeight - base, windowWidth, base))

    wamText = fontObjFifty.render('Birds', True, lightBrown, None)
    centreX = wamText.get_width()
    SCREEN.blit(wamText, ((windowWidth - centreX) / 2, windowHeight - 100))

    timerText = fontObjThirty.render("Time: ", True, lightBrown, None)
    SCREEN.blit(timerText, (windowWidth - 400, windowHeight - 120))

    pointsText = fontObjThirty.render("Points: ", True, lightBrown, None)
    SCREEN.blit(pointsText, (windowWidth - 400, windowHeight - 60))

    pauseText = fontObjThirty.render("Press 'space' to pause", True, lightBrown, None)
    SCREEN.blit(pauseText, (10, windowHeight - 60))

    for i in range(0, 5, 1):
        heartImageOne = pygame.image.load("heart.png")
        heartImage = pygame.transform.scale(heartImageOne, (heartHeight, heartHeight)).convert_alpha()
        SCREEN.blit(heartImage, ((i * (heartHeight + 10)) + 10, windowHeight - 120))

    drawPoints()

    moveCat(centre)

    pygame.display.update()

def drawPoints():
    numPointsText = fontObjThirty.render(str(points), True, lightBrown, None)
    pygame.draw.rect(SCREEN, brown, (windowWidth - 250, windowHeight - 60, 250, 30))
    SCREEN.blit(numPointsText, (windowWidth - 250, windowHeight - 60))

def calculatePoints(caughtBird, clicked):
    global points
    if clicked == True :
        if caughtBird == True:
            points += 50
        else:
            points -= 100
    else:
        if points >= 1000:
            points -= 100
        else:
            points -= 75
    drawPoints()

def spawnBird(x, y):
    global pastX, pastY

    newSurface = pygame.Surface((250,250))
    newSurface.fill(blue)
    SCREEN.blit(newSurface, (pastX, pastY))

    birds.update(x, y)
    birds.draw(SCREEN)
    pastX = x
    pastY = y

    pygame.display.update()

def moveCat(centre) :
    newSurface = pygame.Surface((windowWidth, windowHeight - base))
    newSurface.fill(blue)
    SCREEN.blit(newSurface, (0,0))
    birds.draw(SCREEN)
    cat.update(centre)
    cat.draw(SCREEN)
    pygame.display.update()

if __name__ == '__main__':
    main()