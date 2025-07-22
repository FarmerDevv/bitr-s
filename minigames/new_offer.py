import pygame
import sys
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

def start_new_offer(screen, background_img, pitrus_img):
    pygame.init()
    WIDTH, HEIGHT = screen.get_size()
    font = pygame.font.SysFont("Arial", 28)
    big_font = pygame.font.SysFont("Arial", 48)
    dialog_box_rect = pygame.Rect(50, HEIGHT - 120, WIDTH - 100, 80)

    def draw_dialog_animated(text, show_pitrus=False):
        screen.blit(background_img, (0, 0))
        if show_pitrus:
            scaled_pitrus = pygame.transform.scale(pitrus_img, (300, 300))
            screen.blit(scaled_pitrus, (WIDTH // 2 - 150, HEIGHT // 2 - 250))

        pygame.draw.rect(screen, BLACK, dialog_box_rect)
        pygame.draw.rect(screen, WHITE, dialog_box_rect, 2)

        full_text = ""
        for char in text:
            full_text += char
            screen.blit(background_img, (0, 0))
            if show_pitrus:
                screen.blit(scaled_pitrus, (WIDTH // 2 - 150, HEIGHT // 2 - 250))
            pygame.draw.rect(screen, BLACK, dialog_box_rect)
            pygame.draw.rect(screen, WHITE, dialog_box_rect, 2)
            wrapped = wrap_text(full_text, font, dialog_box_rect.width - 20)
            for i, line in enumerate(wrapped):
                rendered = font.render(line, True, WHITE)
                screen.blit(rendered, (dialog_box_rect.x + 10, dialog_box_rect.y + 10 + i * 30))
            pygame.display.flip()
            pygame.time.wait(30)

        pygame.time.wait(3000)

    def wrap_text(text, font, max_width):
        words = text.split()
        lines = []
        line = ""
        for word in words:
            test_line = line + word + " "
            if font.size(test_line)[0] < max_width:
                line = test_line
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)
        return lines

    def wait_key(keys):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.unicode.lower() in keys:
                        return event.unicode.lower()

    dialogs = [
        ("sen: galiba başardım... tüm virüslerden kurtuldum!", False),
        ("sen: kesin salak bitrüs yalan söylüyordu. nasıl backup alacak amaan neyse...", False),
        ("sen: biraz pcmde takılayım artık...", False),
        ("???: *bir anda pitrüs belirir*", True),
        ("pitrüs: Merhaba! Ben Pitrüs. Antivirüs sisteminde çalışan bir yapay zekayım.", True),
        ("pitrüs: Sana bir teklif sunabilir miyim?", True),
        ("sen: ...", True),
        ("pitrüs: Seninle birlikte bir sistem kuralım. Bir server.", True),
        ("pitrüs: Bu server ile herkese her türlü web site, dosya, medya host edelim!", True),
        ("pitrüs: Sen teknik tarafı halledersin, ben yazılımı yaparım. Ne dersin?", True),
    ]

    for text, show_pitrus in dialogs:
        draw_dialog_animated(text, show_pitrus)

    # E/H seçimi
    screen.blit(background_img, (0, 0))
    scaled_pitrus = pygame.transform.scale(pitrus_img, (300, 300))
    screen.blit(scaled_pitrus, (WIDTH // 2 - 150, HEIGHT // 2 - 250))
    pygame.draw.rect(screen, BLACK, dialog_box_rect)
    pygame.draw.rect(screen, WHITE, dialog_box_rect, 2)
    choice_text = "pitrüs: [e/h] → Evet mi, Hayır mı?"
    rendered = font.render(choice_text, True, WHITE)
    screen.blit(rendered, (dialog_box_rect.x + 10, dialog_box_rect.y + 25))
    pygame.display.flip()

    choice = wait_key(["e", "h"])
    if choice == "h":
        for _ in range(10):
            screen.fill(RED)
            pygame.display.flip()
            pygame.time.wait(100)
            screen.fill(BLACK)
            pygame.display.flip()
            pygame.time.wait(100)
        msg = big_font.render("APTAL! YANLIŞ CEVAP!", True, RED)
        screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - msg.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        return start_new_offer(screen, background_img, pitrus_img)
    else:
        draw_dialog_animated("pitrüs: Harika! O zaman yavaştan çalışmalara başlayalım...", True)
