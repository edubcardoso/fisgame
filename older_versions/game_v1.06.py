import pygame


# Pygame Setup Stuff
pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Game Window
pygame.display.set_caption('Fisgame')
clock = pygame.time.Clock()
running = True

dt = 0  # delta time
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height() / 2)

# GAME SOUND EFFECTS
sound_1 = pygame.mixer.Sound('sounds/sound_1.wav')

# pygame.time.delay(2000)   # TIME DELAY
# sound_1.play()  # PLAY SOUND EFFECT
# sound_1.set_volume(0.1)  # CHANGE SOUND'S VOLUME, BETWEEN 0 AND 1
# pygame.time.delay(2000)   # TIME DELAY

# LOAD BACKGROUND MUSIC
pygame.mixer.music.load('sounds/bg.wav')
# PLAY BACKGROUND MUSIC
pygame.mixer.music.play(-1, 0.0)  # REPEATS AND WHERE TO START PLAYING
pygame.time.delay(5000)
pygame.mixer.music.stop()
# DISPLAY OUR FONTS
# fonts = pygame.font.get_fonts()
# for font in fonts:
#     print(font)

system_font = pygame.font.SysFont('arial', 80)

# RENDER THE TEXT (AS A SURFACE)
text_ = "This is the Fisgame"
system_font = system_font.render(text_, True, "black")
# WE HAVE TO CREATE A RECT
system_font_rect = system_font.get_rect()
# POSITION THE TEXT
system_font_rect.center = (WINDOW_WIDTH//2, 100)


# TODO RESIZNG THE IMAGES
hero_type = "sec"
hero_left = pygame.image.load(f"images/fisg_{hero_type}_left.png")
hero_right = pygame.image.load(f"images/fisg_{hero_type}_right.png")

# Set the scale factor for resizing
scale_factor = 2/3  # Adjust this value as needed
# Resize the images
hero_left = pygame.transform.scale(
    hero_left,
    (int(hero_left.get_width() * scale_factor),
     int(hero_left.get_height() * scale_factor))
    )
hero_right = pygame.transform.scale(
    hero_right,
    (int(hero_right.get_width() * scale_factor),
     int(hero_right.get_height() * scale_factor))
    )

# GET RECT AROUND THE IMAGES
hero_left_rect = hero_left.get_rect()
hero_right_rect = hero_right.get_rect()

# POSITING OUR IMAGES
hero_left_rect.topleft = (0, 0)
hero_right_rect.topright = (WINDOW_WIDTH, 0)

while running:
    # poll for events
    # pygame.quit() event means the user clicked the X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # it means they clicked in the X
            running = False

    # PICK THE SCREEN COLOR
    screen.fill("silver")

    # RENDER OUR GAME HERE
    # pygame.draw.circle(screen, "red", player_pos, 50)

    # BLIT THE TEXT ON THE SCREEN
    screen.blit(system_font, system_font_rect)

    # BLIT (=COPY) SCREEN OBJECT AT SOME GIVEN COORDINATES
    # screen.blit(hero_right, hero_right_rect)
    screen.blit(hero_left, hero_left_rect)



    # MOVE OUR CIRCLE
    keys = pygame.key.get_pressed()
    player_pos = hero_left_rect
    # UP OR DOWN IS Y
    if keys[pygame.K_UP]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        player_pos.y += 300 * dt
        sound_1.play()

    # LEFT OR RIGHT IS X
    if keys[pygame.K_LEFT]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_RIGHT]:
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
