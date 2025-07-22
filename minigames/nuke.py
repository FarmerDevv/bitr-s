import pygame
import os
import random
import time

ASSETS_DIR = "assets/pixel_art"
bg_path = os.path.join(ASSETS_DIR, "xp_background.jpg")
nuke_sound_path = os.path.join(ASSETS_DIR, "nuke.mp3")
credits_music_path = os.path.join(ASSETS_DIR, "credits_theme.mp3")  # GTA tarzı fon müzik

dialogues = [
    "Bitrüs: Ahhh... ahhhh...",
    "Bitrüs: Bu... bir son değil...",
    "Bitrüs: BU BİR SON DEĞİL!!!"
]

particles = []

def draw_dialog_bar(screen, text, alpha):
    s = pygame.Surface((800, 100), pygame.SRCALPHA)
    s.fill((20, 20, 20, alpha))
    pygame.draw.rect(s, (80, 80, 80), s.get_rect(), 3, border_radius=10)
    screen.blit(s, (100, 450))

    font = pygame.font.SysFont("arial", 24, bold=True)
    rendered_text = font.render(text, True, (255, 255, 255))
    screen.blit(rendered_text, (120, 480))

def create_particles(center):
    for _ in range(50):  # Turuncu alev partikülleri
        particles.append({
            "pos": list(center),
            "vel": [random.uniform(-6, 6), random.uniform(-6, 6)],
            "radius": random.randint(3, 6),
            "color": (255, random.randint(100, 180), 0),
            "life": random.randint(40, 60),
            "type": "fire"
        })
    for _ in range(30):  # Kan partikülleri
        particles.append({
            "pos": list(center),
            "vel": [random.uniform(-3, 3), random.uniform(-3, 3)],
            "radius": random.randint(4, 7),
            "color": random.choice([(180, 0, 0), (120, 0, 0), (200, 20, 20)]),
            "life": random.randint(80, 100),
            "type": "blood"
        })
    for _ in range(15):  # Bitrüs parçaları
        particles.append({
            "pos": list(center),
            "vel": [random.uniform(-2, 2), random.uniform(-2, 2)],
            "radius": random.randint(6, 12),
            "color": random.choice([(100, 255, 100), (150, 150, 150), (80, 180, 80)]),
            "life": random.randint(70, 90),
            "type": "bitrus"
        })

def update_particles(screen):
    for p in particles[:]:
        p["pos"][0] += p["vel"][0]
        p["pos"][1] += p["vel"][1]
        p["life"] -= 1

        if p["type"] == "fire":
            p["radius"] *= 0.93
        elif p["type"] == "blood":
            p["radius"] *= 0.98
        elif p["type"] == "bitrus":
            p["radius"] *= 0.97

        if p["life"] <= 0 or p["radius"] <= 0.5:
            particles.remove(p)
            continue

        alpha = max(30, min(255, int(255 * (p["life"]/100))))
        surf = pygame.Surface((int(p["radius"]*2), int(p["radius"]*2)), pygame.SRCALPHA)
        pygame.draw.circle(surf, (*p["color"], alpha), (int(p["radius"]), int(p["radius"])), int(p["radius"]))
        screen.blit(surf, (int(p["pos"][0] - p["radius"]), int(p["pos"][1] - p["radius"])))

def screen_shake(amount):
    return random.randint(-amount, amount), random.randint(-amount, amount)

def fade_text(screen, text, duration, font_size=60):
    font = pygame.font.SysFont("arial", font_size, bold=True)
    clock = pygame.time.Clock()
    start = pygame.time.get_ticks()
    while True:
        elapsed = pygame.time.get_ticks() - start
        alpha = min(255, int(255 * (elapsed / duration)))
        if elapsed > duration:
            break
        screen.fill((0, 0, 0))
        text_surface = font.render(text, True, (255, 0, 0))
        text_surface.set_alpha(alpha)
        screen.blit(text_surface, (screen.get_width()//2 - text_surface.get_width()//2, screen.get_height()//2 - text_surface.get_height()//2))
        pygame.display.update()
        clock.tick(60)

def show_credits(screen):
    pygame.mixer.music.load(credits_music_path)
    pygame.mixer.music.play(-1)

    font = pygame.font.SysFont("arial", 32, bold=True)
    small_font = pygame.font.SysFont("arial", 24)

    credit_lines = [
        "Yapımcı: Ömer/Farmer dev",
        "Kodlama: Ömer/Farmer dev",
        "Grafikler: Ömer/Farmerdev",
        "Müzik: İnternetten dızladım",
        "Test Ekibi: Ömer/Farmerdev",
        "Bitrüs: 221291819151445912114114261991120913",
        "Sezon 2 yakında...",
        "",
        "Bitrüs Studios © 2025"
    ]

    scroll_y = screen.get_height()
    clock = pygame.time.Clock()

    while scroll_y > -len(credit_lines)*60:
        screen.fill((0, 0, 0))
        for i, line in enumerate(credit_lines):
            font_used = font if i < len(credit_lines) - 2 else small_font
            rendered = font_used.render(line, True, (255, 255, 255))
            screen.blit(rendered, (screen.get_width() // 2 - rendered.get_width() // 2, scroll_y + i * 60))
        pygame.display.update()
        scroll_y -= 1
        clock.tick(60)

    pygame.mixer.music.fadeout(3000)

def start_end_sezon1(screen, bitrus_img):
    pygame.mixer.init()
    pygame.mixer.music.load(nuke_sound_path)

    background = pygame.image.load(bg_path).convert()
    background = pygame.transform.scale(background, screen.get_size())

    clock = pygame.time.Clock()

    # Bitrüs resmi ölçekle ve konumlandır
    bitrus_scaled = pygame.transform.scale(bitrus_img, (200, 200))
    bitrus_pos = (screen.get_width()//2 - bitrus_scaled.get_width()//2, screen.get_height()//2 - 180)

    # Konuşma kısmı
    for dialog in dialogues:
        for alpha in range(0, 180, 12):
            screen.blit(background, (0, 0))
            screen.blit(bitrus_scaled, bitrus_pos)
            draw_dialog_bar(screen, dialog, alpha)
            pygame.display.update()
            clock.tick(30)
        pygame.time.delay(1800)

    # Patlama müziği başlat
    pygame.mixer.music.play()

    shake_start = pygame.time.get_ticks()
    create_particles((screen.get_width()//2, screen.get_height()//2))

    while pygame.mixer.music.get_busy() or particles:
        now = pygame.time.get_ticks()
        screen.blit(background, (0, 0))

        # Shake ilk 3 saniye devam etsin
        if now - shake_start < 3000:
            offset = screen_shake(12)
        else:
            offset = (0, 0)

        screen.blit(bitrus_scaled, (bitrus_pos[0] + offset[0], bitrus_pos[1] + offset[1]))
        update_particles(screen)

        pygame.display.update()
        clock.tick(60)

    fade_text(screen, "BU BİR SON DEĞİL!", 2000)
    pygame.time.delay(2500)

    show_credits(screen)
