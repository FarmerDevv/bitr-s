import pygame

def start_lab_game(screen, bitrus_img, pc_img):
    pygame.font.init()
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    # Labirent ayarları
    TILE_SIZE = 40
    MAP_WIDTH, MAP_HEIGHT = 30, 20
    
    # Labirent haritası
    labyrinth_map = [
        [1]*30,
        [1,0,0,0,0,0,0,0,1,0,0,2,0,1,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1],
        [1,0,1,1,1,0,1,0,1,0,1,1,0,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,0,1],
        [1,0,1,0,0,0,1,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,1],
        [1,0,1,0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,0,1,0,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1],
        [1,0,1,0,0,0,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1],
        [1,0,0,0,1,0,0,1,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1],
        [1,1,1,0,1,0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1],
        [1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1],
        [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,2,1,0,1,1,1,1,1,0,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,1,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,4],  # Çıkış
        [1]*30
    ]

    # Renkler
    COLOR_BG = (10, 10, 10)
    COLOR_WALL = (100, 50, 50)
    COLOR_PATH = (50, 100, 50)
    COLOR_PC = (50, 150, 200)
    COLOR_SPIKE = (180, 30, 30)
    COLOR_JUMP_BLOCK = (50, 50, 150)
    COLOR_EXIT = (30, 180, 30)

    # PC başlangıç pozisyonu
    pc_x, pc_y = 1, 1

    # Font
    font = pygame.font.SysFont("Arial", 32)

    # Dialog (isteğe bağlı, kaldırabilirsin)
    bitrus_dialog = [
        "Hey, seni uyarmıştım...",
        "Beni çok sinirlendirdin!",
        "Şimdi seni bu mağaraya hapsedeceğim.",
        "Bak bakalım kaçabilir misin...",
        "A, D, W, S ile hareket et, boşluk ile zıpla!",
        "Yeşil çıkışa ulaş yeter, amk zaten başaramazsın!"
    ]
    dialog_index = 0
    dialog_timer = pygame.time.get_ticks()
    dialog_delay = 3000
    in_dialog = True

    # Zıplama değişkenleri
    is_jumping = False
    jump_height = 80
    jump_speed = 8
    jump_offset = 0

    clock = pygame.time.Clock()

    running = True
    while running:
        dt = clock.tick(60)
        screen.fill(COLOR_BG)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # Sadece minigame'i bitir, ana oyuna dön
                running = False

        keys = pygame.key.get_pressed()

        if in_dialog:
            bitrus_scaled = pygame.transform.scale(bitrus_img, (150, 150))
            screen.blit(bitrus_scaled, (WIDTH//2 - 75, HEIGHT//5))

            dialog_rect = pygame.Rect(WIDTH//4, HEIGHT//1.7, WIDTH//2, 100)
            pygame.draw.rect(screen, (40, 40, 40), dialog_rect, border_radius=10)
            pygame.draw.rect(screen, (200, 200, 200), dialog_rect, 3, border_radius=10)

            text_surface = font.render(bitrus_dialog[dialog_index], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=dialog_rect.center)
            screen.blit(text_surface, text_rect)

            if pygame.time.get_ticks() - dialog_timer > dialog_delay:
                dialog_index += 1
                dialog_timer = pygame.time.get_ticks()
                if dialog_index >= len(bitrus_dialog):
                    in_dialog = False

        else:
            # Labirenti çiz
            for y in range(MAP_HEIGHT):
                for x in range(MAP_WIDTH):
                    tile = labyrinth_map[y][x]
                    rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    if tile == 1:
                        pygame.draw.rect(screen, COLOR_WALL, rect)
                    elif tile == 2:
                        pygame.draw.rect(screen, COLOR_SPIKE, rect)
                    elif tile == 3:
                        pygame.draw.rect(screen, COLOR_JUMP_BLOCK, rect)
                    elif tile == 4:
                        pygame.draw.rect(screen, COLOR_EXIT, rect)
                    else:
                        pygame.draw.rect(screen, COLOR_PATH, rect)

            # PC hareketi
            if not is_jumping:
                new_x, new_y = pc_x, pc_y
                if keys[pygame.K_a]:
                    new_x -= 1
                elif keys[pygame.K_d]:
                    new_x += 1
                elif keys[pygame.K_w]:
                    new_y -= 1
                elif keys[pygame.K_s]:
                    new_y += 1

                if 0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT:
                    if labyrinth_map[new_y][new_x] in (0, 4):
                        pc_x, pc_y = new_x, new_y

                # Boşluk ile zıplama kontrolü
                if keys[pygame.K_SPACE]:
                    front_x = pc_x + 1
                    if front_x < MAP_WIDTH and labyrinth_map[pc_y][front_x] == 3:
                        is_jumping = True
                        jump_offset = 0

            # Zıplama hareketi
            if is_jumping:
                jump_offset += jump_speed
                if jump_offset > jump_height:
                    is_jumping = False
                    jump_offset = 0

            # Diken kontrolü
            if labyrinth_map[pc_y][pc_x] == 2:
                pc_x, pc_y = 1, 1
                is_jumping = False
                jump_offset = 0

            # Çıkış kontrolü
            if labyrinth_map[pc_y][pc_x] == 4:
                screen.fill(COLOR_BG)
                win_font = pygame.font.SysFont("Arial", 48)
                win_text = win_font.render("Amk be, çıkışı buldun!", True, (0, 255, 0))
                screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, HEIGHT//2 - win_text.get_height()//2))
                pygame.display.flip()
                pygame.time.wait(3000)
                running = False  # Burada oyun kapanmaz, minigame biter.

            # PC pozisyonu ve çizimi
            pc_screen_x = pc_x * TILE_SIZE
            pc_screen_y = pc_y * TILE_SIZE - jump_offset

            if pc_img:
                pc_scaled = pygame.transform.scale(pc_img, (TILE_SIZE, TILE_SIZE))
                screen.blit(pc_scaled, (pc_screen_x, pc_screen_y))
            else:
                pygame.draw.rect(screen, COLOR_PC, (pc_screen_x, pc_screen_y, TILE_SIZE, TILE_SIZE))

        pygame.display.flip()

    # Minigame bitti, fonksiyondan çıkıyoruz.
