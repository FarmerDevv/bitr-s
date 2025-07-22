import pygame
import random
import time
import math

pygame.init()

WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

CABLE_COLORS = [(255, 0, 0), (0, 255, 0), (0, 150, 255), (255, 255, 0)]

font = pygame.font.SysFont("consolas", 32)
big_font = pygame.font.SysFont("consolas", 64)

pitrus_img = pygame.image.load("assets/pixel_art/pitrüs.png")
pitrus_img = pygame.transform.scale(pitrus_img, (200, 200))

dialogs = [
    "Hey! Bu bilgisayarda bağlantılar kopmuş.",
    "Kabloları doğru renklere göre bağla!",
    "Dikkatli ol, her renk sadece bir kez kullanılabilir.",
    "Hazırsan başla!"
]

def draw_dialog_box(screen, text, progress=1.0):
    pygame.draw.rect(screen, BLACK, (100, HEIGHT - 160, WIDTH - 200, 120))
    pygame.draw.rect(screen, WHITE, (100, HEIGHT - 160, WIDTH - 200, 120), 3)
    # Animasyonlu yazı:
    length = int(len(text) * progress)
    rendered = font.render(text[:length], True, WHITE)
    screen.blit(rendered, (120, HEIGHT - 130))

def draw_cable_sockets(screen, positions, side):
    for i, pos in enumerate(positions):
        color = CABLE_COLORS[i]
        if side == "left":
            pygame.draw.circle(screen, color, (150, pos), 20)
        else:
            pygame.draw.circle(screen, color, (WIDTH - 150, pos), 20)

def lerp(a, b, t):
    return a + (b - a) * t

def screen_shake(screen, intensity=10, duration=0.5):
    clock = pygame.time.Clock()
    start_time = time.time()
    base_surf = screen.copy()
    while time.time() - start_time < duration:
        offset_x = random.randint(-intensity, intensity)
        offset_y = random.randint(-intensity, intensity)
        screen.fill(BLACK)
        screen.blit(base_surf, (offset_x, offset_y))
        pygame.display.flip()
        clock.tick(60)

def electric_flash(screen, positions_left, positions_right, connections):
    clock = pygame.time.Clock()
    flash_duration = 1.0
    start_time = time.time()
    while time.time() - start_time < flash_duration:
        screen.fill(GRAY)
        pygame.draw.rect(screen, BLACK, (100, 100, WIDTH - 200, HEIGHT - 250))
        pygame.draw.rect(screen, WHITE, (100, 100, WIDTH - 200, HEIGHT - 250), 3)
        draw_cable_sockets(screen, positions_left, "left")
        draw_cable_sockets(screen, positions_right, "right")
        # Elektrik çizgileri
        flash_color = YELLOW if int((time.time() * 10) % 2) == 0 else WHITE
        for left_idx, right_idx in connections.items():
            start_pos = (150, positions_left[left_idx])
            end_pos = (WIDTH - 150, positions_right[right_idx])
            pygame.draw.line(screen, flash_color, start_pos, end_pos, 5)
        pygame.display.flip()
        clock.tick(30)

def start_cable_game(screen):
    clock = pygame.time.Clock()

    dialog_index = 0
    dialog_start_time = time.time()
    dialog_duration = 4  # saniye

    cable_positions_left = [200, 300, 400, 500]
    cable_positions_right = cable_positions_left.copy()
    random.shuffle(cable_positions_right)

    # Bağlantı durumu: left_idx -> right_idx
    connections = {}

    # Kabloların pozisyonları ve sürüklenme durumu
    cables = []
    for i, y in enumerate(cable_positions_left):
        cables.append({
            "color": CABLE_COLORS[i],
            "start_pos": (150, y),
            "current_pos": (150, y),
            "dragging": False,
            "connected_to": None,  # sağdaki index
            "left_idx": i
        })

    # Sağ soketlerin dikdörtgen alanları (bağlanmak için)
    right_sockets = []
    for y in cable_positions_right:
        right_sockets.append(pygame.Rect(WIDTH - 170, y - 20, 40, 40))

    in_dialog = True
    running = True

    # Yazı animasyonu kontrolü için
    anim_progress = 0.0
    anim_speed = 0.03

    while running:
        dt = clock.tick(60) / 1000  # saniye cinsinden delta time
        screen.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if not in_dialog:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for cable in cables:
                        cx, cy = cable["current_pos"]
                        dist = math.hypot(mx - cx, my - cy)
                        if dist < 20:
                            cable["dragging"] = True
                            break

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    for cable in cables:
                        if cable["dragging"]:
                            cable["dragging"] = False
                            mx, my = pygame.mouse.get_pos()
                            # Sağ soketlere bak
                            snapped = False
                            for idx, rect in enumerate(right_sockets):
                                if rect.collidepoint(mx, my):
                                    # Eğer o sağ soket başka kabloya bağlıysa iptal et
                                    if idx in connections.values():
                                        break
                                    # Bağlanabilir
                                    cable["connected_to"] = idx
                                    connections[cable["left_idx"]] = idx
                                    # Kablo pozisyonunu sağ soketin tam ortasına getir
                                    cable["current_pos"] = (rect.centerx, rect.centery)
                                    snapped = True
                                    break
                            if not snapped:
                                # Bağlantı iptal, başlangıç noktasına dön
                                if cable["connected_to"] is not None:
                                    connections.pop(cable["left_idx"], None)
                                cable["connected_to"] = None
                                cable["current_pos"] = cable["start_pos"]

                if event.type == pygame.MOUSEMOTION:
                    for cable in cables:
                        if cable["dragging"]:
                            cable["current_pos"] = event.pos

        if in_dialog:
            screen.blit(pitrus_img, ((WIDTH - 200) // 2, 50))
            anim_progress += anim_speed
            if anim_progress > 1:
                anim_progress = 1
            draw_dialog_box(screen, dialogs[dialog_index], anim_progress)

            # 4 saniye geçince sonraki dialog
            if time.time() - dialog_start_time > dialog_duration:
                dialog_index += 1
                dialog_start_time = time.time()
                anim_progress = 0
                if dialog_index >= len(dialogs):
                    in_dialog = False
        else:
            # Elektrik kutusu çizimi
            pygame.draw.rect(screen, BLACK, (100, 100, WIDTH - 200, HEIGHT - 250))
            pygame.draw.rect(screen, WHITE, (100, 100, WIDTH - 200, HEIGHT - 250), 3)

            # Sol ve sağ soketler
            draw_cable_sockets(screen, cable_positions_left, "left")
            draw_cable_sockets(screen, cable_positions_right, "right")

            # Kabloları çiz
            for cable in cables:
                # Kablo çizgisi sol soketten current_pos'a
                start_pos = cable["start_pos"]
                end_pos = cable["current_pos"]
                pygame.draw.line(screen, cable["color"], start_pos, end_pos, 8)
                # Kablo ucu dairesi
                pygame.draw.circle(screen, cable["color"], (int(end_pos[0]), int(end_pos[1])), 15)

            # Tüm bağlantı doğru mu kontrolü
            if len(connections) == len(cables):
                # Her bir bağlantı için sol ve sağ renkler eşleşmeli
                all_correct = True
                for left_idx, right_idx in connections.items():
                    if CABLE_COLORS[left_idx] != CABLE_COLORS[right_idx]:
                        all_correct = False
                        break
                if all_correct:
                    electric_flash(screen, cable_positions_left, cable_positions_right, connections)
                    msg = big_font.render("BAŞARILI!", True, (0, 255, 0))
                    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    running = False
                else:
                    # Yanlış bağlantı titremesi
                    screen_shake(screen)
                    # Yanlış bağlantı mesajı
                    msg = big_font.render("YANLIŞ BAĞLANTI!", True, RED)
                    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
                    pygame.display.flip()
                    pygame.time.wait(1500)
                    # Bağlantıları sıfırla
                    for cable in cables:
                        cable["connected_to"] = None
                        cable["current_pos"] = cable["start_pos"]
                    connections.clear()

        pygame.display.update()

