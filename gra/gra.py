import pygame
import random

# Inicjalizacja Pygame
pygame.init()

# Ustawienia ekranu
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mistrz lotów')

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Załaduj obraz tła
background = pygame.image.load('background.jpg').convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Klasa gracza


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Ładowanie obrazka dla gracza
        self.image = pygame.image.load('player.png').convert_alpha()
        # Skalowanie obrazka do 30x30 pikseli
        self.image = pygame.transform.scale(self.image, (37, 37))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Zatrzymaj gracza na ekranie
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Klasa przeszkód


class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super(Obstacle, self).__init__()
        # Ładowanie obrazka dla przeszkody
        self.image = pygame.image.load('walizka2.png').convert_alpha()
        # Skalowanie obrazka do 30x30 pikseli
        self.image = pygame.transform.scale(self.image, (37, 37))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(5, 13)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed = random.randint(5, 13)


def show_start_screen():
    screen.blit(background, (0, 0))
    draw_text(screen, "MISTRZ LOTÓW", 64,
              SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(screen, "Naciśnij SPACJĘ, aby rozpocząć",
              22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    wait_for_key()


def show_game_over_screen():
    screen.blit(background, (0, 0))
    draw_text(screen, "KONIEC GRY", 64, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text(screen, "Naciśnij SPACJĘ, aby zagrać ponownie",
              22, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    pygame.display.flip()
    wait_for_key()


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False


def new_game():
    global player, all_sprites, obstacles
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    obstacles = pygame.sprite.Group()
    for i in range(10):
        obstacle = Obstacle()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)


# Główna pętla gry
clock = pygame.time.Clock()
running = True

show_start_screen()
new_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Aktualizacja
    all_sprites.update()

    # Sprawdzenie kolizji
    if pygame.sprite.spritecollideany(player, obstacles):
        show_game_over_screen()
        new_game()

    # Rysowanie
    screen.blit(background, (0, 0))
    all_sprites.draw(screen)
    pygame.display.flip()

    # Kontrola liczby klatek na sekundę
    clock.tick(30)

pygame.quit()
