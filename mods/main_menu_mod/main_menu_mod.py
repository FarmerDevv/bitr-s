# -*- coding: utf-8 -*-
"""
Ana Menü Mod - Oyuna ana menü sistemi ekler
Mod Adı: main_menu_mod
Versiyon: 1.1
Açıklama: Splash screen sonrası ana menü, kayıt sistemi ve devam et özelliği ekler
Düzeltme: Devam et seçeneği artık doğru minigame'den başlatıyor
"""

import pygame
import json
import os
import sys

class MainMenuMod:
    def __init__(self):
        self.name = "Ana Menü Mod"
        self.version = "1.1"
        self.description = "Oyuna ana menü sistemi ekler"
        self.enabled = True
        self.save_file = "savegame.json"
        self.game_state = {
            'current_minigame': 0,
            'completed_minigames': [],
            'player_name': 'Oyuncu',
            'total_score': 0
        }
        self.minigame_list = [
            'labyrinth', 'virus_defense', 'new_game', 'code_race', 
            'system_check', 'bitrus_attack', 'jumpscare', 'lab_game',
            'chapter_1', 'end_sezon1', 'notdie', 'new_offer', 
            'cable_game', 'water_system', 'sun_panel'
        ]
        self.menu_active = False
        self.show_menu_after_splash = False
        self.menu_choice = None
        self.force_minigame_index = None
    
    def load_save(self):
        """Kayıt dosyasını yükle"""
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    self.game_state.update(loaded_data)
                print(f"Kayıt dosyası yüklendi! Minigame: {self.game_state.get('current_minigame', 0)}")
                return True
            except Exception as e:
                print(f"Kayıt dosyası yüklenemedi: {e}")
                return False
        return False
    
    def save_game(self):
        """Oyunu kaydet"""
        try:
            with open(self.save_file, 'w', encoding='utf-8') as f:
                json.dump(self.game_state, f, indent=4, ensure_ascii=False)
            print(f"Oyun kaydedildi! Minigame: {self.game_state.get('current_minigame', 0)}")
            return True
        except Exception as e:
            print(f"Oyun kaydedilemedi: {e}")
            return False
    
    def create_new_save(self):
        """Yeni kayıt oluştur"""
        self.game_state = {
            'current_minigame': 0,
            'completed_minigames': [],
            'player_name': 'Oyuncu',
            'total_score': 0,
            'created_date': pygame.time.get_ticks()
        }
        self.save_game()
        print("Yeni kayıt oluşturuldu!")
    
    def show_main_menu(self, screen):
        """Ana menüyü göster"""
        pygame.init()
        WIDTH, HEIGHT = screen.get_size()
        
        # Renkler
        BLACK = (0, 0, 0)
        WHITE = (255, 255, 255)
        GREEN = (0, 255, 0)
        RED = (255, 0, 0)
        BLUE = (100, 200, 255)
        GRAY = (128, 128, 128)
        
        # Fontlar
        title_font = pygame.font.SysFont("Arial", 64, bold=True)
        menu_font = pygame.font.SysFont("Arial", 36, bold=True)
        info_font = pygame.font.SysFont("Arial", 24)
        small_font = pygame.font.SysFont("Arial", 18)
        
        # Arka plan gradient efekti için
        def draw_gradient_bg():
            for y in range(HEIGHT):
                ratio = y / HEIGHT
                r = int(20 + ratio * 30)
                g = int(20 + ratio * 40)
                b = int(50 + ratio * 80)
                pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))
        
        # Menü seçenekleri
        menu_options = [
            {"text": "YENİ OYUN", "action": "new_game"},
            {"text": "DEVAM ET", "action": "continue"},
            {"text": "ÇIKIŞ", "action": "quit"}
        ]
        
        selected_option = 0
        clock = pygame.time.Clock()
        
        # Kayıt dosyası var mı kontrol et
        save_exists = os.path.exists(self.save_file)
        save_data = None
        
        if not save_exists:
            menu_options[1]["text"] = "DEVAM ET (Kayıt Yok)"
            menu_options[1]["disabled"] = True
        else:
            menu_options[1]["disabled"] = False
            # Kayıt dosyasını oku
            try:
                with open(self.save_file, 'r', encoding='utf-8') as f:
                    save_data = json.load(f)
            except:
                save_data = None
        
        # Ana menü döngüsü
        running = True
        while running:
            # Gradient arka plan
            draw_gradient_bg()
            
            # Başlık
            title_text = "FREE BITCOIN BITRÜS"
            title_shadow = title_font.render(title_text, True, (10, 10, 10))
            title = title_font.render(title_text, True, GREEN)
            title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
            screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
            screen.blit(title, title_rect)
            
            # Alt başlık
            subtitle = "ANA MENÜ"
            sub_text = info_font.render(subtitle, True, BLUE)
            sub_rect = sub_text.get_rect(center=(WIDTH // 2, HEIGHT // 4 + 80))
            screen.blit(sub_text, sub_rect)
            
            # Menü seçenekleri
            menu_start_y = HEIGHT // 2
            option_height = 80
            
            for i, option in enumerate(menu_options):
                y_pos = menu_start_y + i * option_height
                
                # Seçili seçenek için arka plan
                if i == selected_option:
                    rect = pygame.Rect(WIDTH // 4, y_pos - 20, WIDTH // 2, 60)
                    pygame.draw.rect(screen, (50, 50, 50), rect)
                    pygame.draw.rect(screen, GREEN, rect, 3)
                    text_color = GREEN
                else:
                    text_color = WHITE
                
                # Devre dışı seçenekler için gri renk
                if option.get("disabled", False):
                    text_color = GRAY
                
                # Menü metni
                text = menu_font.render(option["text"], True, text_color)
                text_rect = text.get_rect(center=(WIDTH // 2, y_pos))
                screen.blit(text, text_rect)
                
                # Seçili seçenek için ok işareti
                if i == selected_option and not option.get("disabled", False):
                    arrow = menu_font.render("→", True, GREEN)
                    screen.blit(arrow, (WIDTH // 4 - 50, y_pos - 15))
            
            # Alt bilgi
            if save_exists and save_data:
                # Kayıt bilgilerini göster
                current_game = save_data.get('current_minigame', 0)
                total_games = len(self.minigame_list)
                progress = f"İlerleme: {current_game}/{total_games}"
                
                progress_text = small_font.render(progress, True, WHITE)
                screen.blit(progress_text, (50, HEIGHT - 120))
                
                score_text = f"Skor: {save_data.get('total_score', 0)}"
                score_surface = small_font.render(score_text, True, WHITE)
                screen.blit(score_surface, (50, HEIGHT - 95))
                
                # Sonraki minigame bilgisi
                if current_game < len(self.minigame_list):
                    next_game_name = self.minigame_list[current_game]
                    next_text = f"Sonraki: {next_game_name}"
                    next_surface = small_font.render(next_text, True, BLUE)
                    screen.blit(next_surface, (50, HEIGHT - 70))
                else:
                    completed_text = "Oyun Tamamlandı!"
                    completed_surface = small_font.render(completed_text, True, GREEN)
                    screen.blit(completed_surface, (50, HEIGHT - 70))
            
            # Kontroller bilgisi
            controls_info = [
                "↑↓ : Menüde Hareket Et",
                "ENTER : Seçimi Onayla",
                "ESC : Çıkış"
            ]
            
            for i, info in enumerate(controls_info):
                info_text = small_font.render(info, True, (200, 200, 200))
                screen.blit(info_text, (WIDTH - 250, HEIGHT - 100 + i * 25))
            
            # Mod bilgisi
            mod_info = small_font.render("Ana Menü Mod v1.1 Aktif", True, (100, 100, 255))
            screen.blit(mod_info, (50, 50))
            
            pygame.display.flip()
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return "quit"
                    
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(menu_options)
                        # Devre dışı seçenekleri atla
                        while menu_options[selected_option].get("disabled", False):
                            selected_option = (selected_option - 1) % len(menu_options)
                    
                    elif event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(menu_options)
                        # Devre dışı seçenekleri atla
                        while menu_options[selected_option].get("disabled", False):
                            selected_option = (selected_option + 1) % len(menu_options)
                    
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                        if not menu_options[selected_option].get("disabled", False):
                            action = menu_options[selected_option]["action"]
                            
                            if action == "new_game":
                                # Yeni oyun başlat
                                self.create_new_save()
                                self.menu_choice = "new_game"
                                self.force_minigame_index = 0
                                return "start_game"
                            
                            elif action == "continue":
                                # Kayıttan devam et
                                if self.load_save():
                                    self.menu_choice = "continue"
                                    # Kayıttan yüklenen minigame index'ini zorla ayarla
                                    self.force_minigame_index = self.game_state.get('current_minigame', 0)
                                    print(f"Devam et: Minigame {self.force_minigame_index} yüklenecek")
                                    return "continue_game"
                                else:
                                    # Kayıt yüklenemezse yeni oyun başlat
                                    self.create_new_save()
                                    self.menu_choice = "new_game"
                                    self.force_minigame_index = 0
                                    return "start_game"
                            
                            elif action == "quit":
                                return "quit"
            
            clock.tick(60)
        
        return "quit"
    
    def get_current_minigame_name(self):
        """Mevcut minigame'in adını döndür"""
        if self.force_minigame_index is not None:
            current = self.force_minigame_index
        else:
            current = self.game_state.get('current_minigame', 0)
            
        if current < len(self.minigame_list):
            return self.minigame_list[current]
        return None
    
    def get_forced_minigame_index(self):
        """Zorlanmış minigame index'ini döndür"""
        return self.force_minigame_index
    
    def advance_to_next_minigame(self):
        """Bir sonraki minigame'e geç"""
        current = self.game_state.get('current_minigame', 0)
        if current < len(self.minigame_list) - 1:
            # Tamamlanan minigame'i listeye ekle
            if current < len(self.minigame_list):
                completed_game = self.minigame_list[current]
                if completed_game not in self.game_state['completed_minigames']:
                    self.game_state['completed_minigames'].append(completed_game)
            
            # Bir sonraki minigame'e geç
            self.game_state['current_minigame'] = current + 1
            self.save_game()
            print(f"Sonraki minigame'e geçildi: {current + 1}")
            return True
        else:
            print("Tüm minigame'ler tamamlandı!")
            return False
    
    def on_game_start(self, game_data):
    # Eğer geçerli kayıt varsa splash sonrası ana menü göstermeyelim
     if os.path.exists(self.save_file):
        try:
            with open(self.save_file, 'r', encoding='utf-8') as f:
                saved = json.load(f)
                self.game_state.update(saved)
                self.force_minigame_index = self.game_state.get('current_minigame', 0)
                self.menu_choice = 'continue'
                self.show_menu_after_splash = True
                print(f"[Devam Et] Kayıttan direkt minigame {self.force_minigame_index} yüklenecek")
        except Exception as e:
            print(f"Kayıt dosyası okunamadı: {e}")
            self.show_menu_after_splash = True
     else:
        self.show_menu_after_splash = True  # Kayıt yoksa menüyü göster
    
     return game_data

    
    def on_screen_update(self, screen, game_data):
        """Her frame'de çalışır"""
        # Splash screen bittikten sonra menüyü göster
        if self.show_menu_after_splash and not self.menu_active:
            self.show_menu_after_splash = False
            self.menu_active = True
            
            # Ana menüyü göster
            result = self.show_main_menu(screen)
            
            if result == "quit":
                pygame.quit()
                sys.exit()
            elif result == "start_game":
                # Yeni oyun başlat
                game_data['menu_choice'] = 'new_game'
                game_data['current_minigame'] = 0
                game_data['force_minigame_index'] = 0
                print("Yeni oyun başlatılıyor")
            elif result == "continue_game":
                # Kayıttan devam et
                game_data['menu_choice'] = 'continue'
                game_data['current_minigame'] = self.game_state.get('current_minigame', 0)
                game_data['force_minigame_index'] = self.force_minigame_index
                game_data['save_data'] = self.game_state
                print(f"Kayıttan devam ediliyor: Minigame {game_data['force_minigame_index']}")
        
        # Eğer zorlanmış minigame index'i varsa, game_data'yı güncelle
        if self.force_minigame_index is not None and 'force_minigame_index' not in game_data:
            game_data['force_minigame_index'] = self.force_minigame_index
            game_data['current_minigame'] = self.force_minigame_index
            print(f"Minigame index zorlandı: {self.force_minigame_index}")
        
        return game_data
    
    def on_minigame_start(self, minigame_name, game_data):
        """Minigame başlarken çalışır"""
        # Eğer menüden geldiyse ve zorlanmış index varsa, doğru minigame'i başlat
        if self.force_minigame_index is not None:
            target_minigame = self.minigame_list[self.force_minigame_index]
            if minigame_name != target_minigame:
                print(f"Minigame değiştiriliyor: {minigame_name} -> {target_minigame}")
                game_data['switch_to_minigame'] = target_minigame
                game_data['target_minigame_index'] = self.force_minigame_index
            
            # Zorlamayı temizle (sadece bir kere uygulamak için)
            self.force_minigame_index = None
        
        return game_data
    
    def on_minigame_end(self, minigame_name, game_data):
        """Minigame bittiğinde çalışır"""
        # Minigame tamamlandığında otomatik kaydet
        if minigame_name in self.minigame_list:
            current_index = self.minigame_list.index(minigame_name)
            if current_index == self.game_state.get('current_minigame', 0):
                self.advance_to_next_minigame()
                print(f"Minigame {minigame_name} tamamlandı ve kaydedildi!")
        
        return game_data
    
    def on_key_press(self, key, game_data):
        """Tuş basıldığında çalışır"""
        # F5 ile hızlı kaydet
        if key == pygame.K_F5:
            # Mevcut durumu kaydet
            if 'current_minigame' in game_data:
                self.game_state['current_minigame'] = game_data['current_minigame']
            self.save_game()
            print("Oyun F5 ile kaydedildi!")
        
        # F9 ile ana menüye dön (acil durum)
        elif key == pygame.K_F9:
            self.menu_active = False
            self.show_menu_after_splash = True
        
        return game_data
    
    def update_game_progress(self, minigame_index, score=0):
        """Oyun ilerlemesini güncelle"""
        self.game_state['current_minigame'] = minigame_index
        self.game_state['total_score'] += score
        self.save_game()

# Mod'u kaydet
mod_instance = MainMenuMod()