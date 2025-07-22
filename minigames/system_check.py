import pygame
import sys
import random
import math

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)
GREEN = (20, 60, 20)
CABLE = (0, 0, 0)

clock = pygame.time.Clock()

class Asset:
    def __init__(self, x, y, kir_image, w=120, h=120):
        self.rect = pygame.Rect(x, y, w, h)
        self.deleted = False
        self.delete_progress = 0.0
        self.particles = []
        self.kir_image = pygame.transform.scale(kir_image, (w, h))

    def draw(self, surface):
        if self.deleted:
            for p in self.particles:
                pygame.draw.circle(surface, WHITE, (int(p[0]), int(p[1])), max(int(p[2]), 0))
        else:
            surface.blit(self.kir_image, self.rect.topleft)
            if self.delete_progress > 0:
                progress_width = int(self.rect.width * (self.delete_progress / 4))
                pygame.draw.rect(surface, YELLOW, (self.rect.x, self.rect.y - 10, progress_width, 5))

    def update(self, dt):
        if self.deleted:
            for p in self.particles:
                p[1] -= p[3] * dt
                p[2] -= 20 * dt
            self.particles = [p for p in self.particles if p[2] > 0]

    def start_delete_particles(self):
        self.particles = []
        for i in range(15):
            angle = (360 / 15) * i
            rad = math.radians(angle)
            x = self.rect.centerx + (math.cos(rad) * 20)
            y = self.rect.centery + (math.sin(rad) * 20)
            radius = 5
            speed = 60 + i * 3
            self.particles.append([x, y, radius, speed])

def draw_circuit_board(surface, width, height):
    surface.fill(GREEN)
    for _ in range(25):
        x1 = random.randint(100, width - 100)
        y1 = random.randint(480, 620)
        x2 = x1 + random.choice([-60, 60])
        y2 = y1 + random.choice([-20, 20])
        pygame.draw.line(surface, CABLE, (x1, y1), (x2, y2), 3)
        if random.random() < 0.3:
            pygame.draw.circle(surface, YELLOW, (x1, y1), 4)

def draw_typing_text(surface, font, text, pos, color, char_index):
    rendered_text = font.render(text[:char_index], True, color)
    surface.blit(rendered_text, pos)

def start_bitrus_cutscene(screen, bitrus_img, kir_img):
    WIDTH, HEIGHT = screen.get_size()
    dialogs = [
        "Vay götü ballı naber, yaptığın şeyler şansın sayesinde kolay geldi heh salak!",
        "Bilgisayarını bırakmıyacağım madem, zenginlik umuduyla keriz gibi virüse tıkladın!",
        "O zaman sana zenginlik verelim hakettin hahaa..."
    ]

    font = pygame.font.SysFont("Arial", 28)
    dialog_index = 0
    char_index = 0
    text_speed = 0.05  # saniye başına harf
    time_since_last_char = 0
    dialog_start_time = pygame.time.get_ticks()
    dialog_advance_delay = 1000  # animasyon bittikten sonra kaç ms sonra sonraki dialoga geçilsin



    running_dialog = True
    dialog_finished = False
    dialog_timer = 0

    while running_dialog:
        dt = clock.tick(60) / 1000
        time_ms = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BLACK)
        screen.blit(bitrus_img, (WIDTH // 2 - bitrus_img.get_width() // 2, 80))

        title_text = font.render("Minigame: system_check", True, WHITE)
        screen.blit(title_text, (WIDTH - title_text.get_width() - 20, 20))

        if dialog_index < len(dialogs):
            current_dialog = dialogs[dialog_index]
            if char_index < len(current_dialog):
                time_since_last_char += dt
                if time_since_last_char >= text_speed:
                    char_index += 1
                    time_since_last_char = 0
            else:
                if not dialog_finished:
                    dialog_finished = True
                    dialog_timer = time_ms
                elif time_ms - dialog_timer > dialog_advance_delay:
                    dialog_index += 1
                    char_index = 0
                    dialog_finished = False

            draw_typing_text(
                screen, font, current_dialog,
                (WIDTH // 2 - font.size(current_dialog)[0] // 2, 350),
                WHITE, char_index
            )
        else:
            running_dialog = False


        pygame.display.flip()

    assets = [
        Asset(300, 520, kir_img),
        Asset(420, 520, kir_img),
        Asset(540, 520, kir_img),
        Asset(660, 520, kir_img),
        Asset(780, 520, kir_img)
    ]

    deleting_asset = None
    running = True
    scroll_x = WIDTH

    while running:
        dt = clock.tick(60) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        draw_circuit_board(screen, WIDTH, HEIGHT)

        screen.blit(bitrus_img, (WIDTH - bitrus_img.get_width() - 30, 30))

        instruction = pygame.font.SysFont("Arial", 24).render(
            "Kirlerin üzerine sol tıkla basılı tutarak eşşek gibi temizle köle!", True, WHITE)
        screen.blit(instruction, (50, 450))

        for asset in assets:
            if not asset.deleted:
                if asset.rect.collidepoint(mouse_pos):
                    if mouse_pressed[0]:
                        if deleting_asset is None:
                            deleting_asset = asset
                            asset.delete_progress = 0
                        if deleting_asset == asset:
                            asset.delete_progress = min(4, asset.delete_progress + dt)
                            if asset.delete_progress >= 4:
                                asset.deleted = True
                                asset.start_delete_particles()
                                deleting_asset = None
                        else:
                            deleting_asset.delete_progress = 0
                            deleting_asset = asset
                            asset.delete_progress = 0
                    else:
                        if deleting_asset == asset:
                            asset.delete_progress = 0
                            deleting_asset = None
                else:
                    if deleting_asset == asset:
                        asset.delete_progress = 0
                        deleting_asset = None

            asset.update(dt)
            asset.draw(screen)

        if all(a.deleted for a in assets):
            running = False

  

        pygame.display.flip()
