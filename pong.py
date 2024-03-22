import pygame
import stuff

pygame.mixer.pre_init(22100, -16, 2, 64)

pygame.mixer.init()
ballGotHit = pygame.mixer.Sound("pongHit.ogg")
pygame.init()

# Font that is used to render the text
font20 = pygame.font.Font("freesansbold.ttf", 20)

clock = pygame.time.Clock()
FPS = 30

# Striker class


class Striker:
    # Take the initial position, dimensions, speed and color of the object
    def __init__(self, posx, posy, width, height, speed, color):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        # Rect that is used to control the position and collision of the object
        self.geekRect = pygame.Rect(posx, posy, width, height)
        # Object that is blit on the screen
        self.geek = pygame.draw.rect(stuff.screen, self.color, self.geekRect)

    # Used to display the object on the screen
    def display(self):
        self.geek = pygame.draw.rect(stuff.screen, self.color, self.geekRect)

    def update(self, yFac):
        self.posy = self.posy + self.speed * yFac

        # Restricting the striker to be below the top surface of the screen
        if self.posy <= 0:
            self.posy = 0
        # Restricting the striker to be above the bottom surface of the screen
        elif self.posy + self.height >= stuff.HEIGHT:
            self.posy = stuff.HEIGHT - self.height

        # Updating the rect with the new values
        self.geekRect = (self.posx, self.posy, self.width, self.height)

    def displayScore(self, text, score, x, y, color):
        text = font20.render(text + str(score), True, color)
        textRect = text.get_rect()
        textRect.center = (x, y)

        stuff.screen.blit(text, textRect)

    def getRect(self):
        return self.geekRect


# Ball class


class Ball:
    def __init__(self, posx, posy, radius, speed, color):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.xFac = 1
        self.yFac = -1
        self.ball = pygame.draw.circle(
            stuff.screen, self.color, (self.posx, self.posy), self.radius
        )
        self.firstTime = 1

    def display(self):
        self.ball = pygame.draw.circle(
            stuff.screen, self.color, (self.posx, self.posy), self.radius
        )

    def update(self):
        self.posx += self.speed * self.xFac
        self.posy += self.speed * self.yFac

        # If the ball hits the top or bottom surfaces,
        # then the sign of yFac is changed and
        # it results in a reflection
        if self.posy <= 0 or self.posy >= stuff.HEIGHT:
            self.yFac *= -1

        if self.posx <= 0 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= stuff.WIDTH and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0

    def reset(self):
        self.posx = stuff.WIDTH // 2
        self.posy = stuff.HEIGHT // 2
        self.xFac *= -1
        self.firstTime = 1

    # Used to reflect the ball along the X-axis
    def hit(self):
        self.xFac *= -1
        ballGotHit.play()

    def getRect(self):
        return self.ball


# Game Manager


def main():
    running = True
    tipCounter = 0
    pointsLog = 0
    # Defining the objects
    geek1 = Striker(20, 0, 10, 100, 10, stuff.GREEN)
    geek2 = Striker(stuff.WIDTH - 30, 0, 10, 100, 10, stuff.GREEN)
    ball = Ball(stuff.WIDTH // 2, stuff.HEIGHT // 2, 7, 7, stuff.WHITE)

    listOfGeeks = [geek1, geek2]

    # Initial parameters of the players
    geek1Score, geek2Score = 0, 0
    geek1YFac, geek2YFac = 0, 0

    while running:
        stuff.screen.fill(stuff.BLACK)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    geek2YFac = -1
                if event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_DOWN:
                    geek2YFac = 1
                if event.key == pygame.K_w:
                    geek1YFac = -1
                if event.key == pygame.K_s:
                    geek1YFac = 1
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    geek2YFac = 0
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    geek1YFac = 0

        # Collision detection
        for geek in listOfGeeks:
            if pygame.Rect.colliderect(ball.getRect(), geek.getRect()):
                ball.hit()
                ballGotHit.play()

        # Updating the objects
        geek1.update(geek1YFac)
        geek2.update(geek2YFac)
        point = ball.update()

        # -1 -> Geek_1 has scored
        # +1 -> Geek_2 has scored
        # 0 -> None of them scored
        if point == -1:
            pointsLog = pointsLog + 1
            geek1Score += 1

        elif point == 1:
            pointsLog = pointsLog + 1
            geek2Score += 1

        # Someone has scored
        # a point and the ball is out of bounds.
        # So, we reset it's position
        if point:
            ball.reset()

        # Displaying the objects on the screen
        geek1.display()
        geek2.display()
        ball.display()
        # if tipCounter <= 3 & pointsLog == 3:
        # print(stuff.gamesLore["pong"][tipCounter])

        # Displaying the scores of the players
        geek1.displayScore("Player 1 : ", geek1Score, 100, 20, stuff.WHITE)
        geek2.displayScore(
            "Player 2 : ", geek2Score, stuff.WIDTH - 100, 20, stuff.WHITE
        )
        print(f"POINT LOG{pointsLog}  COUNTER{tipCounter}")
        if pointsLog >= 3 and tipCounter + 1 <= 7:
            geek1.displayScore(
                stuff.gamesLore["pong"][tipCounter],
                "",
                stuff.WIDTH - 400,
                stuff.HEIGHT - 100,
                stuff.WHITE,
            )
            geek1.displayScore(
                stuff.gamesLore["pong"][tipCounter + 1],
                "",
                stuff.WIDTH - 400,
                stuff.HEIGHT - 80,
                stuff.WHITE,
            )
        if pointsLog > 4:
            pointsLog = 0
            tipCounter = tipCounter + 2

        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
    pygame.quit()
