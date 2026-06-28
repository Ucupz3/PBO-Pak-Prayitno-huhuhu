import pygame
import math


# --- 1. PELURU BIASA / GANDA (Kuning Menyala) ---
class Peluru:
    def __init__(self, x, y, sudut=0):
        surface_asal = pygame.Surface((6, 15), pygame.SRCALPHA)
        if sudut == 0:
            surface_asal.fill((255, 255, 0))   # Kuning
        else:
            surface_asal.fill((255, 50, 50))    # Merah serong
        self.image = pygame.transform.rotate(surface_asal, -sudut)
        self.rect  = self.image.get_rect(center=(x, y))
        self.speed = 11
        self.vx    = self.speed * math.sin(math.radians(sudut))
        self.vy    = -self.speed * math.cos(math.radians(sudut))

    def update(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

    def draw(self, layar):
        layar.blit(self.image, self.rect)


# --- 2. PELURU SERONG: 2 depan kuning + 2 serong merah ---
class PeluruSerong:
    def __init__(self, x, y):
        self.sub_peluru = [
            Peluru(x - 15, y, sudut=0),    # depan kiri  - KUNING
            Peluru(x + 15, y, sudut=0),    # depan kanan - KUNING
            Peluru(x - 15, y, sudut=-20),  # serong kiri - MERAH
            Peluru(x + 15, y, sudut=20),   # serong kanan- MERAH
        ]
        self.rect = pygame.Rect(x, y, 1, 1)

    def update(self):
        for p in self.sub_peluru:
            p.update()

    def draw(self, layar):
        for p in self.sub_peluru:
            p.draw(layar)


# --- 3. LASER TUNGGAL (Cyan tebal) ---
class Laser:
    def __init__(self, x, y):
        self.image = pygame.Surface((12, 40))
        self.image.fill((0, 255, 255))
        self.rect  = self.image.get_rect(center=(x, y))
        self.speed = 20

    def update(self):
        self.rect.y -= self.speed

    def draw(self, layar):
        layar.blit(self.image, self.rect)


# --- 4. LASER DOUBLE: 2 laser sejajar (ganda + laser) ---
class LaserGanda:
    def __init__(self, x, y):
        self.sub_peluru = [
            Laser(x - 15, y),
            Laser(x + 15, y),
        ]
        self.rect = pygame.Rect(x, y, 1, 1)

    def update(self):
        for p in self.sub_peluru:
            p.update()

    def draw(self, layar):
        for p in self.sub_peluru:
            p.draw(layar)


# --- 5. LASER MINI bergerak serong (untuk LaserSerong) ---
class LaserMini:
    def __init__(self, x, y, sudut=0):
        w, h = 8, 28
        surface_asal = pygame.Surface((w, h), pygame.SRCALPHA)
        surface_asal.fill((0, 200, 255))
        glow = pygame.Rect(2, 4, w - 4, h - 8)
        pygame.draw.rect(surface_asal, (180, 240, 255), glow)
        self.image = pygame.transform.rotate(surface_asal, -sudut)
        self.rect  = self.image.get_rect(center=(x, y))
        self.speed = 14
        self.vx    = self.speed * math.sin(math.radians(sudut))
        self.vy    = -self.speed * math.cos(math.radians(sudut))

    def update(self):
        self.rect.x += int(self.vx)
        self.rect.y += int(self.vy)

    def draw(self, layar):
        layar.blit(self.image, self.rect)


# --- 6. LASER SERONG: 2 laser penuh depan + 2 laser mini serong ---
class LaserSerong:
    def __init__(self, x, y):
        self.sub_peluru = [
            Laser(x - 15, y),                 # depan kiri  - ukuran penuh (12x40)
            Laser(x + 15, y),                 # depan kanan - ukuran penuh (12x40)
            LaserMini(x - 15, y, sudut=-20),  # serong kiri
            LaserMini(x + 15, y, sudut=20),   # serong kanan
        ]
        self.rect = pygame.Rect(x, y, 1, 1)

    def update(self):
        for p in self.sub_peluru:
            p.update()

    def draw(self, layar):
        for p in self.sub_peluru:
            p.draw(layar)