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
# CREATE VARIABLES TO KEEP TRACK OF SCORE AND LIVES
score = 0
lives = 5
speed = 5
play_sound = True

# DEFINE BACKGROUD MUSIC
pygame.mixer.music.load('sounds/apita.wav')
# PLAY BACKGROUND MUSIC
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1, 0.0)

# DEFINE SOUND EFFECTS
hit_sound = pygame.mixer.Sound('sounds/obg.wav')
miss_sound = pygame.mixer.Sound('sounds/vaca.wav')
game_over_sound = pygame.mixer.Sound('sounds/gozar.wav')


dt = 0  # delta time
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height() / 2)

# DEFINE THE FONTS
title_font = pygame.font.SysFont('impact', 50)
score_font = pygame.font.SysFont('impact', 25)
lives_font = pygame.font.SysFont('impact', 25)
game_over_font = pygame.font.SysFont('impact', 75)
restart_game_font = pygame.font.SysFont('impact', 50)

# RENDER THE FONTS
title_text = title_font.render("Get  Fisgado  Drunk!", True, 'red')
score_text = score_font.render(f"Score: {score}", True, 'red')
lives_text = lives_font.render(f"Lives: {lives}", True, 'red')
game_over_text = game_over_font.render("Game Over", True, 'red')
restart_game_text = restart_game_font.render("Press 'p' to play again", True, 'red')

# TRANSFORM THE TEXT IN RECTANGLES
title_text_rect = title_text.get_rect()
score_text_rect = score_text.get_rect()
lives_text_rect = lives_text.get_rect()
game_over_text_rect = game_over_text.get_rect()
restart_game_text_rect = restart_game_text.get_rect()

# POSITION THE TEXT
title_text_rect.center = (WINDOW_WIDTH/2, 30)
score_text_rect.topleft = (10, 5)
lives_text_rect.topleft = ((WINDOW_WIDTH - lives_text.get_width() - 10), 5)
game_over_text_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2)
restart_game_text_rect.center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2+100)

# LOAD IMAGES
hero = pygame.image.load("images/fisg_sec_right.png")
beer = pygame.image.load(f"images/beer.png")
# TRANSFORM THE IMAGES IN RECTANGLES
hero_rect = hero.get_rect()
beer_rect = beer.get_rect()
# POSITING OUR IMAGES
hero_rect.x = 0
hero_rect.y = WINDOW_HEIGHT/2
beer_rect.x = WINDOW_WIDTH - 100
beer_rect.y = random.randint(65, (WINDOW_HEIGHT - beer.get_height()))
#
pygame_icon = pygame.image.load("images/fisg.ico")
pygame.display.set_icon(pygame_icon)
while running:
    # poll for events
    # pygame.quit() event means the user clicked the X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # it means they clicked in the X
            running = False

    # PICK THE SCREEN COLOR
    screen.fill("#F5DADF")

    # BLIT THE TEXT ON THE SCREEN
    screen.blit(title_text, title_text_rect)
    screen.blit(score_text, score_text_rect)
    screen.blit(lives_text, lives_text_rect)
    # screen.blit(game_over_text, game_over_text_rect)

    # BLIT (=COPY) IMAGES ON SCREEN
    screen.blit(beer, beer_rect)
    screen.blit(hero, hero_rect)

    # DRAW A LINE
    pygame.draw.line(screen, "red", (0, 60), (WINDOW_WIDTH, 60), 2)

    # CHECK IF WE'RE OUT OF LIVES
    if lives == 0:

        sleep(1)
        screen.blit(game_over_text, game_over_text_rect)
        screen.blit(restart_game_text, restart_game_text_rect)
        # STOP FOOD
        beer_rect.x = WINDOW_WIDTH + 100
        # beer_rect.y = 10000

        if play_sound:
            # PLAY GAME OVER SOUND
            game_over_sound.play()
            play_sound = False
            # TURN OFF BG MUSIC
            pygame.mixer.music.stop()

        # CHECK FOR 'P'
        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            score = 0
            lives = 5
            speed = 5
            play_sound = True
            pygame.mixer.music.play(-1, 0.0)

            # RE-RENDER THE SCORE & LIVES
            score_text = score_font.render(f"Score: {score}", True, 'red')
            lives_text = lives_font.render(f"Lives: {lives}", True, 'red')

        # CHECK FOR COLLISIONS
    if hero_rect.colliderect(beer_rect):
        # PLAY SOUND
        hit_sound.play()
        # PUSH THE IMAGE
        # beer.fill(0)  MAKE THE IMAGE BLANK
        score += 1
        speed += random.random()
        if speed > 25:
            speed = 25.0
        score_text = score_font.render(f"Score: {score}", True, 'red')
        beer_rect.x = WINDOW_WIDTH + 100
        beer_rect.y = random.randint(60, WINDOW_HEIGHT - 150)

    keys = pygame.key.get_pressed()

    # MOVE HERO
    player_pos = hero_rect
    if keys[pygame.K_UP] and player_pos.y > 60:
        player_pos.y -= (speed*30) * dt
    if keys[pygame.K_DOWN] and player_pos.y < WINDOW_HEIGHT - hero.get_height() - 5:
        player_pos.y += (speed*30) * dt

    # MOVE BEER
    if beer_rect.x < 0:
        # PLAY SOUND
        miss_sound.play()
        # CESAR MISSED THE FOOD
        lives -= 1
        lives_text = lives_font.render(f"Lives: {lives}", True, 'red')
        beer_rect.x = WINDOW_WIDTH + 100
        beer_rect.y = random.randint(65, (WINDOW_HEIGHT - beer.get_height()))
    else:
        # speed = speed + score/100
        beer_rect.x -= speed

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
    # USED FROM FRAME RATE INDEPENDENT OF PHYSICS
    dt = clock.tick(60)/1000


pygame.quit()
