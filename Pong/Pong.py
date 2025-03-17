import pygame

pygame.init()

WIDTH = 1000
HEIGHT = 600

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Classical Pong Game")

paddleLeftPosition = HEIGHT//2 - 100//2
paddleRightPosition = HEIGHT//2 - 100//2

posx = WIDTH//2 - 10//2
posy = HEIGHT//2 - 10//2

yFac = -1
xFac = 1
firstTime = 1

leftScore = 0
rightScore = 0

leftMoving = 0
rightMoving = 0

paddleLeft = pygame.Rect(10, paddleLeftPosition, 10, 100)
paddleRight = pygame.Rect(WIDTH - 20, paddleRightPosition, 10, 100)
ball = pygame.Rect(posx, posy, 10, 10)

font20 = pygame.font.Font('freesansbold.ttf', 20)

running = True

paddles = [paddleLeft, paddleRight]

def update():
    global rightScore
    screen.fill(BLACK)

    text = "right score: "
    text2 = "left score: "

    text = font20.render(text+str(rightScore), True, GREEN)
    textRect = text.get_rect()
    textRect.center = (WIDTH/2 -100, 40)

    textLeft = font20.render(text2+str(leftScore), True, GREEN)
    textRectLeft = textLeft.get_rect()
    textRectLeft.center = (WIDTH/2 + 100, 40)
 
    screen.blit(text, textRect)
    screen.blit(textLeft, textRectLeft)

    global paddleLeftPosition, paddleRightPosition

    paddleLeftPosition += 0.5*leftMoving
    paddleRightPosition += 0.5*rightMoving

    paddleLeft.y = paddleLeftPosition
    paddleRight.y = paddleRightPosition

    pygame.draw.rect(screen, (255,0,0), paddleLeft)
    pygame.draw.rect(screen, (255,0,0), paddleRight)

    ball.x = posx
    ball.y = posy
    
    pygame.draw.circle(screen, (255,255,255, 0), (posx, posy), 5)
    pygame.display.flip()


def updateBall():
    global posx, posy, xFac, yFac, leftScore, rightScore

    posx += 0.2*xFac
    posy += 0.2*yFac

    global firstTime

    if posy <= 0 or posy >= HEIGHT:
        yFac *= -1

    if posx <= 0:
        rightScore += 1
        reset()
        return 1
    elif posx >= WIDTH:
        reset()
        leftScore += 1
        return -1
    else:
        return 0
        
def hit():
    global xFac
    xFac *= -1

def reset():
    global posx, posy, xFac, yFac, paddleLeftPosition, paddleRightPosition

    paddleLeftPosition = HEIGHT//2 - 100//2
    paddleRightPosition = HEIGHT//2 - 100//2

    posx = WIDTH//2 - 10//2
    posy = HEIGHT//2 - 10//2

    yFac = -1
    xFac = 1

while running:

    updateBall()
    update()
    
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                rightMoving = -1
            if event.key == pygame.K_DOWN:
                rightMoving = 1
            if event.key == pygame.K_w:
                leftMoving = -1
            if event.key == pygame.K_s:
                leftMoving = 1
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                rightMoving = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                leftMoving = 0

    for paddle in paddles:
        if ball.colliderect(paddle):
            hit()