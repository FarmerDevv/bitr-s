import pygame
import sys
import os
import importlib.util
import json
import random
import math
import time
import webbrowser
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
pygame.init()
icon = pygame.image.load("assets/pixel_art/bitcoin_icon.png")
pygame.display.set_icon(icon)
ACCENT_COLOR = (100, 200, 255)
GITHUB_URL = "https://github.com/FarmerDevv"
pygame.init()
BG_COLOR = (54, 54, 54)
SAVE_FILE = "save.json"
# Minigame sıralaması (kullanabilirsiniz)
MINIGAMES = [
    "labyrinth_game",
    "virus_defense",
    "new_game",
    "code_race",
    "bitrus_cutscene",
    "bitrus_attack",
    "bitrus_jumpscare",
    "lab_game",
    "chap_1",
    "end_sezon1",
    "notdie"
]

def splash_screen(screen):
    pygame.init()
    WIDTH, HEIGHT = screen.get_size()
    clock = pygame.time.Clock()

    BG_COLOR = (54, 54, 54)
    font = pygame.font.SysFont("Arial", 32, bold=True)
    text = "Farmer Dev tarafından Python teknolojileriyle yapıldı"
    text_surface = font.render(text, True, (200, 200, 200))
    text_rect = text_surface.get_rect(center=(WIDTH//2, HEIGHT//2 + 100))

    logo_path = os.path.join("assets", "pixel_art", "bitcoin_icon.png")
    logo_img = pygame.image.load(logo_path).convert_alpha()
    logo_img = pygame.transform.smoothscale(logo_img, (150, 150))

    duration = 15_000
    start_time = pygame.time.get_ticks()

    # Logo pozisyonu animasyonu
    logo_x = -150
    logo_y = HEIGHT // 2 - 50
    target_x = WIDTH // 2 - 75  # logo genişliği/2 kadar sola

    particles = []
    particle_triggered = False

    running = True
    while running:
        now = pygame.time.get_ticks()
        elapsed = now - start_time
        t = min(elapsed / duration, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(BG_COLOR)

        # Logo soldan sağa hareket
        if logo_x < target_x:
            logo_x += 8
        else:
            logo_x = target_x
            # Particle tetiklenmesi bir kereye mahsus
            if not particle_triggered:
                for _ in range(120):  # taş rengi parçacıklar
                    particles.append({
                        "pos": [WIDTH//2, logo_y + 75],
                        "vel": [random.uniform(-5, 5), random.uniform(-5, 5)],
                        "radius": random.randint(2, 4),
                        "color": (110 + random.randint(0, 30), 100 + random.randint(0, 30), 90),
                        "lifetime": random.randint(40, 100)
                    })
                particle_triggered = True

        # Logo çizimi
        logo_rect = logo_img.get_rect(topleft=(logo_x, logo_y))
        screen.blit(logo_img, logo_rect)

        # Yazı titreme/parlama efekti
        brightness = 150 + 105 * math.sin(t * math.pi * 4)
        text_color = (brightness, brightness, brightness)
        text_surface = font.render(text, True, text_color)
        screen.blit(text_surface, text_rect)

        # Particle güncelleme ve çizim
        for p in particles:
            p["pos"][0] += p["vel"][0]
            p["pos"][1] += p["vel"][1]
            p["vel"][1] += 0.1  # gravity
            p["lifetime"] -= 1
            if p["lifetime"] > 0:
                pygame.draw.circle(screen, p["color"], (int(p["pos"][0]), int(p["pos"][1])), p["radius"])
        # Ölen partikülleri temizle
        particles = [p for p in particles if p["lifetime"] > 0]

        pygame.display.flip()
        clock.tick(60)

        if elapsed >= duration:
            running = False

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
splash_screen(screen)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
FONT = pygame.font.SysFont("Arial", 28)
font_title = pygame.font.SysFont("Arial", 64, bold=True)
font_button = pygame.font.SysFont("Arial", 40)

clock = pygame.time.Clock()

class Button:
    def __init__(self, text, x, y, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, 300, 70)
        self.callback = callback

    def draw(self, surface, mouse_pos):
        color = (70, 70, 70) if self.rect.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        txt = font_button.render(self.text, True, (255, 255, 255))
        surface.blit(txt, (self.rect.x + 30, self.rect.y + 15))

    def click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()

def start_minigame(name):
    print(f"Minigame '{name}' başlatıldı!")  # Buraya oyun başlatma fonksiyonunu ekle

def yeni_oyun():
    save = {"last_minigame": MINIGAMES[0]}
    with open(SAVE_FILE, "w") as f:
        json.dump(save, f)
    start_minigame(MINIGAMES[0])

def devam_et():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            save = json.load(f)
            minigame = save.get("last_minigame", MINIGAMES[0])
            start_minigame(minigame)
    else:
        yeni_oyun()

def oyundan_cik():
    pygame.quit()
    sys.exit()

buttons = [
    Button("Yeni Oyun", WIDTH//2 - 150, 300, yeni_oyun),
    Button("Devam Et", WIDTH//2 - 150, 400, devam_et),
    Button("Oyundan Çık", WIDTH//2 - 150, 500, oyundan_cik)
]

def main_menu():
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                oyundan_cik()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    btn.click(mouse_pos)

        screen.fill(BG_COLOR)

        title_surf = font_title.render("Bitrüs", True, (0, 255, 180))
        title_rect = title_surf.get_rect(center=(WIDTH//2, 150))
        screen.blit(title_surf, title_rect)

        for btn in buttons:
            btn.draw(screen, mouse_pos)

        pygame.display.flip()
        clock.tick(60)
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
wantvirus_img = pygame.image.load("assets/pixel_art/wantvirus.png")
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
    pygame.init()
    screen.fill(BLACK)
    WIDTH, HEIGHT = screen.get_size()

    gallery_images = []
    gallery_rects = []

    valid_exts = (".jpg", ".jpeg", ".png")
    files = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(valid_exts)]

    for filename in files:
        path = os.path.join(ASSETS_DIR, filename)
        try:
            img = pygame.image.load(path).convert_alpha()
            thumbnail = pygame.transform.scale(img, (200, 200))
            gallery_images.append((img, thumbnail))
        except Exception as e:
            print(f"Galeri resmi yüklenemedi: {path}, hata: {e}")

    if not gallery_images:
        print("Galeri klasöründe uygun resim bulunamadı.")
        return

    gallery_start_x = 0
    gap = 50
    thumb_width = 200
    total_width = len(gallery_images) * thumb_width + (len(gallery_images) - 1) * gap
    y = HEIGHT // 3

    viewing = True
    zoom = 1.0
    max_zoom = 5.0
    min_zoom = 0.5
    zoom_step = 0.1
    selected_image = None

    img_pos_x = 0
    img_pos_y = 0
    dragging_big = False
    drag_start_mouse_big = (0, 0)
    drag_start_img_big = (0, 0)

    dragging_gallery = False
    drag_start_mouse_gallery = (0, 0)
    drag_start_gallery_x = 0

    def draw_gallery():
        screen.fill(BLACK)
        gallery_rects.clear()
        for i, (original, thumbnail) in enumerate(gallery_images):
            x = gallery_start_x + i * (thumb_width + gap)
            rect = pygame.Rect(x, y, thumb_width, 200)
            gallery_rects.append((rect, original))
            screen.blit(thumbnail, (x, y))
        pygame.display.flip()

    draw_gallery()

    while viewing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                viewing = False
                break

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if selected_image is not None:
                        # Büyük moddan çık, küçük galeriye dön
                        selected_image = None
                        img_pos_x = 0
                        img_pos_y = 0
                        draw_gallery()
                    else:
                        # Küçük galeride ESC ise programı kapat
                        viewing = False
                    # ESC tuşu işlendi, döngüyü kır
                    break

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if selected_image:
                        dragging_big = True
                        drag_start_mouse_big = event.pos
                        drag_start_img_big = (img_pos_x, img_pos_y)
                    else:
                        for rect, img in gallery_rects:
                            if rect.collidepoint(event.pos):
                                selected_image = img
                                zoom = 1.0
                                img_pos_x = 0
                                img_pos_y = 0
                                break

                elif event.button == 3:
                    if selected_image is None:
                        dragging_gallery = True
                        drag_start_mouse_gallery = event.pos
                        drag_start_gallery_x = gallery_start_x

                elif event.button == 4:
                    if selected_image:
                        zoom = min(zoom + zoom_step, max_zoom)

                elif event.button == 5:
                    if selected_image:
                        zoom = max(zoom - zoom_step, min_zoom)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging_big = False
                elif event.button == 3:
                    dragging_gallery = False

            elif event.type == pygame.MOUSEMOTION:
                if dragging_big and selected_image:
                    dx = event.pos[0] - drag_start_mouse_big[0]
                    dy = event.pos[1] - drag_start_mouse_big[1]
                    img_pos_x = drag_start_img_big[0] + dx
                    img_pos_y = drag_start_img_big[1] + dy

                elif dragging_gallery and selected_image is None:
                    dx = event.pos[0] - drag_start_mouse_gallery[0]
                    gallery_start_x = drag_start_gallery_x + dx
                    max_x = 0
                    min_x = min(WIDTH - total_width, 0)
                    if gallery_start_x > max_x:
                        gallery_start_x = max_x
                    elif gallery_start_x < min_x:
                        gallery_start_x = min_x
                    draw_gallery()

        if selected_image:
            screen.fill(BLACK)
            img_width = int(selected_image.get_width() * zoom)
            img_height = int(selected_image.get_height() * zoom)
            img_scaled = pygame.transform.scale(selected_image, (img_width, img_height))
            x = (WIDTH - img_width) // 2 + img_pos_x
            y = (HEIGHT - img_height) // 2 + img_pos_y
            screen.blit(img_scaled, (x, y))
            pygame.display.flip()

        pygame.time.delay(10)

def rgb_wave(t, frequency=0.6, phase=0):
    # Zamanla RGB renklerinin yumuşak geçişi için sine dalgası
    r = int((math.sin(frequency * t + phase) + 1) * 127.5)
    g = int((math.sin(frequency * t + phase + 2 * math.pi / 3) + 1) * 127.5)
    b = int((math.sin(frequency * t + phase + 4 * math.pi / 3) + 1) * 127.5)
    return (r, g, b)

def start_about_app(screen):
    pygame.init()
    screen.fill(BLACK)
    WIDTH, HEIGHT = screen.get_size()

    FONT_TITLE = pygame.font.SysFont("Arial", 56, bold=True)
    FONT_TEXT = pygame.font.SysFont("Arial", 28)
    FONT_SMALL = pygame.font.SysFont("Arial", 20, italic=True)

    title_text = "Hakkında"
    title_shadow = FONT_TITLE.render(title_text, True, (30, 30, 30))
    title = FONT_TITLE.render(title_text, True, ACCENT_COLOR)
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 6))
    screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
    screen.blit(title, title_rect)

    about_lines = [
        "Bu uygulama Farmer_Dev tarafından yapıldı.",
        "Python Pygame teknolojisi kullanıldı.",
        "Tüm grafikler ve tasarımlar Farmer_Dev'e aittir.",
        "İyi oyunlar oynadıkça eğlenin!",
        "",
        "Gelişmiş Mod Desteği Eklendi!",
        f"Aktif Mod Sayısı: {len(mod_manager.active_mods)}",
        "Modlar artık kendi klasörlerinde ve manifest.json ile çalışıyor!"
    ]

    start_y = HEIGHT // 3
    line_height = 42

    clock = pygame.time.Clock()
    start_ticks = pygame.time.get_ticks()

    # GitHub ikonunu oluştur
    # İkon PNG yoksa basit bir şekil ile göstereceğiz (yuvarlak içinde "GH")
    icon_size = 60
    icon_pos = (WIDTH - icon_size - 20, HEIGHT - icon_size - 20)
    icon_rect = pygame.Rect(icon_pos[0], icon_pos[1], icon_size, icon_size)

    running = True
    while running:
        t = (pygame.time.get_ticks() - start_ticks) / 1000  # saniye cinsinden zaman

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Sol tık
                    if icon_rect.collidepoint(event.pos):
                        webbrowser.open(GITHUB_URL)

        screen.fill(BLACK)

        # Başlık
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title, title_rect)

        # Yazılar
        for i, line in enumerate(about_lines):
            color = ACCENT_COLOR if i in [5, 6, 7] else WHITE
            text_shadow = FONT_TEXT.render(line, True, (20, 20, 20))
            text = FONT_TEXT.render(line, True, color)
            x = WIDTH // 6
            y = start_y + i * line_height
            screen.blit(text_shadow, (x + 2, y + 2))
            screen.blit(text, (x, y))

        # Alt yazı
        footer_text = "© 2025 Farmer_Dev. Tüm hakları saklıdır."
        footer = FONT_SMALL.render(footer_text, True, (150, 150, 150))
        footer_rect = footer.get_rect(center=(WIDTH // 2, HEIGHT - HEIGHT // 12))
        screen.blit(footer, footer_rect)

        # RGB animasyonlu GitHub ikonu çizimi
        color_rgb = rgb_wave(t)
        pygame.draw.circle(screen, color_rgb, icon_rect.center, icon_size // 2)
        # İkon üzeri "GH" yazısı
        gh_text = FONT_SMALL.render("GH", True, BLACK)
        gh_rect = gh_text.get_rect(center=icon_rect.center)
        screen.blit(gh_text, gh_rect)

        pygame.display.flip()
        clock.tick(60)

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


  

    mod_manager.call_hook('on_minigame_start', 'labyrinth', game_data)
    start_labyrinth_game(screen)
    mod_manager.call_hook('on_minigame_end', 'labyrinth', game_data)

    mod_manager.call_hook('on_minigame_start', 'virus_defense', game_data)
    start_virus_defense(screen, virus_image, wantvirus_image)
    mod_manager.call_hook('on_minigame_end', 'virus_defense', game_data)

    mod_manager.call_hook('on_minigame_start', 'new_game', game_data)
    start_new_game(screen, virus_image)
    mod_manager.call_hook('on_minigame_end', 'new_game', game_data)

    mod_manager.call_hook('on_minigame_start', 'code_race', game_data)
    start_code_race(screen, bitrus_img)
    mod_manager.call_hook('on_minigame_end', 'code_race', game_data)

    mod_manager.call_hook('on_minigame_start', 'system_check', game_data)
    start_bitrus_cutscene(screen, bitrus_img, kir_img)
    mod_manager.call_hook('on_minigame_end', 'system_check', game_data)

    mod_manager.call_hook('on_minigame_start', 'bitrus_attack', game_data)
    start_bitrus_attack(screen, bitrus_img, pc_img)
    mod_manager.call_hook('on_minigame_end', 'bitrus_attack', game_data)

    mod_manager.call_hook('on_minigame_start', 'jumpscare', game_data)
    start_bitrus_jumpscare(screen, bitrus_img, human_img, human_sound)
    mod_manager.call_hook('on_minigame_end', 'jumpscare', game_data)

    mod_manager.call_hook('on_minigame_start', 'lab_game', game_data)
    start_lab_game(screen, bitrus_img, pc_img)
    mod_manager.call_hook('on_minigame_end', 'lab_game', game_data)

    mod_manager.call_hook('on_minigame_start', 'chapter_1', game_data)
    start_chap_1(screen, bitrus_img)
    mod_manager.call_hook('on_minigame_end', 'chapter_1', game_data)

    mod_manager.call_hook('on_minigame_start', 'end_sezon1', game_data)
    start_end_sezon1(screen, bitrus_img)
    mod_manager.call_hook('on_minigame_end', 'end_sezon1', game_data)

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
