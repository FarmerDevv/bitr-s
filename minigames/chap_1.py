import pygame
import time
import os
import sys

def start_chap_1(screen, bitrus_img):
    pygame.font.init()
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Arial", 48)
    font_medium = pygame.font.SysFont("Arial", 32)
    font_small = pygame.font.SysFont("Arial", 24)
    font_input = pygame.font.SysFont("Segoe UI", 28)

    ASSETS_DIR = "assets/pixel_art"
    bg_path = os.path.join(ASSETS_DIR, "xp_background.jpg")
    background = pygame.image.load(bg_path)
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    bitrus_scaled = pygame.transform.scale(bitrus_img, (200, 200))

    anti_icon_path = os.path.join(ASSETS_DIR, "anti.png")
    anti_icon = pygame.image.load(anti_icon_path)
    anti_icon = pygame.transform.scale(anti_icon, (80, 80))
    anti_icon_rect = anti_icon.get_rect(topleft=(10, 10))

    state = "cutscene"

    cutscene_dialogs = [
        "Ahhh çok hasar aldım ama asla pes etmeyeceğim!",
        "Sen: Çok mu hasar aldın?",
        "Neden sordun salak",
        "Sen: ahaa aklıma birşey geldi",
        "Sen: Antivirüs kurmalıyım!"
    ]
    dialog_index = 0
    dialog_timer = pygame.time.get_ticks()
    dialog_delay = 3500

    user_input = ""
    search_error = ""

    options = [
        {"text": "fullbeleşantivirüsindir", "desc": "En iyi antivirüs, tam koruma sağlar.", "correct": True},
        {"text": "profantivirüsindir", "desc": "profosyonel antivirüs harika koua :).", "correct": False}
    ]

    selected_option = None
    show_results = False

    cleaning = False
    cleaning_start_time = 0
    cleaning_duration = 5

    final_dialog = "Aaahh şerefsiz!!!"
    final_dialog_show_time = 0
    final_dialog_duration = 3000

    malware_show_time = 0
    malware_duration = 5000

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if state == "cutscene":
                pass

            elif state == "search":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        user_input = user_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if user_input.lower() == "antivirüs kur":
                            show_results = True
                            search_error = ""
                            state = "show_results"
                        else:
                            search_error = "Geçersiz arama! Tam yaz 'antivirüs kur'."
                            user_input = ""
                    else:
                        if len(user_input) < 30 and event.unicode.isprintable():
                            user_input += event.unicode

            elif state == "show_results":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    option1_rect = pygame.Rect(WIDTH*0.2 + 10, HEIGHT//2 + 20, WIDTH*0.6 - 20, 40)
                    option2_rect = pygame.Rect(WIDTH*0.2 + 10, HEIGHT//2 + 80, WIDTH*0.6 - 20, 40)

                    if option1_rect.collidepoint(mx, my):
                        selected_option = options[0]
                        if selected_option["correct"]:
                            state = "antivirus_icon"
                        else:
                            state = "malware"
                            malware_show_time = pygame.time.get_ticks()
                    elif option2_rect.collidepoint(mx, my):
                        selected_option = options[1]
                        if selected_option["correct"]:
                            state = "antivirus_icon"
                        else:
                            state = "malware"
                            malware_show_time = pygame.time.get_ticks()

            elif state == "antivirus_icon":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    if anti_icon_rect.collidepoint(mx, my):
                        state = "cleaning"
                        cleaning = True
                        cleaning_start_time = time.time()

            elif state == "cleaning":
                pass

            elif state == "finale":
                pass

            elif state == "malware":
                pass

        screen.blit(background, (0, 0))

        if state == "cutscene":
            screen.blit(bitrus_scaled, (WIDTH//2 - bitrus_scaled.get_width()//2, HEIGHT//4))
            if dialog_index < len(cutscene_dialogs):
                text_surface = font_medium.render(cutscene_dialogs[dialog_index], True, (255, 255, 255))
                text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
                screen.blit(text_surface, text_rect)
                if pygame.time.get_ticks() - dialog_timer > dialog_delay:
                    dialog_index += 1
                    dialog_timer = pygame.time.get_ticks()
            else:
                state = "search"

        elif state == "search":
            box_w, box_h = WIDTH*0.6, 50
            box_x, box_y = WIDTH*0.2, HEIGHT*0.4
            pygame.draw.rect(screen, (255,255,255), (box_x, box_y, box_w, box_h), border_radius=10)
            pygame.draw.rect(screen, (200,200,200), (box_x, box_y, box_w, box_h), 2, border_radius=10)
            input_surface = font_input.render(user_input, True, (0,0,0))
            screen.blit(input_surface, (box_x+15, box_y + (box_h - input_surface.get_height())//2))
            if search_error:
                err_surface = font_small.render(search_error, True, (255, 0, 0))
                screen.blit(err_surface, (box_x, box_y + box_h + 10))

        elif state == "show_results":
            results_x, results_y = WIDTH*0.2, HEIGHT//2 + 20
            results_w, results_h = WIDTH*0.6, 120
            pygame.draw.rect(screen, (255,255,255), (results_x, results_y, results_w, results_h), border_radius=10)
            pygame.draw.rect(screen, (200,200,200), (results_x, results_y, results_w, results_h), 2, border_radius=10)

            option1_rect = pygame.Rect(results_x + 10, results_y + 10, results_w - 20, 40)
            option2_rect = pygame.Rect(results_x + 10, results_y + 70, results_w - 20, 40)

            pygame.draw.rect(screen, (230, 230, 230), option1_rect, border_radius=8)
            pygame.draw.rect(screen, (230, 230, 230), option2_rect, border_radius=8)

            opt1_text = font_medium.render(options[0]["text"], True, (0,0,0))
            opt2_text = font_medium.render(options[1]["text"], True, (0,0,0))
            screen.blit(opt1_text, (option1_rect.x + 10, option1_rect.y + 5))
            screen.blit(opt2_text, (option2_rect.x + 10, option2_rect.y + 5))

            desc1_surf = font_small.render(options[0]["desc"], True, (50,50,50))
            desc2_surf = font_small.render(options[1]["desc"], True, (50,50,50))
            screen.blit(desc1_surf, (option1_rect.x + 10, option1_rect.bottom + 2))
            screen.blit(desc2_surf, (option2_rect.x + 10, option2_rect.bottom + 2))

        elif state == "antivirus_icon":
            screen.blit(anti_icon, anti_icon_rect)
            info_text = font_small.render("İkona tıklayın, virüsleri kaldırmak için.", True, (255,255,255))
            screen.blit(info_text, (10, 100))

        elif state == "cleaning":
            elapsed = time.time() - cleaning_start_time
            progress = min(1, elapsed / cleaning_duration)

            bar_w, bar_h = WIDTH//2, 30
            bar_x, bar_y = WIDTH//2 - bar_w//2, HEIGHT//2 - bar_h//2
            pygame.draw.rect(screen, (50,50,50), (bar_x, bar_y, bar_w, bar_h))
            pygame.draw.rect(screen, (0,200,0), (bar_x, bar_y, int(bar_w * progress), bar_h))

            progress_text = font_small.render(f"Virüsler temizleniyor... %{int(progress*100)}", True, (255,255,255))
            text_rect = progress_text.get_rect(center=(WIDTH//2, bar_y - 30))
            screen.blit(progress_text, text_rect)

            if progress >= 1:
                cleaning = False
                state = "finale"
                final_dialog_show_time = pygame.time.get_ticks()

        elif state == "finale":
            screen.blit(bitrus_scaled, (WIDTH//2 - bitrus_scaled.get_width()//2, HEIGHT//4))
            final_text = font_big.render(final_dialog, True, (255, 0, 0))
            text_rect = final_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))
            screen.blit(final_text, text_rect)

            if pygame.time.get_ticks() - final_dialog_show_time > final_dialog_duration:
                return

        elif state == "malware":
            screen.fill((0,0,0))
            malware_text = font_big.render("!!! MALWARE İNDİRİLDİ !!!", True, (255, 0, 0))
            malware_rect = malware_text.get_rect(center=(WIDTH//2, HEIGHT//3))
            screen.blit(malware_text, malware_rect)

            warning_text = font_medium.render("Sistem bozuldu, yeniden başlatılıyor...", True, (255, 100, 0))
            warning_rect = warning_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(warning_text, warning_rect)

            offset = 5 if (pygame.time.get_ticks() // 300) % 2 == 0 else -5
            shake_rect = pygame.Rect(WIDTH//4 + offset, HEIGHT//4 + offset, WIDTH//2, HEIGHT//2)
            pygame.draw.rect(screen, (255, 0, 0), shake_rect, 5)

            if pygame.time.get_ticks() - malware_show_time > malware_duration:
                # Yanlış seçimde minigame baştan başlasın
                return start_chap_1(screen, bitrus_img)

        pygame.display.flip()
