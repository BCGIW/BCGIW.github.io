import pygame
import sys

pygame.init()

# Window settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
FONT = pygame.font.Font(None, 36)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 60)

    def move(self, y):
        self.rect.y += y
        self.rect.clamp_ip(WINDOW.get_rect())

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.dx = 1
        self.dy = 1

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def bounce(self, axis):
        if axis == "x":
            self.dx *= -1
        elif axis == "y":
            self.dy *= -1

paddle_a = Paddle(20, WINDOW_HEIGHT // 2 - 30)
paddle_b = Paddle(WINDOW_WIDTH - 30, WINDOW_HEIGHT // 2 - 30)
ball = Ball(WINDOW_WIDTH // 2 - 5, WINDOW_HEIGHT // 2 - 5)

def draw_objects():
    WINDOW.fill(BLACK)
    pygame.draw.rect(WINDOW, WHITE, paddle_a.rect)
    pygame.draw.rect(WINDOW, WHITE, paddle_b.rect)
    pygame.draw.ellipse(WINDOW, WHITE, ball.rect)
    pygame.draw.aaline(WINDOW, WHITE, (WINDOW_WIDTH // 2, 0), (WINDOW_WIDTH // 2, WINDOW_HEIGHT))
    pygame.display.flip()

def collision_detection():
    if ball.rect.colliderect(paddle_a.rect) or ball.rect.colliderect(paddle_b.rect):
        ball.bounce("x")
    if ball.rect.y <= 0 or ball.rect.y + ball.rect.height >= WINDOW_HEIGHT:
        ball.bounce("y")

def start_menu():
    menu_font = pygame.font.Font(None, 48)
    menu_options = ['SINGLE PLAYER', 'MULTIPLAYER']
    selected_option = 0

    while True:
        WINDOW.fill(BLACK)

        for i, option in enumerate(menu_options):
            if i == selected_option:
                color = (255, 255, 0)
            else:
                color = WHITE
            option_text = menu_font.render(option, True, color)
            WINDOW.blit(option_text, (WINDOW_WIDTH // 2 - option_text.get_width() // 2, 200 + 60 * i))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    return selected_option

def ai_paddle_move(paddle, ball):
    if paddle.rect.centery < ball.rect.centery - 5:
        paddle.move(5)
    elif paddle.rect.centery > ball.rect.centery + 5:
        paddle.move(-5)

player_choice = start_menu()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        paddle_b.move(-5)
    if keys[pygame.K_DOWN]:
        paddle_b.move(5)
    if player_choice == 1:  # Play against a friend
        if keys[pygame.K_w]:
            paddle_a.move(-5)
        if keys[pygame.K_s]:
            paddle_a.move(5)
    else:  # Play against the computer
        ai_paddle_move(paddle_a, ball)

    ball.move()
    collision_detection()
    draw_objects()
    clock.tick(60)
