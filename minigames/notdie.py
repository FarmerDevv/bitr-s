import pygame
import time

def draw_dialog_box(screen, text, font, y=50):
    width, height = 700, 80
    x = (screen.get_width() - width) // 2
    pygame.draw.rect(screen, (20, 20, 20), (x, y, width, height))
    pygame.draw.rect(screen, (255, 255, 255), (x, y, width, height), 3)
    wrapped_text = font.render(text, True, (255, 255, 255))
    screen.blit(wrapped_text, (x + 20, y + 25))


def start_notdie(screen, bitrus_img, pc_img, wantvirus_img, bomb_img, nuke_img, explosion_sound):
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    screen_rect = screen.get_rect()
    bitrus_pos = [screen_rect.centerx - 100, -200]
    pc_pos = [screen_rect.centerx - 100, screen_rect.bottom - 150]
    wantvirus_pos = [pc_pos[0], pc_pos[1] - 60]
    nuke_pos = [pc_pos[0] + 30, pc_pos[1]]
    bitrus_dead = False
    explosion = False

    bombs = []
    bomb_speed = 5
    rocket_launched = False
    nuke_launched = False

    stage = 0
    timer = time.time()
    running = True

    while running:
        screen.fill((10, 10, 30))
        now = time.time()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return

        if stage == 0 and now - timer > 1:
            if bitrus_pos[1] < 100:
                bitrus_pos[1] += 4
            else:
                timer = now
                stage = 1

        elif stage == 1:
            draw_dialog_box(screen, "Öldüğümü sandın ha...", font)
            if now - timer > 2:
                timer = now
                stage = 2

        elif stage == 2:
            draw_dialog_box(screen, "Senin mükemmel antivirüsün sayesinde... tekrar doğdum!"
            "ve kendimi backupladım", font)
            if now - timer > 3:
                timer = now
                rocket_launched = True
                bombs.append([bitrus_pos[0] + 40, bitrus_pos[1] + 100])
                stage = 3

        elif stage == 3:
            for bomb in bombs:
                bomb[1] += bomb_speed
                if bomb[1] >= wantvirus_pos[1] and not explosion:
                    explosion = True
                    explosion_sound.play()  # 💥 Patlama sesi çalıyor
                    timer = now
                    stage = 4

        elif stage == 4:
            draw_dialog_box(screen, "WantVirus: Kendini feda etti!", font)
            if now - timer > 2:
                nuke_launched = True
                stage = 5
                timer = now

        elif stage == 5:
            nuke_pos[1] -= 10
            if nuke_pos[1] < bitrus_pos[1] + 50:
                bitrus_dead = True
                stage = 6
                timer = now

        elif stage == 6:
            draw_dialog_box(screen, "Bitrüs: Ahah... yedek varyasyonlarım varrr...", font)
            if now - timer > 3:
                running = False

        screen.blit(pc_img, pc_pos)

        if not bitrus_dead:
            screen.blit(bitrus_img, bitrus_pos)

        if stage >= 3:
            screen.blit(wantvirus_img, wantvirus_pos)

        for bomb in bombs:
            if not explosion:
                screen.blit(bomb_img, bomb)

        if explosion:
            boom_text = font.render("BOOOM!", True, (255, 100, 0))
            screen.blit(boom_text, (wantvirus_pos[0] + 20, wantvirus_pos[1]))

        if nuke_launched and not bitrus_dead:
            screen.blit(nuke_img, nuke_pos)

        pygame.display.flip()
        clock.tick(60)
