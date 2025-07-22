import pygame
import random
import time

def start_code_race(screen, bitrus_img):
    pygame.font.init()
    width, height = screen.get_size()
    font = pygame.font.SysFont("consolas", 24)
    input_font = pygame.font.SysFont("consolas", 28)
    clock = pygame.time.Clock()

    code_snippets = [
        "for i in range",
        "def hello()",
        "import game"
    ]

    def draw_minigame_title():
        title_font = pygame.font.SysFont("Arial", 20)
        title_text = title_font.render("Minigame: Code_race", True, (255, 255, 0))
        screen.blit(title_text, (width - title_text.get_width() - 20, 10))

    def show_dialog():
        screen.fill((0, 0, 0))
        dialog_font = pygame.font.SysFont("Arial", 28)
        text = "Lan göt, bakalım eller ne kadar hızlı, beyin ne kadar çalışıyor..."
        bitrus_scaled = pygame.transform.scale(bitrus_img, (200, 200))
        screen.blit(bitrus_scaled, (width // 2 - 100, 80))

        # Soldan sağa yazma efekti
        x = width // 2
        y = 300
        for i in range(len(text) + 1):
            screen.fill((0, 0, 0))
            screen.blit(bitrus_scaled, (width // 2 - 100, 80))
            draw_minigame_title()
            rendered_text = dialog_font.render(text[:i], True, (255, 255, 255))
            screen.blit(rendered_text, (width // 2 - rendered_text.get_width() // 2, y))
            pygame.display.flip()
            pygame.time.wait(30)
        pygame.time.wait(2000)

    while True:  # oyuncu başaramazsa baştan oynat
        current_round = 0
        show_dialog()

        while current_round < 5:
            screen.fill((0, 0, 0))
            active_snippet = random.choice(code_snippets)
            input_text = ""
            start_time = time.time()
            max_time = 10  # saniye
            running = True

            while running:
                screen.fill((30, 30, 30))
                draw_minigame_title()

                remaining_time = max_time - (time.time() - start_time)
                timer_color = (255, 0, 0) if remaining_time < 3 else (255, 255, 255)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_RETURN:
                            if input_text.strip() == active_snippet.strip():
                                current_round += 1
                                running = False
                            else:
                                # Başarısız → başa dön
                                fail_msg = font.render("Yanlış yazdın! Baştan başla salak!", True, (255, 0, 0))
                                screen.blit(fail_msg, (width // 2 - fail_msg.get_width() // 2, height // 2))
                                pygame.display.flip()
                                pygame.time.wait(2500)
                                running = False
                                current_round = 0
                                break
                        elif event.key == pygame.K_BACKSPACE:
                            input_text = input_text[:-1]
                        else:
                            input_text += event.unicode

                if remaining_time <= 0:
                    fail_msg = font.render("Zaman bitti! gerizekalı aahaaaa Baştan başla!", True, (255, 0, 0))
                    screen.blit(fail_msg, (width // 2 - fail_msg.get_width() // 2, height // 2))
                    pygame.display.flip()
                    pygame.time.wait(2500)
                    current_round = 0
                    break

                snippet_surf = font.render(f"Yaz: {active_snippet}", True, (255, 255, 255))
                input_surf = input_font.render(input_text, True, (0, 255, 0))
                timer_surf = font.render(f"Kalan Süre: {int(remaining_time)}s", True, timer_color)

                screen.blit(snippet_surf, (50, 100))
                screen.blit(input_surf, (50, 160))
                screen.blit(timer_surf, (50, 220))

                pygame.display.flip()
                clock.tick(30)

        # Oyunu başarıyla bitirdi
        screen.fill((0, 0, 0))
        draw_minigame_title()
        success_text = font.render("ahhhhhhh beni sinirlendiriyorsun!", True, (0, 255, 0))
        screen.blit(success_text, (width // 2 - success_text.get_width() // 2, height // 2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break  # başarıyla tamamlandı
