import pygame
import random
import time

# Sabitler
WIDTH, HEIGHT = 1280, 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
BLUE = (80, 180, 255)
YELLOW = (255, 255, 100)
DIRT_COLOR = (139, 69, 19)

pygame.init()
font = pygame.font.SysFont("consolas", 32)
big_font = pygame.font.SysFont("consolas", 64)

pitrus_img = pygame.image.load("assets/pixel_art/pitrüs.png")
pitrus_img = pygame.transform.scale(pitrus_img, (200, 200))

def draw_dialog_box(screen, text, progress=1.0):
    box_width = WIDTH - 40  # Tam yatay, neredeyse tam ekran genişliği
    pygame.draw.rect(screen, BLACK, (20, HEIGHT - 170, box_width, 130))
    pygame.draw.rect(screen, WHITE, (20, HEIGHT - 170, box_width, 130), 3)
    length = int(len(text) * progress)
    rendered = font.render(text[:length], True, WHITE)
    screen.blit(rendered, (40, HEIGHT - 135))  # Soldan biraz daha geniş boşluk

# Animasyon hızını da düşürdüm:
anim_speed = 0.008  # Önceki 0.01 idi, daha yavaş oldu

class Panel:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.dirts = []
        self.generate_dirt()

    def generate_dirt(self):
        for _ in range(20):
            x = random.randint(self.rect.x + 10, self.rect.x + self.rect.width - 30)
            y = random.randint(self.rect.y + 10, self.rect.y + self.rect.height - 30)
            size = random.randint(15, 25)
            self.dirts.append(pygame.Rect(x, y, size, size))

    def draw(self, screen):
        pygame.draw.rect(screen, (30, 30, 30), self.rect, border_radius=15)
        inner = self.rect.inflate(-12, -12)
        pygame.draw.rect(screen, BLUE, inner, border_radius=10)
        for dirt in self.dirts:
            pygame.draw.ellipse(screen, DIRT_COLOR, dirt)

    def clean(self, sponge_rect):
        self.dirts = [d for d in self.dirts if not sponge_rect.colliderect(d)]

    def is_clean(self):
        return len(self.dirts) == 0

def draw_sponge(screen, pos):
    sponge = pygame.Rect(pos[0] - 15, pos[1] - 15, 30, 30)
    pygame.draw.ellipse(screen, YELLOW, sponge)
    return sponge

def start_sun_panel(screen):
    clock = pygame.time.Clock()

    dialog = "Pitrüs: Hey! Güneş panelleri çalışmıyor galiba. Lekelenmiş olabilir. Bir bakabilir misin sen?"
    anim_progress = 0.0
    anim_speed = 0.01  # Daha yavaş animasyon
    show_dialog = True
    dialog_start_time = time.time()

    panels = [
        Panel((80, 180, 220, 120)),
        Panel((320, 180, 220, 120)),
        Panel((560, 180, 220, 120)),
        Panel((800, 180, 220, 120)),
        Panel((1040, 180, 220, 120)),
    ]

    running = True
    game_finished = False

    while running:
        dt = clock.tick(60) / 1000
        screen.fill(GRAY)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        for panel in panels:
            panel.draw(screen)

        if mouse_pressed:
            sponge = draw_sponge(screen, mouse_pos)
            for panel in panels:
                panel.clean(sponge)
        else:
            draw_sponge(screen, mouse_pos)

        if show_dialog:
            screen.blit(pitrus_img, ((WIDTH - 200) // 2, 30))
            anim_progress += anim_speed
            if anim_progress > 1:
                anim_progress = 1
            draw_dialog_box(screen, dialog, anim_progress)
            if time.time() - dialog_start_time > 6:
                show_dialog = False

        if not game_finished and all(panel.is_clean() for panel in panels) and not show_dialog:
            msg = big_font.render("BAŞARILI!", True, (0, 255, 0))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(2000)
            game_finished = True
            running = False

        pygame.display.flip()


