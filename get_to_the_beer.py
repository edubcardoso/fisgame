import pygame
import random

# Pygame Setup Stuff
pygame.init()
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Game Window
pygame.display.set_caption('Fisgame')
clock = pygame.time.Clock()
running = True
# CREATE VARIABLES TO KEEP TRACK OF SCORE AND LIVES
score = 0
lives = 5

dt = 0  # delta time
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height() / 2)

# DEFINE THE FONTS
title_font = pygame.font.SysFont('impact', 50)
score_font = pygame.font.SysFont('impact', 25)
lives_font = pygame.font.SysFont('impact', 25)
game_over_font = pygame.font.SysFont('impact', 75)

# RENDER THE FONTS
title_text = title_font.render("Get  Cesar  Drunk!", True, 'red')
score_text = score_font.render(f"Score: {score}", True, 'red')
lives_text = lives_font.render(f"Lives: {lives}", True, 'red')
game_over_text = game_over_font.render("Game Over", True, 'red')

# TRANSFORM THE TEXT IN RECTANGLES
title_text_rect = title_text.get_rect()
score_text_rect = score_text.get_rect()
lives_text_rect = lives_text.get_rect()
game_over_text_rect = game_over_text.get_rect()

# POSITION THE TEXT
title_text_rect.center = (WINDOW_WIDTH/2, 30)
score_text_rect.topleft = (10, 5)
lives_text_rect.topleft = ((WINDOW_WIDTH - lives_text.get_width() - 10), 5)
game_over_text_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)

# LOAD IMAGES
hero = pygame.image.load("images/fisg_main_right.png")
beer = pygame.image.load(f"images/beer.png")
# TRANSFORM THE IMAGES IN RECTANGLES
hero_rect = hero.get_rect()
beer_rect = beer.get_rect()
# POSITING OUR IMAGES
hero_rect.center = (60, WINDOW_HEIGHT/2)
beer_rect.center = (WINDOW_WIDTH//2, WINDOW_HEIGHT//2,)

while running:
    # poll for events
    # pygame.quit() event means the user clicked the X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # it means they clicked in the X
            running = False

    # PICK THE SCREEN COLOR
    screen.fill("silver")

    # BLIT THE TEXT ON THE SCREEN
    screen.blit(title_text, title_text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)
    # screen.blit(game_over_text, game_over_text_rect)

    # BLIT (=COPY) SCREEN OBJECT AT SOME GIVEN COORDINATES
    screen.blit(beer, beer_rect)
    screen.blit(hero, hero_rect)

    # DRAW A LINE
    pygame.draw.line(screen, "red", (0, 60), (WINDOW_WIDTH,60),2)

    # CHECK FOR COLLISIONS
    if hero_rect.colliderect(beer_rect):
        # PUSH THE IMAGE
        # beer.fill(0)  MAKE THE IMAGE BLANK
        beer_rect.x = random.randint(0, WINDOW_WIDTH - 150)
        beer_rect.y = random.randint(0, WINDOW_HEIGHT - 150)

    # MOVE OUR CIRCLE
    keys = pygame.key.get_pressed()
    player_pos = hero_rect
    # UP OR DOWN IS Y
    if keys[pygame.K_UP] and player_pos.y > -10:
        player_pos.y -= 300 * dt
    if keys[pygame.K_DOWN] and player_pos.y < WINDOW_HEIGHT-98:
        player_pos.y += 300 * dt
        # sound_1.play()

    # LEFT OR RIGHT IS X
    if keys[pygame.K_LEFT] and player_pos.x > -5:
        player_pos.x -= 300 * dt
    if keys[pygame.K_RIGHT] and player_pos.x < WINDOW_WIDTH-90:
        player_pos.x += 300 * dt

    # CHECK TO SEE IF MOUSE HAS BEEN PRESSED
    if pygame.mouse.get_pressed()[2]:
        # MOVE THE CIRCLE
        if event.type == pygame.MOUSEMOTION:
            pos = pygame.mouse.get_pos()
            player_pos.x = pos[0]
            player_pos.y = pos[1]

    # FLIP THE DISPLAY TO OUTPUT OUR WORK IN THE SCREEN
    pygame.display.flip()

    # SET THE CLOCK STUFF / DELTA TIME IN SECONDS SINCE THE LAST FRAME
    # USED FROM FRAMERATE INDEPENDENT OF PHYSICS
    dt = clock.tick(60)/1000


pygame.quit()
