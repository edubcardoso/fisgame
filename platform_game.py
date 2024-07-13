import pygame

# Define a 2d Vector
vector = pygame.math.Vector2

# Initialize the game
pygame.init()

# Set display surface (divisible by 32 tile size)
WINDOW_WIDTH = 960  # 30 columns
WINDOW_HEIGHT = 640  # 20 rows
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Fisgame - Platform Game")

# Set FPS and clock
FPS = 60
clock = pygame.time.Clock()


# Tile Class
class Tile(pygame.sprite.Sprite):
    # Read and Create tiles and put em on the screen
    def __init__(self, x, y, image_integer, main_group, sub_group=""):
        super().__init__()
        # Load image and add to the tile subgroups
        if image_integer == 1:
            self.image = pygame.image.load('images/platform/dirt.png')
        elif image_integer == 2:
            self.image = pygame.image.load('images/platform/grass.png')
            # CREATE A MASK FRO GRASS
            self.mask = pygame.mask.from_surface(self.image)
            sub_group.add(self)
        elif image_integer == 3:
            self.image = pygame.image.load('images/platform/water.png')
            sub_group.add(self)

        # add every tile to main tile group
        main_group.add(self)

        # Get rect of images and position within the grid
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, bullet_group, player):
        super().__init__()
        self.velocity = 20
        self.range = 400  # Pixels, bullet disapears
        tiro_image = pygame.image.load("images/tiro.png")

        # Load Image, get rect, based on player direction
        if player.velocity.x > 0:  # facing right
            self.image = pygame.transform.scale(tiro_image, (60, 28))
        else:
            # Facing left
            self.image = pygame.transform.scale(pygame.transform.flip(tiro_image, True, False), (60, 28))
            self.velocity = -1*self.velocity

        # rect stuff
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # GET STARTING POSITION
        self.starting_x = x

        # ADD BULLET GROUP
        bullet_group.add(self)

    def update(self):
        # MOVE THE BULLET
        self.rect.x += self.velocity

        # DESTROY THE BULLET
        if abs(self.rect.x - self.starting_x) > self.range:
            self.kill()


# Apsen Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, grass_tiles, water_tiles, bullet_group):
        super().__init__()

        # Define our player image
        # self.image = pygame.image.load("images/fisg_sec_right_sm.png")  # only 1 image
        # Animation lists - Animation Loops
        self.move_right_sprites = []
        self.move_left_sprites = []
        self.idle_right_sprites = []
        self.idle_left_sprites = []

        # SET CURRENT IMAGE
        self.current_sprite = 0  # index of the sprit list

        # Define our moving right sprite images
        for num in range(1, 10):
            self.move_right_sprites.append(pygame.image.load(fr"images/player/Walk ({num}).png"))
        # Define our moving left sprite images
        for sprite_ in self.move_right_sprites:
            self.move_left_sprites.append(pygame.transform.flip(sprite_, True, False))  # Image, Horizonal, Vertical

        # Define our idle right sprite images
        for num in range(1, 10):
            self.idle_right_sprites.append(pygame.image.load(fr"images/player/Idle ({num}).png"))
        # Define our idle left sprite images
        for sprite_ in self.idle_right_sprites:
            self.idle_left_sprites.append(pygame.transform.flip(sprite_, True, False))

        # SET OUR IMAGE
        self.image = self.move_right_sprites[self.current_sprite]

        # Get rect
        self.rect = self.image.get_rect()
        # Postion player
        self.rect.bottomleft = (x, y)

        # RESET PLAYER IF IT FALLS
        self.start_x = x
        self.start_y = y

        # DEFINE OUR GRASS, WATER AND BULLETS
        self.grass_tiles = grass_tiles
        self.water_tiles = water_tiles
        self.bullet_group = bullet_group

        # Kinematic Vectors (x,y)
        self.position = vector(x, y)
        self.velocity = vector(0, 0)  # Don't move to start 0,0
        self.acceleration = vector(0, 0)  # no speeding up or slowing down to start 0,0

        # Kinematic Constants
        self.HORIZONTAL_ACCELERATION = 0.75  # How quick player speeds up
        self.HORIZONTAL_FRICTION = 0.20  # friction
        self.VERTICAL_ACCELARERATION = 0.5  # GRAVITY
        self.VERTICAL_JUMP_SPEED = 15  # Determine how high we can jump

    def jump(self):
        # ONLY WANT TO JUMP WHEN ASPEN IS ON GRASS
        if pygame.sprite.spritecollide(self, self.grass_tiles, False):
            self.velocity.y = -1 * self.VERTICAL_JUMP_SPEED  # jumping up so its negative

    def shoot(self):
        # CREATE A BULLET INSTANCE
        Bullet(self.rect.centerx, self.rect.centery, self.bullet_group, self)

    def update(self):
        # Draw a rect around our player
        # pygame.draw.rect(display_surface, "blue", self.rect, 1)

        # Create a mask
        self.mask = pygame.mask.from_surface(self.image)
        # Draw mask
        self.mask.outline()
        # pygame.draw.lines(self.image, "red", True, mask_outline)

        # set the initial acceleration to 0,0 to start
        self.acceleration = vector(0, self.VERTICAL_ACCELARERATION)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acceleration.x = -1 * self.HORIZONTAL_ACCELERATION
            self.animate(self.move_left_sprites, 0.5)
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acceleration.x = self.HORIZONTAL_ACCELERATION
            # RUN OUR ANIMATION
            self.animate(self.move_right_sprites, 0.5)
        else:
            # CHECK VELOCITY TO IDLE LEFT OR RIGHT
            if self.velocity.x > 0:
                self.animate(self.idle_right_sprites, 0.2)
            else:
                self.animate(self.idle_left_sprites, 0.2)

        # Calculate new Kinematics
        self.acceleration.x -= self.velocity.x * self.HORIZONTAL_FRICTION
        self.velocity += self.acceleration  # (1,2) + (3,4) = (4,6)
        self.position += self.velocity + 0.5 * self.acceleration

        # SET UP WRAPPER
        if self.position.x < 0:  # x value fo position on the left side of the screen
            self.position.x = WINDOW_WIDTH
        if self.position.x > WINDOW_WIDTH:
            self.position.x = 0

        # update rect
        self.rect.bottomleft = self.position

        # CHECK FOR COLLISIONS WITH GRASS
        # RETURN A PYTOHN LIST OF TILES
        touched_grass = pygame.sprite.spritecollide(self, self.grass_tiles, False, pygame.sprite.collide_mask)
        if touched_grass:
            if self.velocity.y > 0:
                self.position.y = touched_grass[0].rect.top + 1
                self.velocity.y = 0

        # CHECK FOR COLLISIONS WITH WATER
        if pygame.sprite.spritecollide(self, self.water_tiles, False):
            # print('YOU DIED')
            # RESET PLAYER POSITION
            self.position = vector(self.start_x, self.start_y)
            self.velocity = vector(0, 0)

    def animate(self, sprite_list, speed):
        if self.current_sprite < len(sprite_list) - 1:
            self.current_sprite += speed
        else:
            self.current_sprite = 0

        self.image = sprite_list[int(self.current_sprite)]


# Define our sprite groups
main_tile_group = pygame.sprite.Group()
grass_tile_group = pygame.sprite.Group()
water_tile_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()


# Create a tile map, nested python list: 0=no tile, 1=dirt, 2=grass, 3=water, 4=player
tile_map = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2],
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 3, 3, 3, 3, 1, 1, 1, 1, 1]
]

# Create Tile objects from the tile map
# 2 for loops because tile map is nested. 20 i down
for i in range(len(tile_map)):
    # loop though the 30 elements in each list, j across
    for j in range(len(tile_map[i])):
        # Check for 0,1,2,3
        if tile_map[i][j] == 1:
            # dirt
            Tile(j*32, i*32, 1, main_tile_group)
        elif tile_map[i][j] == 2:
            # grass
            Tile(j*32, i*32, 2, main_tile_group, grass_tile_group)
        elif tile_map[i][j] == 3:
            # water
            Tile(j*32, i*32, 3, main_tile_group, water_tile_group)
        elif tile_map[i][j] == 4:
            player = Player(j * 32, i * 32 + 32, grass_tile_group, water_tile_group, bullet_group)
            player_group.add(player)


# Add a background
bg_image = pygame.image.load('images/platform/bg.png')
bg_image_rect = bg_image.get_rect()
bg_image_rect.topleft = (0, 0)


# Game Loop
running = True
while running:
    # Check to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # JUMP and SHOOT
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()
            if event.key == pygame.K_s:
                player.shoot()

    # fill the display or blit an image
    # display_surface.fill("black")
    display_surface.blit(bg_image, bg_image_rect)

    # Draw the Tiles
    main_tile_group.draw(display_surface)

    # Update and draw sprites
    player_group.update()
    player_group.draw(display_surface)

    # UPDATE AND DRAW BULLETS
    bullet_group.update()
    bullet_group.draw(display_surface)

    # Update Display
    pygame.display.update()
    clock.tick(FPS)

# End the game
pygame.quit()
