import pygame
import random
# from time import sleep

# Pygame Setup Stuff
pygame.init()
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Game Window
pygame.display.set_caption('Fisgame')
clock = pygame.time.Clock()
running = True
pygame_icon = pygame.image.load("images/fisg.ico")
pygame.display.set_icon(pygame_icon)
# CREATE VARIABLES TO KEEP TRACK OF SCORE AND LIVES
score = 0
lives = 5
speed = 5

dt = 0  # delta time
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height() / 2)


# DEFINE A GAME CLASS
class Game:
    def __init__(self, fisga_group_, beer_group_):
        self.fisga_group = fisga_group_
        self.beer_group = beer_group_

    def update(self):
        self.check_collisions()

    def check_collisions(self):
        if pygame.sprite.groupcollide(self.fisga_group, self.beer_group, False, True):
            print(len(self.beer_group))


# DEFINE A SPRITE CLASS
class Fisga(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/fisg_sec_right.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = 5

    def update(self):
        # IT WILL HAVE ALL THE UPDATED FUNCTIONS, LIKE GAME_OVER, SCORES, ETC
        self.move()

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_UP]:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN]:
            self.rect.y += self.velocity


class Beer(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Define our image
        self.image = pygame.image.load("images/beer.png")
        # Get Rectangle
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = random.randint(1, 3)

    def update(self):
        self.rect.y += self.velocity


# CREATE A HERO GROUP
beer_group = pygame.sprite.Group()
for i in range(10):
    beer_ = Beer(i*100, 10)
    beer_group.add(beer_)

# CREATE FISGA GROUP
fisga_group = pygame.sprite.Group()
# CREATE AND POSITION FISGA
fisga_ = Fisga(200, 400)
# ADD FISGA TO THE GROUP
fisga_group.add(fisga_)

# CREATE GAME OBJECT
our_game = Game(fisga_group, beer_group)

while running:
    # poll for events
    # pygame.quit() event means the user clicked the X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # it means they clicked in the X
            running = False

    # PICK THE SCREEN COLOR
    screen.fill("#F5DADF")

    # DRAW AND MOVE HERO SPRITE
    beer_group.update()
    beer_group.draw(screen)
    fisga_group.update()
    fisga_group.draw(screen)

    # UPDATE GAME INSTANCE
    our_game.update()
    # FLIP THE DISPLAY TO OUTPUT OUR WORK IN THE SCREEN
    pygame.display.flip()

    # SET THE CLOCK STUFF  / DELTA TIME IN SECONDS SINCE THE LAST FRAME
    # USED FROM FRAME RATE INDEPENDENT OF PHYSICS
    dt = clock.tick(60)/1000


pygame.quit()
