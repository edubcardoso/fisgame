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
    def __init__(self, fisga_group_, drink_group_):
        self.fisga_group = fisga_group_
        self.drink_group = drink_group_
        self.score = 0
        self.lives = 5

        # DEFINE FONTS
        self.small_font = pygame.font.SysFont("imapact", 24)
        self.big_font = pygame.font.SysFont("imapact", 60)

        # DEFINE IMAGES
        self.beer = pygame.image.load("images/beer.png")
        self.water = pygame.image.load("images/water.png")

        # ADD DRINKS to a GROUP
        # TYPE 0=WATER, 1=BEER
        self.drink_group.add(Drink(random.randint(20, 800), random.randint(100, 400), self.beer, 1))
        for i in range(7):
            self.drink_group.add(Drink(i*50+50, 190, self.water, 0))

        # DEFINE OUR SOUNDS
        self.score_sound = pygame.mixer.Sound('sounds/obg.wav')
        self.die_sound = pygame.mixer.Sound('sounds/vaca.wav')
        self.game_over_sound = pygame.mixer.Sound('sounds/gozar.wav')

    def update(self):
        self.check_collisions()
        self.draw()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_p]:
            self.pause_game()

    def draw(self):
        # DRAW A BOUNDARY BOX
        pygame.draw.rect(screen, 'red', (0, 100, WINDOW_WIDTH, WINDOW_HEIGHT-200), 4)
        # CREATE TEXT
        title_text = self.big_font.render('DRINK BEER', True, "red")
        title_rect = title_text.get_rect()
        title_rect.centerx = WINDOW_WIDTH / 2
        title_rect.top = 5

        win_text = self.big_font.render('YOU WON!!!', True, "black")
        win_rect = win_text.get_rect()
        win_rect.centerx = WINDOW_WIDTH / 2
        win_rect.centery = WINDOW_HEIGHT / 2 - 100

        lose_text = self.big_font.render('YOU LOST!!!', True, "orange")
        lose_rect = lose_text.get_rect()
        lose_rect.centerx = WINDOW_WIDTH / 2
        lose_rect.centery = WINDOW_HEIGHT / 2 - 100

        restart_text = self.big_font.render('Press Enter to Play Again', True, "black")
        restart_rect = restart_text.get_rect()
        restart_rect.centerx = WINDOW_WIDTH / 2
        restart_rect.centery = WINDOW_HEIGHT / 2

        score_text = self.small_font.render(f'Score: {self.score}', True, "red")
        score_rect = score_text.get_rect()
        score_rect.topleft = (5, 5)

        lives_text = self.small_font.render(f'Lives: {self.lives}', True, "red")
        lives_rect = lives_text.get_rect()
        lives_rect.topright = (WINDOW_WIDTH - 5, 5)

        # BLIT THE TEXT
        screen.blit(title_text, title_rect)
        screen.blit(score_text, score_rect)
        screen.blit(lives_text, lives_rect)

        if self.score == 7:
            screen.blit(win_text, win_rect)
            screen.blit(restart_text, restart_rect)
            self.game_over()

        if self.lives <= 0:
            screen.blit(lose_text, lose_rect)
            screen.blit(restart_text, restart_rect)
            self.drink_group.remove(drink_group)  # REMOVE ANY REMAINING FOOD
            self.game_over()

    def game_over(self):
        self.fisga_group.reset()
        # CHECK FOR RESTART ENTER
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            # RESET NUMBERS
            self.score = 0
            self.lives = 5
            # ADD NEW
            self.drink_group.add(Drink(random.randint(20, 800), random.randint(100, 400), self.beer, 1))
            for i in range(7):
                self.drink_group.add(Drink(i * 50 + 50, 190, self.water, 0))

    def pause_game(self):
        print(self)
        global running
        is_paused = True
        # CREATE PAUSED GROUP
        while is_paused:
            # ACCOUNT FOR HITTING ENTER WHILE ON PAUSE TO UNPAUSE
            for event_ in pygame.event.get():
                if event_.type == pygame.KEYDOWN:
                    if event_.key == pygame.K_RETURN:
                        is_paused = False
                # ACCOUNT FOR CLICKING THE X TO QUIT
                if event_.type == pygame.QUIT:
                    is_paused = False
                    running = False
                    # pygame.quit()

    def check_collisions(self):
        caught_drink = pygame.sprite.spritecollideany(self.fisga_group, self.drink_group)
        if caught_drink:
            # IF IS BEER
            if caught_drink.drink_type == 0:
                # PLAY DIE SOUND
                self.die_sound.play()
                self.lives -= 1
                self.fisga_group.reset()
                if self.lives == 0:
                    self.game_over_sound.play()
            else:
                # PLAY SCORE SOUND
                self.score_sound.play()
                caught_drink.remove(self.drink_group)
                self.score += 1
                # LOGIC to REMOVE WATER and ADD BEER
                if len(self.drink_group) > 0:
                    # RANDOMLY REMOVE WATER FROM SPRITES in DRINK GROUP
                    random.choice(self.drink_group.sprites()).kill()
                    # ADD A NEW BEER - TRANFORM WATER IN BEER
                    if len(self.drink_group) >= 1:
                        self.drink_group.add(Drink(random.randint(20, 800), random.randint(100, 400), self.beer, 1))
                    else:
                        self.fisga_group.reset()
                        self.game_over_sound.play()


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
        if keys[pygame.K_LEFT] and self.rect.x >= 10:
            self.rect.x -= self.velocity
        if keys[pygame.K_RIGHT] and self.rect.x <= WINDOW_WIDTH - 105:
            self.rect.x += self.velocity
        if keys[pygame.K_UP] and self.rect.y >= 100:
            self.rect.y -= self.velocity
        if keys[pygame.K_DOWN] and self.rect.y <= WINDOW_HEIGHT - 95:
            self.rect.y += self.velocity

    # MOVE FISGA TO UNDE THE BOX
    def reset(self):
        self.rect.topleft = ((WINDOW_WIDTH/2)-50, 510)


class Drink(pygame.sprite.Sprite):
    def __init__(self, x, y, image, drink_type):
        super().__init__()
        # Define our image
        self.image = image
        # Get Rectangle
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.velocity = random.randint(1, 5)
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])
        # DRINK TYPE 0=water, 1=beer
        self.drink_type = drink_type

    def update(self):
        # self.rect.y += self.velocity
        self.rect.x += self.dx * self.velocity
        self.rect.y += self.dy * self.velocity
        # KEEP FROM LEAVING THE SCREEN
        if self.rect.left <= -1 or self.rect.right >= WINDOW_WIDTH:
            self.dx = -1 * self.dx
        if self.rect.top <= 100 or self.rect.bottom >= 500:
            self.dy = -1 * self.dy


# CREATE A HERO GROUP
drink_group = pygame.sprite.Group()

# CREATE FISGA GROUP
fisga_group = pygame.sprite.Group()
# CREATE AND POSITION FISGA
fisga_ = Fisga((WINDOW_WIDTH/2)-50, 510)
# ADD FISGA TO THE GROUP
fisga_group.add(fisga_)

# CREATE GAME OBJECT
our_game = Game(fisga_, drink_group)

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
    drink_group.update()
    drink_group.draw(screen)
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
