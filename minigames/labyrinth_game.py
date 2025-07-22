import pygame
import sys

# Renkler
WHITE = (200, 200, 200)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BG_COLOR = (30, 30, 30)
TEXT_COLOR = (255, 255, 255)
DIALOG_BG = (50, 50, 50)

# Engeller
walls = [
    pygame.Rect(100, 100, 600, 20),
    pygame.Rect(100, 100, 20, 400),
    pygame.Rect(100, 480, 600, 20),
    pygame.Rect(680, 100, 20, 400),
    pygame.Rect(200, 200, 400, 20),
    pygame.Rect(200, 300, 20, 100),
    pygame.Rect(300, 300, 300, 20),
    pygame.Rect(580, 200, 20, 120),
    pygame.Rect(250, 150, 20, 150),
    pygame.Rect(350, 150, 200, 20),
    pygame.Rect(550, 150, 20, 100),
    pygame.Rect(400, 350, 150, 20),
    pygame.Rect(400, 370, 20, 100),
    pygame.Rect(500, 370, 20, 100),
    pygame.Rect(250, 400, 150, 20),
    pygame.Rect(150, 350, 20, 150),
]

start_area = pygame.Rect(120, 120, 40, 40)
exit_area = pygame.Rect(640, 440, 40, 40)

# Dialog mesajları
dialog_messages = [
    "sen: aahh bura neresi",
    "sen: bitrüs ne yaptı bana",
    "sen: lanet olası şey",
    "sen: neyse hadi bu minigame geçmeliyim"
]

def start_labyrinth_game(screen):
    pygame.mouse.set_pos((start_area.centerx, start_area.centery))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)
    font_dialog = pygame.font.SysFont("Arial", 28)
    running = True

    dialog_index = 0
    dialog_text = ""
    char_index = 0
    dialog_speed = 5
    frame_count = 0
    dialog_done = False
    dialog_wait_time = 1500
    last_dialog_switch = 0
    show_dialog = True

    while running:
        screen.fill(BG_COLOR)

        # Duvarları çiz
        for wall in walls:
            pygame.draw.rect(screen, WHITE, wall)

        # Başlangıç ve çıkış alanı
        pygame.draw.rect(screen, GREEN, start_area)
        pygame.draw.rect(screen, RED, exit_area)

        # Fare pozisyonu ve kutusu
        mx, my = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mx, my, 5, 5)
        pygame.draw.rect(screen, YELLOW, mouse_rect)

        # Sağ üst köşeye minigame başlığı
        text = font.render("Minigame: labyrinth_game", True, TEXT_COLOR)
        screen.blit(text, (screen.get_width() - text.get_width() - 20, 20))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Duvarlara çarpma
        for wall in walls:
            if mouse_rect.colliderect(wall):
                pygame.mouse.set_pos((start_area.centerx, start_area.centery))

        # Çıkışa ulaşma
        if exit_area.collidepoint(mx, my):
            screen.fill((0, 100, 0))
            font_big = pygame.font.SysFont("Arial", 48)
            text = font_big.render("ahhh göte bala buldun salak kendini bir şey sanma!", True, (255, 255, 255))
            screen.blit(text, (screen.get_width()//2 - text.get_width()//2, screen.get_height()//2 - text.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(4000)
            running = False

        # Dialog animasyonu
        if show_dialog and dialog_index < len(dialog_messages):
            if not dialog_done:
                frame_count += 1
                if frame_count >= dialog_speed:
                    frame_count = 0
                    if char_index < len(dialog_messages[dialog_index]):
                        char_index += 1
                        dialog_text = dialog_messages[dialog_index][:char_index]
                    else:
                        dialog_done = True
                        last_dialog_switch = pygame.time.get_ticks()
            else:
                if pygame.time.get_ticks() - last_dialog_switch > dialog_wait_time:
                    dialog_index += 1
                    char_index = 0
                    dialog_text = ""
                    dialog_done = False
                    if dialog_index >= len(dialog_messages):
                        show_dialog = False

            # Dialog kutusu
            dialog_rect = pygame.Rect(50, screen.get_height() - 100, screen.get_width() - 100, 60)
            pygame.draw.rect(screen, DIALOG_BG, dialog_rect, border_radius=10)
            pygame.draw.rect(screen, WHITE, dialog_rect, 2, border_radius=10)
            dialog_render = font_dialog.render(dialog_text, True, TEXT_COLOR)
            screen.blit(dialog_render, (dialog_rect.x + 15, dialog_rect.y + 15))

        pygame.display.flip()
        clock.tick(60)
