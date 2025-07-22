import pygame 
import sys
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def start_virus_defense(screen, virus_img, wantvirus_img):
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 32)
    big_font = pygame.font.SysFont("Arial", 48)
    dialog_font = pygame.font.SysFont("Arial", 28)

    # Sağ üstte minigame başlığı
    def draw_minigame_title():
        title_font = pygame.font.SysFont("Arial", 20)
        title_text = title_font.render("Minigame: Virüs_Defense", True, (255, 255, 0))
        screen.blit(title_text, (WIDTH - title_text.get_width() - 20, 10))

    # Soldan sağa kayan yazı için fonksiyon
    def draw_typing_text_with_image(text, x, y, font, surface, img, img_x, img_y, speed=2):
        chars_to_show = 0
        frame_counter = 0
        done = False
        clock_typing = pygame.time.Clock()

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            surface.fill(BLACK)
            draw_minigame_title()

            # Resmi çiz
            surface.blit(img, (img_x, img_y))

            if frame_counter % speed == 0 and chars_to_show < len(text):
                chars_to_show += 1

            rendered_text = font.render(text[:chars_to_show], True, WHITE)
            surface.blit(rendered_text, (x, y))

            pygame.display.flip()
            frame_counter += 1
            clock_typing.tick(60)

            if chars_to_show == len(text):
                pygame.time.wait(1500)  # tamamlanınca 1.5 saniye bekle
                done = True

    # Virüs saldırısı animasyonu
    def virus_attack():
        x = -virus_img.get_width()
        y = HEIGHT//2 - virus_img.get_height()//2
        speed = 5
        show_text_animation = True  # Yazı animasyonunu sadece 1 kere göster

        text = "Bitrüsler bilgisayarına saldırıyor!"
        chars_to_show = 0
        frame_counter = 0

        while x < WIDTH//2 - virus_img.get_width()//2:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BLACK)
            draw_minigame_title()
            screen.blit(virus_img, (x, y))

            # Yazı animasyonu sadece başta
            if show_text_animation:
                if frame_counter % 2 == 0 and chars_to_show < len(text):
                    chars_to_show += 1
                rendered_text = big_font.render(text[:chars_to_show], True, RED)
                screen.blit(rendered_text, (WIDTH//2 - rendered_text.get_width()//2, 100))

                if chars_to_show == len(text):
                    # Yazı tamamlandı, bundan sonra hep tam yazıyı göster
                    show_text_animation = False
            else:
                # Yazı tamamlandıktan sonra tam yazı göster
                rendered_text = big_font.render(text, True, RED)
                screen.blit(rendered_text, (WIDTH//2 - rendered_text.get_width()//2, 100))

            x += speed
            frame_counter += 1

            pygame.display.flip()
            clock.tick(60)

    class MathQuiz:
        def __init__(self):
            self.screen = screen
            self.font = font
            self.questions = self.generate_questions()
            self.current_q = 0
            self.user_input = ""
            self.correct = 0

        def generate_questions(self):
            q_list = []
            for _ in range(2):
                a = random.randint(1, 20)
                b = random.randint(1, 20)
                op = random.choice(["+", "-", "*"])
                if op == "+":
                    ans = a + b
                elif op == "-":
                    ans = a - b
                else:
                    ans = a * b
                q_list.append((f"{a} {op} {b} = ?", ans))
            return q_list

        def run(self):
            running = True
            while running:
                self.screen.fill(BLACK)
                draw_minigame_title()

                question, answer = self.questions[self.current_q]

                q_text = self.font.render(f"Soru {self.current_q+1}: {question}", True, WHITE)
                self.screen.blit(q_text, (WIDTH//2 - q_text.get_width()//2, HEIGHT//3))

                input_text = self.font.render(self.user_input, True, WHITE)
                self.screen.blit(input_text, (WIDTH//2 - input_text.get_width()//2, HEIGHT//3 + 50))

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_BACKSPACE:
                            self.user_input = self.user_input[:-1]
                        elif event.key == pygame.K_RETURN:
                            try:
                                if int(self.user_input) == answer:
                                    self.correct += 1
                                self.user_input = ""
                                self.current_q += 1
                                if self.current_q >= len(self.questions):
                                    running = False
                            except:
                                self.user_input = ""
                        else:
                            if event.unicode.isdigit() or (event.unicode == '-' and len(self.user_input) == 0):
                                self.user_input += event.unicode

                pygame.display.flip()
                clock.tick(60)
            return self.correct == len(self.questions)

    while True:
        virus_attack()

        want_text = "Bitrüsleri temizlemek için matematik sorularını doğru cevaplaki wantivirüs proglamı çalışsın!"
        # İkonu ve animasyonlu yazıyı birlikte göster
        draw_typing_text_with_image(
            want_text,
            WIDTH//2 - 200, HEIGHT//4, 
            font, 
            screen, 
            wantvirus_img, 
            WIDTH//2 - wantvirus_img.get_width() - 250, HEIGHT//4 - wantvirus_img.get_height()//2
        )

        quiz = MathQuiz()
        success = quiz.run()

        screen.fill(BLACK)
        draw_minigame_title()

        if success:
            draw_typing_text_with_image(
                "ahhh göte bala buldun salak kendini bir şey sanma!",
                WIDTH//2 - 300, HEIGHT//2 - 20,
                big_font,
                screen,
                virus_img,
                WIDTH//2 - virus_img.get_width() - 350,
                HEIGHT//2 - virus_img.get_height()//2
            )
            break  # doğru yaptıysa döngüden çık
        else:
            draw_typing_text_with_image(
                "Başarısız oldun! hahaha tekrar dene!",
                WIDTH//2 - 200, HEIGHT//2 - 20,
                big_font,
                screen,
                virus_img,
                WIDTH//2 - virus_img.get_width() - 250,
                HEIGHT//2 - virus_img.get_height()//2
            )
            pygame.time.wait(1000)
