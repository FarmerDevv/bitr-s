import pygame
import time
import math

pygame.init()

WIDTH, HEIGHT = 1280, 720
GRAY = (60, 60, 60)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (220, 20, 60)
YELLOW = (255, 215, 0)
BLUE = (30, 144, 255)
GREEN = (34, 139, 34)

BUTTON_COLORS = [RED, YELLOW, BLUE, GREEN]

font = pygame.font.SysFont("consolas", 32)
big_font = pygame.font.SysFont("consolas", 48)

dialogs = [
    "Hey! Server sıvı soğutma sistemini başlatır mısın?",
    "Sen: Tamamdır."
]

def draw_dialog_box(screen, text, progress=1.0):
    pygame.draw.rect(screen, BLACK, (100, HEIGHT - 160, WIDTH - 200, 120))
    pygame.draw.rect(screen, WHITE, (100, HEIGHT - 160, WIDTH - 200, 120), 3)
    length = int(len(text) * progress)
    rendered = font.render(text[:length], True, WHITE)
    screen.blit(rendered, (120, HEIGHT - 130))

def draw_servers(screen, start_x, start_y, rows, cols, pc_width, pc_height, spacing_x, spacing_y, button_colors):
    pcs = []
    for row in range(rows):
        for col in range(cols):
            x = start_x + col * (pc_width + spacing_x)
            y = start_y + row * (pc_height + spacing_y)
            pc_rect = pygame.Rect(x, y, pc_width, pc_height)
            pygame.draw.rect(screen, BLACK, pc_rect)
            pygame.draw.rect(screen, WHITE, pc_rect, 2)

            btn_radius = 12
            btn_x = x + pc_width // 2
            btn_y = y + 10
            color = button_colors[row % len(button_colors)]
            pygame.draw.circle(screen, color, (btn_x, btn_y), btn_radius)

            pcs.append({"rect": pc_rect, "button_pos": (btn_x, btn_y), "button_color": color})
    return pcs

def draw_transparent_pipes(screen, start_x, start_y, rows, cols, pc_width, pc_height, spacing_x, spacing_y):
    pipe_color = (0, 128, 255, 120)  # %50 saydam mavi
    pipe_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for row in range(rows):
        y = start_y + row * (pc_height + spacing_y) + pc_height // 2
        for col in range(cols - 1):
            x1 = start_x + col * (pc_width + spacing_x) + pc_width
            pygame.draw.rect(pipe_surface, pipe_color, (x1, y - 10, spacing_x, 20))

    for col in range(cols):
        x = start_x + col * (pc_width + spacing_x) + pc_width // 2
        for row in range(rows - 1):
            y1 = start_y + row * (pc_height + spacing_y) + pc_height
            y2 = y1 + spacing_y
            pygame.draw.rect(pipe_surface, pipe_color, (x - 10, y1, 20, spacing_y))

    screen.blit(pipe_surface, (0, 0))

def draw_water_droplets(screen, droplets):
    for droplet in droplets:
        pygame.draw.circle(screen, (30, 144, 255), (int(droplet["x"]), int(droplet["y"])), 10)

def start_water_system(screen):
    clock = pygame.time.Clock()

    dialog_index = 0
    dialog_start_time = time.time()
    dialog_duration = 4
    anim_progress = 0.0
    anim_speed = 0.03
    in_dialog = True

    start_x = 300
    start_y = 100
    rows = 4
    cols = 5
    pc_width = 80
    pc_height = 100
    spacing_x = 40
    spacing_y = 40

    BUTTON_COLORS = [RED, YELLOW, BLUE, GREEN]

    water_path = []
    for row in range(rows):
        y = start_y + row * (pc_height + spacing_y) + pc_height // 2
        for col in range(cols):
            x = start_x + col * (pc_width + spacing_x) + pc_width // 2
            water_path.append({"x": x, "y": y})
        if row < rows - 1:
            x = start_x + (cols - 1) * (pc_width + spacing_x) + pc_width // 2
            y2 = start_y + (row + 1) * (pc_height + spacing_y) + pc_height // 2
            water_path.append({"x": x, "y": y2})

    red_button_base_rect = pygame.Rect(100, HEIGHT // 2 - 50, 80, 100)
    red_button_rect = red_button_base_rect.copy()
    red_button_pressed_time = None
    water_flowing = False
    droplets = []
    droplet_index = 0
    droplet_timer = 0
    water_speed = 180
    finish_time = None
    button_activated = False

    while True:
        dt = clock.tick(60) / 1000
        screen.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if not in_dialog and not button_activated:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1 and red_button_rect.collidepoint(event.pos):
                        red_button_pressed_time = time.time()
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        red_button_pressed_time = None

        if in_dialog:
            anim_progress += anim_speed
            if anim_progress > 1:
                anim_progress = 1

            screen.blit(pitrus_img, ((WIDTH - 200) // 2, 50))
            draw_dialog_box(screen, dialogs[dialog_index], anim_progress)

            if time.time() - dialog_start_time > dialog_duration:
                dialog_index += 1
                dialog_start_time = time.time()
                anim_progress = 0
                if dialog_index >= len(dialogs):
                    in_dialog = False
        else:
            draw_servers(screen, start_x, start_y, rows, cols, pc_width, pc_height, spacing_x, spacing_y, BUTTON_COLORS)
            draw_transparent_pipes(screen, start_x, start_y, rows, cols, pc_width, pc_height, spacing_x, spacing_y)

            # Buton büyütme ve rengi ayarlama
            if button_activated:
                # Yeşil ve biraz büyük
                red_button_rect.width = int(red_button_base_rect.width * 1.3)
                red_button_rect.height = int(red_button_base_rect.height * 1.3)
                red_button_rect.center = red_button_base_rect.center
                pygame.draw.rect(screen, GREEN, red_button_rect)
            else:
                red_button_rect = red_button_base_rect.copy()
                pygame.draw.rect(screen, RED, red_button_rect)

            btn_text = font.render("Başlat", True, WHITE)
            screen.blit(btn_text, (red_button_rect.centerx - btn_text.get_width() // 2, red_button_rect.centery - btn_text.get_height() // 2))

            if red_button_pressed_time and not button_activated:
                held_time = time.time() - red_button_pressed_time
                bar_width = 60
                bar_height = 10
                bar_x = red_button_rect.centerx - bar_width // 2
                bar_y = red_button_rect.bottom + 10
                progress = min(held_time / 5, 1)
                pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
                pygame.draw.rect(screen, BLUE, (bar_x + 2, bar_y + 2, int((bar_width - 4) * progress), bar_height - 4))

                if held_time >= 5:
                    water_flowing = True
                    button_activated = True
                    red_button_pressed_time = None
                    droplets = []
                    droplet_index = 0
                    droplet_timer = 0

            # Su akışı
            if water_flowing:
                droplet_timer += dt
                if droplet_timer > 0.3:
                    droplet_timer = 0
                    if droplet_index < len(water_path):
                        droplets.append({"x": water_path[droplet_index]["x"], "y": water_path[droplet_index]["y"], "path_index": droplet_index, "progress": 0.0})
                        droplet_index += 1

                for droplet in droplets[:]:
                    idx = droplet["path_index"]
                    if idx >= len(water_path) - 1:
                        droplets.remove(droplet)
                        continue

                    start_pos = water_path[idx]
                    end_pos = water_path[idx + 1]

                    droplet["progress"] += water_speed * dt / max(1, math.dist((start_pos["x"], start_pos["y"]), (end_pos["x"], end_pos["y"])))
                    if droplet["progress"] >= 1:
                        droplet["path_index"] += 1
                        droplet["progress"] = 0
                    else:
                        new_x = start_pos["x"] + (end_pos["x"] - start_pos["x"]) * droplet["progress"]
                        new_y = start_pos["y"] + (end_pos["y"] - start_pos["y"]) * droplet["progress"]
                        droplet["x"] = new_x
                        droplet["y"] = new_y

                draw_water_droplets(screen, droplets)

                if droplet_index >= len(water_path) and len(droplets) == 0 and finish_time is None:
                    finish_time = time.time()

            if finish_time is not None and time.time() - finish_time > 3:
                
                return

        pygame.display.update()


# Pitrüs resmi
pitrus_img = pygame.image.load("assets/pixel_art/pitrüs.png")
pitrus_img = pygame.transform.scale(pitrus_img, (200, 200))

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Server Sıvı Soğutma Sistemi")
    start_water_system(screen)
