import pygame


# Pygame Setup Stuff
pygame.init()
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Game Window
pygame.display.set_caption('FISGAME')
clock = pygame.time.Clock()
running = True

dt = 0  # delta time
player_pos = pygame.Vector2(screen.get_width()/2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.quit() event means the user clicked the X to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # it means they clicked in the X
            running = False

    # PICK THE SCREEN COLOR
    screen.fill("silver")
    '''
    # UNDERSTAND COORDINATES
    # TOP-LEFT IS 0,0
    # AS WE GO -> X INCREASES IF WE GO DOWN Y INCREASES

    # DRAW A LINE
    # SCREEN, COLOR, STARTING POINT (X,Y), ENDING POINT (X,Y), THICKNESS
    pygame.draw.line(screen, "yellow", (50, 50), (800, 50), 10)

    # DRAW A CIRCLE
    # SCREEN, COLOR, (TOP-LEFT X, TOP-LEFT Y, WIDTH, HEIGHT) THICKNESS 0=FILLALL
    pygame.draw.circle(screen, "orange", (500, 500), 40, 10)

    # DRAW A RECTANGLE
    # SCREEN, COLOR, CENTER POINT (X,Y), RADIUS, THICKNESS 0=FILLALL
    pygame.draw.rect(screen, "purple", (100, 400, 100, 100), 10)
    '''
    # RENDER OUR GAME HERE
    pygame.draw.circle(screen, "red", player_pos, 50)

    # MOVE OUR CIRCLE
    keys = pygame.key.get_pressed()

    # UP OR DOWN IS Y
    if keys[pygame.K_UP]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_DOWN]:
        player_pos.y += 300 * dt

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

    '''
    # USE THE MOUSE
    if event.type == pygame.MOUSEBUTTONDOWN:
        # print(event)
        pos = pygame.mouse.get_pos()
        # MOVE THE CIRCLE
        player_pos.x = pos[0]
        player_pos.y = pos[1]

    if event.type == pygame.MOUSEBUTTONUP:
        pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, "green", player_pos, 50)
    # MOTION
    if event.type == pygame.MOUSEMOTION:
        pos = pygame.mouse.get_pos()
        # MOVE THE CIRCLE
        player_pos.x = pos[0]
        player_pos.y = pos[1]
    '''
    # FLIP THE DISPLAY TO OUTPUT OUR WORK IN THE SCREEN
    pygame.display.flip()

    # SET THE CLOCK STUFF / DELTA TIME IN SECONDS SINCE THE LAST FRAME
    # USED FROM FRAMERATE INDEPENDENT OF PHYSICS
    dt = clock.tick(60)/1000


pygame.quit()