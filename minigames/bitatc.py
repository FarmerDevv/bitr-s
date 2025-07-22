import pygame
import random
import time

def start_bitrus_attack(screen, bitrus_img, pc_img):
    pygame.font.init()
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    font_big = pygame.font.SysFont("Arial", 48)
    font_small = pygame.font.SysFont("Arial", 28)

    # PC ve Bitrüs resimlerini ölçekle
    pc_img_scaled = pygame.transform.scale(pc_img, (200, 150))
    bitrus_img_scaled = pygame.transform.scale(bitrus_img, (80, 80))
    mini_bitrus_img = pygame.transform.scale(bitrus_img, (40, 40))

    # PC pozisyonu (ekranın altında ortada)
    pc_pos = pygame.Rect(WIDTH // 2 - pc_img_scaled.get_width() // 2, HEIGHT - 180, pc_img_scaled.get_width(), pc_img_scaled.get_height())

    # Cutscene için Bitrüs başlangıç pozisyonu
    cutscene_pos = [-100, HEIGHT - 200]
    cutscene_target_y = HEIGHT // 3

    # Cutscene metni
    cutscene_text = "Bilgisayarın gerçekten patlıcak ahah çünkü beni çok sinir ediyorsun"
    text_render = font_small.render(cutscene_text, True, (255, 0, 0))

    # Mini Bitrüs listesi
    mini_bitrus_list = []

    # Durum değişkenleri
    in_cutscene = True
    running = True
    cutscene_speed = 150
    spawn_delay = 600
    last_spawn_time = 0

    GAME_DURATION = 30  # saniye
    game_start_time = None

    while running:
        dt = clock.tick(60) / 1000  # Delta time (saniye)

        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not in_cutscene:
                mx, my = event.pos
                for mini in mini_bitrus_list[:]:
                    rect = pygame.Rect(mini[0], mini[1], 40, 40)
                    if rect.collidepoint(mx, my):
                        mini_bitrus_list.remove(mini)

        if in_cutscene:
            # Bitrüs yukarı doğru gidiyor
            cutscene_pos[0] += cutscene_speed * dt
            cutscene_pos[1] -= cutscene_speed * dt

            screen.blit(bitrus_img_scaled, (int(cutscene_pos[0]), int(cutscene_pos[1])))
            screen.blit(text_render, (WIDTH // 2 - text_render.get_width() // 2, 50))

            if cutscene_pos[1] <= cutscene_target_y:
                in_cutscene = False
                last_spawn_time = pygame.time.get_ticks()
                game_start_time = time.time()  # sayaç başlat
        else:
            # Oyun sahnesi aktif
            screen.blit(pc_img_scaled, pc_pos.topleft)

            now = pygame.time.get_ticks()
            if now - last_spawn_time > spawn_delay:
                spawn_x = random.randint(0, WIDTH - 40)
                spawn_y = -40
                speed = random.uniform(150, 250)
                mini_bitrus_list.append([spawn_x, spawn_y, speed])
                last_spawn_time = now

            # Mini Bitrüs hareketi ve çarpışma kontrolü
            for mini in mini_bitrus_list[:]:
                mini[1] += mini[2] * dt
                screen.blit(mini_bitrus_img, (mini[0], mini[1]))

                mini_rect = pygame.Rect(mini[0], mini[1], 40, 40)
                if mini_rect.colliderect(pc_pos):
                    # Çarptı, oyun başa dönüyor
                    in_cutscene = True
                    cutscene_pos = [-100, HEIGHT - 200]
                    mini_bitrus_list.clear()
                    game_start_time = None  # sayaç sıfırla

        # Sayaç göster
        if not in_cutscene and game_start_time:
            elapsed = time.time() - game_start_time
            remaining = max(0, int(GAME_DURATION - elapsed))
            timer_text = font_small.render(f"Kalan Süre: {remaining}", True, (255, 255, 255))
            screen.blit(timer_text, (10, 10))

            if remaining <= 0:
                # Süre bitti, oyun başarılı tamamlandı
                win_text = font_big.render("ahhhhhhhhhhhhhhhhhhhh nasıl yaptın yaaa bunu amk Bilgisayarını  korudun!", True, (0, 255, 0))
                screen.blit(win_text, (WIDTH // 2 - win_text.get_width() // 2, HEIGHT // 2))
                pygame.display.flip()
                pygame.time.wait(4000)
                return

        pygame.display.flip()
