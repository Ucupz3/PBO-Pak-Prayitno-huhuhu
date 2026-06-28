import pygame
import os
from config import SCREEN_WIDTH

class Pesawat:
    def __init__(self, x, y, nama_file_gambar, speed, hp, cooldown_tembak):
        self.x = x
        self.y = y
        self.speed = speed
        self.hp = hp
        self.max_hp = hp
        self.cooldown_tembak = cooldown_tembak 
        self.last_shot = pygame.time.get_ticks() 

        jalur_gambar = os.path.join("assets", nama_file_gambar)
        self.gambar_asli = pygame.image.load(jalur_gambar)
        
        self.gambar = pygame.transform.scale(self.gambar_asli, (64, 64))
        self.rect = self.gambar.get_rect()
        self.rect.center = (x, y)

    def kendalikan(self):
        tombol = pygame.key.get_pressed()
        if tombol[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if tombol[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Batas Layar
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH

    def gambar_ke_layar(self, layar):
        layar.blit(self.gambar, self.rect)

class PesawatBiasa(Pesawat):
    def __init__(self, x, y):
        super().__init__(x, y, "pesawat_utama.png", speed=5, hp=5, cooldown_tembak=380)
        self.gambar = pygame.transform.scale(self.gambar_asli, (80, 80))
        self.rect = self.gambar.get_rect(center=(x, y))

class PesawatBomber(Pesawat):
    def __init__(self, x, y):
        super().__init__(x, y, "pesawat_bomber.png", speed=3, hp=15, cooldown_tembak=530)
        self.gambar = pygame.transform.scale(self.gambar_asli, (80, 80))
        self.rect = self.gambar.get_rect(center=(x, y))

class PesawatRaptor(Pesawat):
    def __init__(self, x, y):
        super().__init__(x, y, "pesawat_raptor.png", speed=10, hp=3, cooldown_tembak=250)
        self.gambar = pygame.transform.scale(self.gambar_asli, (70, 70))
        self.rect = self.gambar.get_rect(center=(x, y))