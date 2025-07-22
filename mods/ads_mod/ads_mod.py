# -*- coding: utf-8 -*-
"""
Ads Mod - Minigame başlamadan önce reklam gösterir
Mod Adı: ads_mod
Versiyon: 1.1
Açıklama: Minigame başlamadan önce mod klasöründeki ads klasöründen rastgele mp4 oynatır.
"""

import os
import random
import pygame
import cv2
import numpy as np
import time

class AdsMod:
    def __init__(self):
        self.name = "Ads Mod"
        self.version = "1.1"
        self.description = "Minigame öncesi rastgele mp4 gösterir."
        self.enabled = True
        self.ads_folder = os.path.join(os.path.dirname(__file__), "ads")
        self.screen = None

    def on_minigame_start(self, minigame_name, game_data):
        """Minigame başlamadan önce çağrılır"""
        self.screen = game_data.get('screen')
        if not self.screen:
            return game_data

        ads_files = []
        try:
            for f in os.listdir(self.ads_folder):
                if f.lower().endswith(".mp4"):
                    ads_files.append(os.path.join(self.ads_folder, f))
        except Exception as e:
            print(f"Ads klasörü okunamadı: {e}")
            return game_data
        
        if not ads_files:
            return game_data  # Reklam yoksa geç

        ad_video = random.choice(ads_files)
        print(f"Reklam oynatılıyor: {ad_video}")
        
        self.show_message("Reklam oynatılıyor...\nPara kazanmamız lazım :)", duration=2)
        self.play_video(ad_video)

        return game_data

    def show_message(self, message, duration=2):
        """Ekrana yazı basar (pygame üzerinden)"""
        screen = self.screen
        if screen is None:
            return

        font = pygame.font.SysFont("arial", 40)
        lines = message.split("\n")
        screen.fill((0, 0, 0))

        for i, line in enumerate(lines):
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + i * 50))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()
        time.sleep(duration)

    def play_video(self, video_path):
        """OpenCV kullanarak mp4 oynatma"""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Video açılamadı: {video_path}")
            return

        clock = pygame.time.Clock()
        screen = self.screen
        width, height = screen.get_size()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (width, height))

            # OpenCV görüntüsünü pygame formatına çevir
            frame = np.rot90(frame)
            frame = pygame.surfarray.make_surface(frame)

            screen.blit(frame, (0, 0))
            pygame.display.flip()
            clock.tick(30)  # 30 FPS oynatma hızı

            # Pygame eventleri işleme (örneğin ESC ile kapatma)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    cap.release()
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        cap.release()
                        return

        cap.release()

# Mod instance olarak kaydet
mod_instance = AdsMod()
