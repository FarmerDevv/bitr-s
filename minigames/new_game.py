import pygame 
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def start_new_game(screen, bitrus_img):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)
    big_font = pygame.font.SysFont("Arial", 40)

    intro_texts = [
        "Bitrüs: Hey gerizekalı.",
        "Bitrüs: Sistemin virüslü, şimdi yeni testim var!",
        "Bitrüs: Sistem dosyalarını kopyaladım, biri sahte.",
        "Bitrüs: Sana sorular soracağım, yanlış olanı silmelisin.",
        "Bitrüs: Doğruyu silersen test devam eder.",
        "Bitrüs: Yanlış seçersen sistem çöker!",
        "Bitrüs: Kontroller: Yukarı/Aşağı okları ile seçim yap, Enter ile onayla.",
        "Bitrüs: Hazırsan başlamak için bir tuşa bas!"
    ]

    def draw_typing_text(surface, text, x, y, font, color=WHITE, delay=15):
        for i in range(len(text) + 1):
            rendered = font.render(text[:i], True, color)
            surface.blit(rendered, (x, y))
            pygame.display.flip()
            pygame.time.wait(delay)

    def draw_intro(selected_line):
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(bitrus_img, (300, 300)), (WIDTH//2 - 150, 50))

        # Sağ üst köşeye "Minigame: new_game" yazısı
        title_text = font.render("Minigame: new_game", True, WHITE)
        screen.blit(title_text, (WIDTH - title_text.get_width() - 20, 20))

        y = 380
        for i, line in enumerate(intro_texts):
            color = GREEN if i == selected_line else WHITE
            rendered = font.render(line, True, color)
            screen.blit(rendered, (50, y + i * 35))
        pygame.display.flip()

    selected_intro = 0
    intro_done = False
    intro_typed_once = False

    while not intro_done:
        if not intro_typed_once:
            screen.fill(BLACK)
            screen.blit(pygame.transform.scale(bitrus_img, (300, 300)), (WIDTH//2 - 150, 50))

            # Sağ üst köşeye "Minigame: new_game" yazısı
            title_text = font.render("Minigame: new_game", True, WHITE)
            screen.blit(title_text, (WIDTH - title_text.get_width() - 20, 20))

            for i, line in enumerate(intro_texts):
                color = GREEN if i == selected_intro else WHITE
                draw_typing_text(screen, line, 50, 380 + i*35, font, color, delay=5)
            intro_typed_once = True
        else:
            draw_intro(selected_intro)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_intro = (selected_intro - 1) % len(intro_texts)
                elif event.key == pygame.K_DOWN:
                    selected_intro = (selected_intro + 1) % len(intro_texts)
                else:
                    intro_done = True
        clock.tick(30)

    questions = [
        ("Windows sistem dosyaları genellikle hangi klasördedir?", 
         ["C:\\Windows\\System32", "C:\\Program Files", "C:\\Users", "D:\\Backup"], 0),

        ("Hangi dosya uzantısı Python dosyasıdır?", 
         [".exe", ".py", ".txt", ".dll"], 1),

        ("RAM ne işe yarar?", 
         ["Veri depolama", "Geçici hafıza", "Ekran kartı", "İşlemci"], 1),

        ("Hangisi bir işlemci markasıdır?", 
         ["Intel", "Nvidia", "Samsung", "Seagate"], 0),

        ("Hangisi dosya sisteminde kullanılır?", 
         ["GUID Partition Table", "HTML", "JPEG", "MP3"], 0)
    ]

    current_q = 0
    message = ""
    game_over = False
    shown_questions = {}

    def draw_question(q_text, options, selected, error_msg=None):
        screen.fill(BLACK)
        screen.blit(pygame.transform.scale(bitrus_img, (300, 300)), (WIDTH//2 - 150, 50))

        # Sağ üst köşeye "Minigame: new_game" yazısı
        title_text = font.render("Minigame: choose_correct", True, WHITE)
        screen.blit(title_text, (WIDTH - title_text.get_width() - 20, 20))

        if current_q not in shown_questions:
            draw_typing_text(screen, q_text, WIDTH//2 - font.size(q_text)[0]//2, 380, font)
            shown_questions[current_q] = True
        else:
            question_render = font.render(q_text, True, WHITE)
            screen.blit(question_render, (WIDTH//2 - question_render.get_width()//2, 380))

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            option_text = f"{i+1}. {option}"
            option_render = font.render(option_text, True, color)
            screen.blit(option_render, (WIDTH//2 - option_render.get_width()//2, 430 + i*40))

        if error_msg:
            error_render = big_font.render(error_msg, True, RED)
            screen.blit(error_render, (WIDTH//2 - error_render.get_width()//2, HEIGHT - 100))
        elif message:
            msg_render = big_font.render(message, True, GREEN)
            screen.blit(msg_render, (WIDTH//2 - msg_render.get_width()//2, HEIGHT - 100))

        pygame.display.flip()

    selected_option = 0
    show_error = False
    error_timer_start = 0
    ERROR_DISPLAY_TIME = 2000  # ms

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN and not show_error:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(questions[current_q][1])
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(questions[current_q][1])
                elif event.key == pygame.K_RETURN:
                    correct_index = questions[current_q][2]
                    if selected_option == correct_index:
                        current_q += 1
                        message = "Şanslısın lan eşşek nerden buldun bu şansı!"
                        if current_q == len(questions):
                            screen.fill(BLACK)
                            win_msg = "! Testi geçtin gavat!"
                            draw_typing_text(screen, win_msg, WIDTH//2 - big_font.size(win_msg)[0]//2, HEIGHT//2, big_font, GREEN)
                            pygame.display.flip()
                            pygame.time.wait(4000)
                            return
                        else:
                            selected_option = 0
                    else:
                        show_error = True
                        error_timer_start = pygame.time.get_ticks()
                        current_q = 0
                        selected_option = 0
                        shown_questions.clear()

        if show_error:
            elapsed = pygame.time.get_ticks() - error_timer_start
            if elapsed > ERROR_DISPLAY_TIME:
                show_error = False
                message = ""
            draw_question(questions[current_q][0], questions[current_q][1], selected_option, error_msg="Yanlış yaptın, başa döndün salak!")
        else:
            draw_question(questions[current_q][0], questions[current_q][1], selected_option)

        clock.tick(60)
