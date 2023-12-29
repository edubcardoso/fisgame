
import pygame
import random
from time import sleep

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


# DEFINE AN ASPEN CLASS
# IF I WANT A TON OF HEROS
class Hero(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Define our image
        self.image = pygame.image.load("images/fisg_sec_right.png")
        # Get Rectangle
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = random.randint(1, 5)

    def update(self):
        self.rect.y += self.velocity


# CREATE A HERO GROUP
hero_group = pygame.sprite.Group()
for i in range(5):
    hero_ = Hero(i*200, 10)
    hero_group.add(hero_)


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
    hero_group.update()
    hero_group.draw(screen)

    # FLIP THE DISPLAY TO OUTPUT OUR WORK IN THE SCREEN
    pygame.display.flip()

    # SET THE CLOCK STUFF / DELTA TIME IN SECONDS SINCE THE LAST FRAME
    # USED FROM FRAME RATE INDEPENDENT OF PHYSICS
    dt = clock.tick(60)/1000


pygame.quit()
