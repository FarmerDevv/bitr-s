import pygame
import sys
import os
import importlib.util
import json
from typing import Dict, List, Any, Optional
from minigames.labyrinth_game import start_labyrinth_game
from minigames.virus_defense import start_virus_defense
from minigames.new_game import start_new_game
from minigames.code_race import start_code_race
from minigames.system_check import start_bitrus_cutscene
from minigames.bitatc import start_bitrus_attack
from minigames.jump import start_bitrus_jumpscare
from minigames.lab_game import start_lab_game
from minigames.chap_1 import start_chap_1
from minigames.nuke import start_end_sezon1
from minigames.notdie import start_notdie
import random
pygame.init()
class ModManager:
    def __init__(self):
        self.mods_dir = "mods"
        self.loaded_mods = {}
        self.active_mods = []
        self.mod_hooks = {
            'on_game_start': [],
            'on_game_end': [],
            'on_dialog_show': [],
            'on_icon_click': [],
            'on_key_press': [],
            'on_screen_update': [],
            'on_minigame_start': [],
            'on_minigame_end': []
        }
        # Yeni özellikler
        self.mod_imports = {}  # Mod'ların import ettiği minigame'ler
        self.mod_key_bindings = {}  # Mod'ların key binding'leri
        self.mod_functions = {}  # Mod'ların çağırılabilir fonksiyonları
        
        self.create_mods_directory()
        self.load_all_mods()
    
    def create_mods_directory(self):
        """Mods klasörü yoksa oluşturur ve örnek mod klasörü ekler"""
        if not os.path.exists(self.mods_dir):
            os.makedirs(self.mods_dir)
            print(f"{self.mods_dir} klasörü oluşturuldu!")
            
            # Örnek mod klasörü oluştur
            example_mod_dir = os.path.join(self.mods_dir, "example_mod")
            os.makedirs(example_mod_dir, exist_ok=True)
            
            # Örnek mod dosyası oluştur
            example_mod = '''# -*- coding: utf-8 -*-
"""
Örnek Mod - Bu mod oyuna örnek özellikler ekler
Mod Adı: example_mod
Versiyon: 1.0
Açıklama: Bu bir örnek moddur, nasıl mod yapılacağını gösterir
"""

import pygame

class ExampleMod:
    def __init__(self):
        self.name = "Örnek Mod"
        self.version = "1.0"
        self.description = "Bu bir örnek moddur"
        self.enabled = True
    
    def on_game_start(self, game_data):
        """Oyun başladığında çalışır"""
        print(f"{self.name} yüklendi!")
        return game_data
    
    def on_key_press(self, key, game_data):
        """Tuş basıldığında çalışır"""
        if key == pygame.K_h:
            print("Merhaba! Örnek mod aktif!")
        return game_data
    
    def on_screen_update(self, screen, game_data):
        """Her frame'de çalışır"""
        # Sol üst köşeye mod bilgisi yaz
        font = pygame.font.SysFont("Arial", 16)
        text = font.render(f"{self.name} Aktif", True, (255, 255, 0))
        screen.blit(text, (10, HEIGHT - 30))
        return game_data
    
    def on_dialog_show(self, dialog_text, game_data):
        """Diyalog gösterilirken çalışır"""
        # Diyalogu değiştir
        if "Bitrüs" in dialog_text:
            dialog_text += " [MOD: Örnek mod aktif!]"
        return dialog_text, game_data

# Mod'u kaydet
mod_instance = ExampleMod()
'''
            
            with open(os.path.join(example_mod_dir, "example_mod.py"), "w", encoding="utf-8") as f:
                f.write(example_mod)
                
            # Manifest dosyası oluştur
            manifest = {
                "name": "Örnek Mod",
                "version": "1.0",
                "description": "Bu bir örnek moddur, nasıl mod yapılacağını gösterir",
                "author": "Farmer_Dev",
                "main_file": "example_mod.py",
                "enabled": True,
                "dependencies": [],
                "min_game_version": "1.0"
            }
            
            with open(os.path.join(example_mod_dir, "manifest.json"), "w", encoding="utf-8") as f:
                json.dump(manifest, f, indent=4, ensure_ascii=False)
    def load_mod(self, mod_folder: str, manifest: dict):
        """Belirli bir modu yükler"""
        mod_path = os.path.join(self.mods_dir, mod_folder)
        main_file = manifest.get("main_file", f"{mod_folder}.py")
        mod_file_path = os.path.join(mod_path, main_file)
        
        if not os.path.exists(mod_file_path):
            print(f"Mod dosyası bulunamadı: {mod_file_path}")
            return False
            
        try:
            spec = importlib.util.spec_from_file_location(mod_folder, mod_file_path)
            module = importlib.util.module_from_spec(spec)
            
            original_path = sys.path.copy()
            sys.path.insert(0, mod_path)
            
            spec.loader.exec_module(module)
            sys.path = original_path
            
            if hasattr(module, 'mod_instance'):
                mod_instance = module.mod_instance
                
                if hasattr(mod_instance, '__dict__'):
                    mod_instance.manifest = manifest
                    mod_instance.mod_folder = mod_folder
                    mod_instance.mod_path = mod_path
                
                self.loaded_mods[mod_folder] = mod_instance
                self.active_mods.append(mod_folder)
                
                # Hook'ları kaydet - TÜM HOOK'LAR
                for hook_name in self.mod_hooks.keys():
                    if hasattr(mod_instance, hook_name):
                        self.mod_hooks[hook_name].append(getattr(mod_instance, hook_name))
                
                # Import'ları tara
                self.scan_mod_imports(mod_instance, mod_folder, module)
                self.scan_mod_key_bindings(mod_instance, mod_folder)
                self.scan_mod_functions(mod_instance, mod_folder)
                
                print(f"Mod yüklendi: {manifest.get('name', mod_folder)} v{manifest.get('version', '1.0')}")
                return True
            else:
                print(f"Mod'da mod_instance bulunamadı: {mod_folder}")
                return False
                
        except Exception as e:
            print(f"Mod yüklenemedi {mod_folder}: {e}")
            return False
    
    def scan_mod_imports(self, mod_instance, mod_folder, module):
        """Mod'un import ettiği minigame'leri tarar"""
        if hasattr(mod_instance, 'minigame_imports'):
            imports = mod_instance.minigame_imports
            if isinstance(imports, dict):
                self.mod_imports[mod_folder] = imports
                print(f"Mod {mod_folder} minigame import'ları yüklendi: {list(imports.keys())}")
        
        for attr_name in dir(module):
            if attr_name.startswith('start_') and callable(getattr(module, attr_name)):
                if mod_folder not in self.mod_imports:
                    self.mod_imports[mod_folder] = {}
                self.mod_imports[mod_folder][attr_name] = getattr(module, attr_name)
    
    def scan_mod_key_bindings(self, mod_instance, mod_folder):
        """Mod'un key binding'lerini tarar"""
        if hasattr(mod_instance, 'key_bindings'):
            bindings = mod_instance.key_bindings
            if isinstance(bindings, dict):
                self.mod_key_bindings[mod_folder] = bindings
                print(f"Mod {mod_folder} key binding'leri yüklendi: {list(bindings.keys())}")
    
    def scan_mod_functions(self, mod_instance, mod_folder):
        """Mod'un özel fonksiyonlarını tarar"""
        if hasattr(mod_instance, 'custom_functions'):
            functions = mod_instance.custom_functions
            if isinstance(functions, dict):
                self.mod_functions[mod_folder] = functions
                print(f"Mod {mod_folder} özel fonksiyonları yüklendi: {list(functions.keys())}")
    
    def handle_key_press(self, key, game_data):
        """Mod'ların key press event'larını işler - DÜZELTILMIŞ"""
        # Standart hook'ları çağır - DOĞRU PARAMETRELER
        self.call_hook('on_key_press', key, game_data)
        
        # Mod key binding'lerini kontrol et
        for mod_folder, bindings in self.mod_key_bindings.items():
            if mod_folder in self.active_mods:
                for key_code, action in bindings.items():
                    if key == key_code:
                        try:
                            if callable(action):
                                action(game_data)
                            elif isinstance(action, str) and mod_folder in self.mod_functions:
                                if action in self.mod_functions[mod_folder]:
                                    self.mod_functions[mod_folder][action](game_data)
                        except Exception as e:
                            print(f"Mod key binding hatası {mod_folder}: {e}")
    
    def handle_mouse_click(self, pos, button, game_data):
        """Mouse click'leri işler"""
        self.call_hook('on_mouse_click', pos, button, game_data)
    
    def update_mods(self, game_data):
        """Her frame modları günceller"""
        self.call_hook('on_update', game_data)
    
    def call_hook(self, hook_name: str, *args, **kwargs):
        """Mod hook'larını çağırır - DÜZELTILMIŞ"""
        results = []
        for hook_func in self.mod_hooks.get(hook_name, []):
            try:
                result = hook_func(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"Mod hook hatası {hook_name}: {e}")
        return results
    
    def get_mod_minigames(self):
        """Aktif modların minigame'lerini döndürür"""
        minigames = {}
        for mod_folder, imports in self.mod_imports.items():
            if mod_folder in self.active_mods:
                minigames.update(imports)
        return minigames
    
    def call_mod_minigame(self, minigame_name, *args, **kwargs):
        """Mod minigame'ini çağırır"""
        for mod_folder, imports in self.mod_imports.items():
            if mod_folder in self.active_mods and minigame_name in imports:
                try:
                    return imports[minigame_name](*args, **kwargs)
                except Exception as e:
                    print(f"Mod minigame hatası {minigame_name}: {e}")
                    return None
        print(f"Mod minigame bulunamadı: {minigame_name}")
        return None
    def load_all_mods(self):
        """Tüm modları yükler"""
        if not os.path.exists(self.mods_dir):
            return
            
        for mod_folder in os.listdir(self.mods_dir):
            mod_path = os.path.join(self.mods_dir, mod_folder)
            
            # Klasör mü kontrol et
            if os.path.isdir(mod_path):
                manifest_path = os.path.join(mod_path, "manifest.json")
                
                # Manifest dosyası var mı kontrol et
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as f:
                            manifest = json.load(f)
                        
                        # Mod etkin mi kontrol et
                        if manifest.get("enabled", False):
                            self.load_mod(mod_folder, manifest)
                            
                    except Exception as e:
                        print(f"Manifest dosyası okunamadı {mod_folder}: {e}")
    
    def load_mod(self, mod_folder: str, manifest: dict):
        """Belirli bir modu yükler"""
        mod_path = os.path.join(self.mods_dir, mod_folder)
        main_file = manifest.get("main_file", f"{mod_folder}.py")
        mod_file_path = os.path.join(mod_path, main_file)
        
        if not os.path.exists(mod_file_path):
            print(f"Mod dosyası bulunamadı: {mod_file_path}")
            return False
            
        try:
            spec = importlib.util.spec_from_file_location(mod_folder, mod_file_path)
            module = importlib.util.module_from_spec(spec)
            
            # Mod klasörünü Python path'ine ekle
            original_path = sys.path.copy()
            sys.path.insert(0, mod_path)
            
            spec.loader.exec_module(module)
            
            # Path'i eski haline getir
            sys.path = original_path
            
            # mod_instance değişkenini ara
            if hasattr(module, 'mod_instance'):
                mod_instance = module.mod_instance
                
                # Manifest bilgilerini mod instance'a ekle
                if hasattr(mod_instance, '__dict__'):
                    mod_instance.manifest = manifest
                    mod_instance.mod_folder = mod_folder
                    mod_instance.mod_path = mod_path
                
                self.loaded_mods[mod_folder] = mod_instance
                self.active_mods.append(mod_folder)
                
                # Hook'ları kaydet
                for hook_name in self.mod_hooks.keys():
                    if hasattr(mod_instance, hook_name):
                        self.mod_hooks[hook_name].append(getattr(mod_instance, hook_name))
                
                print(f"Mod yüklendi: {manifest.get('name', mod_folder)} v{manifest.get('version', '1.0')}")
                return True
            else:
                print(f"Mod'da mod_instance bulunamadı: {mod_folder}")
                return False
                
        except Exception as e:
            print(f"Mod yüklenemedi {mod_folder}: {e}")
            return False
    
    def call_hook(self, hook_name: str, *args, **kwargs):
        """Mod hook'larını çağırır"""
        results = []
        for hook_func in self.mod_hooks.get(hook_name, []):
            try:
                result = hook_func(*args, **kwargs)
                results.append(result)
            except Exception as e:
                print(f"Mod hook hatası {hook_name}: {e}")
        return results
    
    def get_active_mods_info(self) -> List[str]:
        """Aktif modların bilgilerini döndürür"""
        info_list = []
        for mod_folder in self.active_mods:
            mod = self.loaded_mods.get(mod_folder)
            if mod and hasattr(mod, 'manifest'):
                manifest = mod.manifest
                name = manifest.get('name', mod_folder)
                version = manifest.get('version', '1.0')
                description = manifest.get('description', 'Açıklama yok')
                author = manifest.get('author', 'Bilinmiyor')
                info_list.append(f"{name} v{version} by {author} - {description}")
            elif mod:
                name = getattr(mod, 'name', mod_folder)
                version = getattr(mod, 'version', '1.0')
                description = getattr(mod, 'description', 'Açıklama yok')
                info_list.append(f"{name} v{version} - {description}")
        return info_list
    
    def reload_mod(self, mod_folder: str) -> bool:
        """Belirli bir modu yeniden yükler"""
        if mod_folder in self.loaded_mods:
            # Eski mod'u temizle
            old_mod = self.loaded_mods[mod_folder]
            for hook_name in self.mod_hooks.keys():
                if hasattr(old_mod, hook_name):
                    hook_func = getattr(old_mod, hook_name)
                    if hook_func in self.mod_hooks[hook_name]:
                        self.mod_hooks[hook_name].remove(hook_func)
            
            del self.loaded_mods[mod_folder]
            if mod_folder in self.active_mods:
                self.active_mods.remove(mod_folder)
        
        # Yeni mod'u yükle
        mod_path = os.path.join(self.mods_dir, mod_folder)
        manifest_path = os.path.join(mod_path, "manifest.json")
        
        if os.path.exists(manifest_path):
            try:
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                
                if manifest.get("enabled", False):
                    return self.load_mod(mod_folder, manifest)
            except Exception as e:
                print(f"Mod yeniden yüklenemedi {mod_folder}: {e}")
        
        return False

# Global mod manager
mod_manager = ModManager()


pygame.display.set_caption("free bitcoin")
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont("Arial", 28)

ASSETS_DIR = "assets/pixel_art"
BACKGROUND_PATH = os.path.join(ASSETS_DIR, "xp_background.jpg")
BITCOIN_ICON_PATH = os.path.join(ASSETS_DIR, "bitcoin_icon.png")
GALLERY_ICON_PATH = os.path.join(ASSETS_DIR, "gallery_icon.png")
ABOUT_ICON_PATH = os.path.join(ASSETS_DIR, "about_icon.png")
VIRUS_IMAGE_PATH = os.path.join(ASSETS_DIR, "bitrüs.png")
WANTVIRUS_IMAGE_PATH = os.path.join(ASSETS_DIR, "wantvirus.png")
pc_img = pygame.image.load(os.path.join(ASSETS_DIR, "pc.png"))
bitrus_img = pygame.image.load(os.path.join(ASSETS_DIR, "bitrüs.png"))
kir_img = pygame.image.load(os.path.join(ASSETS_DIR, "kir.png"))
human_img = pygame.image.load(os.path.join(ASSETS_DIR, "human.jpg"))
rocket_img = pygame.image.load(os.path.join(ASSETS_DIR, "rocket.png"))
nuke_img = pygame.image.load(os.path.join(ASSETS_DIR, "nuke.png"))
wantvirus_img = pygame.image.load("assets\pixel_art\wantvirus.png")
human_sound = pygame.mixer.Sound("assets/music/human.mp3")
explosion_sound = pygame.mixer.Sound("assets/music/nuke.mp3")
def reload_mods():
    """Modları yeniden yükler"""
    global mod_manager
    mod_manager = ModManager()

def show_mod_menu(screen):
    """Mod menüsünü gösterir"""
    screen.fill(BLACK)
    WIDTH, HEIGHT = screen.get_size()
    
    title_font = pygame.font.SysFont("Arial", 48)
    info_font = pygame.font.SysFont("Arial", 24)
    small_font = pygame.font.SysFont("Arial", 18)
    button_font = pygame.font.SysFont("Arial", 20)
    
    # Başlık
    title = title_font.render("MODLAR", True, GREEN)
    title_rect = title.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title, title_rect)
    
    # Tüm modları al (aktif ve inaktif)
    all_mods = []
    if os.path.exists(mod_manager.mods_dir):
        for mod_folder in os.listdir(mod_manager.mods_dir):
            mod_path = os.path.join(mod_manager.mods_dir, mod_folder)
            if os.path.isdir(mod_path):
                manifest_path = os.path.join(mod_path, "manifest.json")
                if os.path.exists(manifest_path):
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as f:
                            manifest = json.load(f)
                        all_mods.append((mod_folder, manifest))
                    except Exception as e:
                        print(f"Manifest okunamadı {mod_folder}: {e}")
    
    if not all_mods:
        no_mods = info_font.render("Hiç mod yok", True, WHITE)
        screen.blit(no_mods, (WIDTH // 6, HEIGHT // 3))
        
        # Mod nasıl yüklenir bilgisi
        help_lines = [
            "Mod yüklemek için:",
            "1. 'mods' klasöründe yeni bir klasör oluşturun",
            "2. Klasör içine mod dosyanızı ve manifest.json ekleyin",
            "3. manifest.json'da enabled: true yapın",
            "4. Oyunu yeniden başlatın"
        ]
        
        for i, line in enumerate(help_lines):
            text = small_font.render(line, True, (150, 150, 150))
            screen.blit(text, (WIDTH // 6, HEIGHT // 3 + 100 + i * 25))
            
    else:
        y_offset = HEIGHT // 5
        button_rects = []
        
        for i, (mod_folder, manifest) in enumerate(all_mods):
            y_pos = y_offset + i * 60
            
            # Mod bilgisi
            name = manifest.get('name', mod_folder)
            version = manifest.get('version', '1.0')
            description = manifest.get('description', 'Açıklama yok')
            author = manifest.get('author', 'Bilinmiyor')
            enabled = manifest.get('enabled', False)
            
            # Mod durumu rengi
            status_color = GREEN if enabled else (150, 150, 150)
            status_text = "AKTİF" if enabled else "KAPALI"
            
            # Mod bilgisi metni
            mod_info = f"• {name} v{version} by {author}"
            text = info_font.render(mod_info, True, status_color)
            screen.blit(text, (WIDTH // 8, y_pos))
            
            # Açıklama
            desc_text = small_font.render(description, True, (200, 200, 200))
            screen.blit(desc_text, (WIDTH // 8, y_pos + 25))
            
            # Durum etiketi
            status_label = small_font.render(f"Durum: {status_text}", True, status_color)
            screen.blit(status_label, (WIDTH // 8, y_pos + 45))
            
            # Aç/Kapat butonu
            button_width = 120
            button_height = 35
            button_x = WIDTH - WIDTH // 4
            button_y = y_pos + 10
            
            # Buton rengi
            button_color = (0, 150, 0) if not enabled else (150, 0, 0)
            button_text_color = WHITE
            button_text = "AKTİF YAP" if not enabled else "KAPAT"
            
            # Buton çiz
            button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
            pygame.draw.rect(screen, button_color, button_rect)
            pygame.draw.rect(screen, WHITE, button_rect, 2)
            
            # Buton metni
            btn_text = button_font.render(button_text, True, button_text_color)
            text_rect = btn_text.get_rect(center=button_rect.center)
            screen.blit(btn_text, text_rect)
            
            # Buton bilgisini sakla (click kontrolü için)
            button_rects.append((button_rect, mod_folder, manifest))
        
        # Toplam mod sayısı
        total_text = small_font.render(f"Toplam mod sayısı: {len(all_mods)}", True, GREEN)
        screen.blit(total_text, (WIDTH // 8, y_offset + len(all_mods) * 60 + 20))
    
    # Talimatlar
    instruction = info_font.render("ESC tuşu ile çık", True, GREEN)
    screen.blit(instruction, (WIDTH // 8, HEIGHT - 100))
    
    instruction2 = small_font.render("R tuşu ile modları yeniden yükle", True, (150, 150, 150))
    screen.blit(instruction2, (WIDTH // 8, HEIGHT - 70))
    
    instruction3 = small_font.render("Butonlara tıklayarak modları açıp kapatın", True, (150, 150, 150))
    screen.blit(instruction3, (WIDTH // 8, HEIGHT - 40))
    
    pygame.display.flip()
    
    # Event loop
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
                elif event.key == pygame.K_r:
                    # Modları yeniden yükle
                    screen.fill(BLACK)
                    loading_text = info_font.render("Modlar yeniden yükleniyor...", True, WHITE)
                    screen.blit(loading_text, (WIDTH // 2 - 150, HEIGHT // 2))
                    pygame.display.flip()
                    
                    reload_mods()
                    pygame.time.wait(1000)
                    return show_mod_menu(screen)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol tık
                    pos = event.pos
                    # Buton tıklamaları kontrol et
                    if 'button_rects' in locals():
                        for button_rect, mod_folder, manifest in button_rects:
                            if button_rect.collidepoint(pos):
                                # Mod durumunu değiştir
                                manifest['enabled'] = not manifest.get('enabled', False)
                                
                                # Manifest dosyasını güncelle
                                manifest_path = os.path.join(mod_manager.mods_dir, mod_folder, "manifest.json")
                                try:
                                    with open(manifest_path, "w", encoding="utf-8") as f:
                                        json.dump(manifest, f, indent=4, ensure_ascii=False)
                                    
                                    # Başarı mesajı göster
                                    screen.fill(BLACK)
                                    status = "aktif edildi" if manifest['enabled'] else "kapatıldı"
                                    success_text = info_font.render(f"Mod {status}! Değişiklikler için R tuşuna basın.", True, GREEN)
                                    screen.blit(success_text, (WIDTH // 2 - 300, HEIGHT // 2))
                                    pygame.display.flip()
                                    pygame.time.wait(1500)
                                    
                                    # Menüyü yeniden göster
                                    return show_mod_menu(screen)
                                    
                                except Exception as e:
                                    # Hata mesajı göster
                                    screen.fill(BLACK)
                                    error_text = info_font.render(f"Hata: Mod durumu değiştirilemedi!", True, (255, 0, 0))
                                    screen.blit(error_text, (WIDTH // 2 - 200, HEIGHT // 2))
                                    pygame.display.flip()
                                    pygame.time.wait(1500)
                                    return show_mod_menu(screen)
    
    return True

def start_gallery_app(screen):
    screen.fill(BLACK)
    WIDTH, HEIGHT = screen.get_size()

    gallery_images = []
    for i in range(1, 4):
        path = os.path.join(ASSETS_DIR, f"gallery{i}.jpg")
        try:
            img = pygame.image.load(path)
            img = pygame.transform.scale(img, (200, 200))
            gallery_images.append(img)
        except Exception as e:
            print(f"Galeri resmi yüklenemedi: {path}, hata: {e}")

    gap = 50
    total_width = len(gallery_images) * 200 + (len(gallery_images) - 1) * gap
    start_x = (WIDTH - total_width) // 2
    y = HEIGHT // 3

    for i, img in enumerate(gallery_images):
        x = start_x + i * (200 + gap)
        screen.blit(img, (x, y))

    pygame.display.flip()
    pygame.time.wait(5000)

def start_about_app(screen):
    screen.fill(BLACK)
    WIDTH, HEIGHT = screen.get_size()
    FONT_TITLE = pygame.font.SysFont("Arial", 48)
    FONT_TEXT = pygame.font.SysFont("Arial", 28)

    title = FONT_TITLE.render("Hakkında", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 5))
    screen.blit(title, title_rect)

    about_lines = [
        "Bu uygulama Farmer_Dev tarafından yapıldı.",
        "Python Pygame teknolojisi kullanıldı.",
        "Tüm grafikler ve tasarımlar Farmer_Dev'e aittir.",
        "İyi oyunlar oynadıkça eğlenin!",
        "kelekler :(",
        "",
        "Gelişmiş Mod Desteği Eklendi!",
        f"Aktif Mod Sayısı: {len(mod_manager.active_mods)}",
        "Modlar artık kendi klasörlerinde ve manifest.json ile çalışıyor!"
    ]

    for i, line in enumerate(about_lines):
        text = FONT_TEXT.render(line, True, WHITE)
        screen.blit(text, (WIDTH // 6, HEIGHT // 3 + i * 40))

    pygame.display.flip()
    pygame.time.wait(5000)

def main():
    # Önce tüm asset'leri yükle
    dialogs = [
        "Haha keriz, gerçekten bunu gerçek bitcoin sandın mı?",
        "Ben kim miyim Bitrüs'üm yakında çok daha iyi tanıyacaksın...",
        "Şimdi bilgisayarının boku yedi!",
        "Beni yenemezsin istediğni yapsan bile haha bana karşı koymaya çalışma.",
        "Sen:göreceğz aşağılık piç.",
        "amk laaaaaan senininnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn."
    ]

    try:
        background = pygame.image.load(BACKGROUND_PATH)
        bitcoin_icon = pygame.image.load(BITCOIN_ICON_PATH)
        gallery_icon = pygame.image.load(GALLERY_ICON_PATH)
        about_icon = pygame.image.load(ABOUT_ICON_PATH)
        virus_image = pygame.image.load(VIRUS_IMAGE_PATH)
        wantvirus_image = pygame.image.load(WANTVIRUS_IMAGE_PATH)

        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        bitcoin_icon = pygame.transform.scale(bitcoin_icon, (96, 96))
        gallery_icon = pygame.transform.scale(gallery_icon, (96, 96))
        about_icon = pygame.transform.scale(about_icon, (96, 96))
        virus_image = pygame.transform.scale(virus_image, (300, 300))
        wantvirus_image = pygame.transform.scale(wantvirus_image, (300, 300))
    except Exception as e:
        print(f"Asset yüklenemedi: {e}")
        pygame.quit()
        sys.exit()

    bitcoin_rect = bitcoin_icon.get_rect(topleft=(20, 20))
    gallery_rect = gallery_icon.get_rect(topleft=(20, 20 + 96 + 10))
    about_rect = about_icon.get_rect(topleft=(20, 20 + 2 * (96 + 10)))

    dialog_mode = False
    current_dialog = 0
    dialog_start_time = 0
    dialog_delay = 5000

    game_data = {
        'screen': screen,
        'WIDTH': WIDTH,
        'HEIGHT': HEIGHT,
        'current_state': 'menu'
    }
    
    mod_manager.call_hook('on_game_start', game_data)
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        screen.blit(background, (0, 0))

        if not dialog_mode:
            screen.blit(bitcoin_icon, bitcoin_rect)
            screen.blit(gallery_icon, gallery_rect)
            screen.blit(about_icon, about_rect)
        else:
            screen.blit(virus_image, (WIDTH // 2 - virus_image.get_width() // 2, HEIGHT // 2 - 300))
            pygame.draw.rect(screen, BLACK, (100, HEIGHT - 150, WIDTH - 200, 100))
            pygame.draw.rect(screen, WHITE, (100, HEIGHT - 150, WIDTH - 200, 100), 3)

            if current_dialog < len(dialogs):
                current_text = dialogs[current_dialog]
                
                # Dialog hook'u çağır
                hook_results = mod_manager.call_hook('on_dialog_show', current_text, game_data)
                if hook_results:
                    for result in hook_results:
                        if isinstance(result, tuple) and len(result) >= 2:
                            current_text = result[0]
                            game_data = result[1]
                            break

                text = FONT.render(current_text, True, WHITE)
                screen.blit(text, (120, HEIGHT - 120))

                if pygame.time.get_ticks() - dialog_start_time > dialog_delay:
                    current_dialog += 1
                    dialog_start_time = pygame.time.get_ticks()
            else:
                running = False
        
        # Screen update hook'u çağır
        mod_manager.call_hook('on_screen_update', screen, game_data)
        
        # Her frame mod'ları güncelle
        mod_manager.update_mods(game_data)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # M tuşu ile mod menüsünü aç
                if event.key == pygame.K_m:
                    if not show_mod_menu(screen):
                        running = False
                
                # Mod key handler'ını çağır
                mod_manager.handle_key_press(event.key, game_data)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                # Mouse click hook'u çağır
                mod_manager.handle_mouse_click(pos, event.button, game_data)
                
                if not dialog_mode:
                    clicked_icon = None
                    if bitcoin_rect.collidepoint(pos):
                        clicked_icon = "bitcoin"
                        dialog_mode = True
                        current_dialog = 0
                        dialog_start_time = pygame.time.get_ticks()
                    elif gallery_rect.collidepoint(pos):
                        clicked_icon = "gallery"
                        start_gallery_app(screen)
                    elif about_rect.collidepoint(pos):
                        clicked_icon = "about"
                        start_about_app(screen)
                    
                    if clicked_icon:
                        mod_manager.call_hook('on_icon_click', clicked_icon, game_data)

        pygame.display.flip()
        clock.tick(60)


  

    

    mod_manager.call_hook('on_minigame_start', 'notdie', game_data)
    start_notdie(screen, bitrus_img, pc_img, wantvirus_img, rocket_img, nuke_img , explosion_sound)
    mod_manager.call_hook('on_minigame_end', 'notdie', game_data)

    
    # Oyun bitişi hook'u çağır
    mod_manager.call_hook('on_game_end', game_data)
  
    pygame.quit()
    sys.exit()

pygame.mixer.init()

# Müzik dosyalarının yolu
muzikler = [
    "assets/music/menu_music.mp3",
]

# Rastgele bir müzik seç
secilen_muzik = random.choice(muzikler)

# Müzik çalma
pygame.mixer.music.load(secilen_muzik)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Sonsuz döngüde çal

if __name__ == "__main__":
    main()
