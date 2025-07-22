import pygame
import sys
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
import ctypes

def set_system_volume_max():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = ctypes.cast(interface, ctypes.POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(1.0, None)  # Maksimum ses (100%)

def draw_dialog_box(screen, text, font, box_rect):
    dialog_surf = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
    dialog_surf.fill((30, 30, 30, 220))  # Koyu gri yarı saydam

    pygame.draw.rect(dialog_surf, (255, 255, 255), dialog_surf.get_rect(), 3, border_radius=10)

    wrapped_text = []
    words = text.split(' ')
    line = ''
    for word in words:
        test_line = line + word + ' '
        if font.size(test_line)[0] < box_rect.width - 40:
            line = test_line
        else:
            wrapped_text.append(line)
            line = word + ' '
    wrapped_text.append(line)

    y_offset = 20
    for line in wrapped_text:
        rendered = font.render(line.strip(), True, (255, 255, 255))
        dialog_surf.blit(rendered, ((box_rect.width - rendered.get_width()) // 2, y_offset))
        y_offset += rendered.get_height() + 5

    screen.blit(dialog_surf, (box_rect.x, box_rect.y))


def start_bitrus_jumpscare(screen, bitrus_img, human_img, human_sound):
    pygame.font.init()
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 28)
    big_font = pygame.font.SysFont("Arial", 48)

    bg = pygame.image.load("assets/pixel_art/xp_background.jpg")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

    bitrus_img = pygame.transform.scale(bitrus_img, (200, 200))
    human_img = pygame.transform.scale(human_img, (WIDTH, HEIGHT))

    dialogs = [
        "Ahhh tamam sonunda sen kazandın!",
        "İşte mutlu musun?",
        "Tamam çekip gidiyorum bilgisayarınla, sana iyi eğlenceler..."
    ]

    dialog_index = 0
    dialog_start_time = pygame.time.get_ticks()
    dialog_delay = 3500

    jump_scare_triggered = False
    scare_start_time = 0
    scare_duration = 3000  # jump scare 3 saniye gösterilsin

    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(bg, (0, 0))

        if not jump_scare_triggered:
            screen.blit(bitrus_img, (WIDTH // 2 - bitrus_img.get_width() // 2, HEIGHT // 4))

            box_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 50, WIDTH // 2, 120)
            draw_dialog_box(screen, dialogs[dialog_index], font, box_rect)

            now = pygame.time.get_ticks()
            if now - dialog_start_time > dialog_delay:
                dialog_index += 1
                dialog_start_time = now

                if dialog_index >= len(dialogs):
                    jump_scare_triggered = True
                    scare_start_time = pygame.time.get_ticks()
                    set_system_volume_max()  # Sistem sesini maksimum yap
                    human_sound.set_volume(1.0)
                    human_sound.play()

        else:
            screen.blit(human_img, (0, 0))
            scare_text = big_font.render("Gittiğimi mi sandın salak!", True, (255, 0, 0))
            screen.blit(scare_text, (WIDTH // 2 - scare_text.get_width() // 2, HEIGHT - 150))

            now = pygame.time.get_ticks()
            # Jump scare süresi dolduysa fonksiyondan çık
            if now - scare_start_time > scare_duration:
                return  # Fonksiyondan çık ve ana programa dön

        pygame.display.flip()
