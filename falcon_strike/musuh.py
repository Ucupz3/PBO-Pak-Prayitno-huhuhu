import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT

# CLASS UTAMA INDUK MUSUH
class Musuh(pygame.sprite.Sprite):
    def __init__(self, nama_file_gambar, hp, speed, ukuran, skor_poin):
        super().__init__()
        try:
            gambar_asli = pygame.image.load(nama_file_gambar).convert_alpha()
            self.image = pygame.transform.scale(gambar_asli, ukuran)
        except pygame.error:
            self.image = pygame.Surface(ukuran)
            self.image.fill((200, 50, 50))
            
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - ukuran[0])
        self.rect.y = random.randint(-150, -50)
        
        self.hp = hp
        self.max_hp = hp
        self.speed = speed
        self.skor_poin = skor_poin

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


#3 JENIS PESAWAT MUSUH
class MusuhKroco(Musuh):
    def __init__(self):
        super().__init__(nama_file_gambar="assets/kroco.png", hp=1, speed=5, ukuran=(35, 35), skor_poin=10)


class MusuhTangguh(Musuh):
    def __init__(self):
        super().__init__(nama_file_gambar="assets/tangguh.png", hp=3, speed=3, ukuran=(50, 45), skor_poin=30)


class MusuhElite(Musuh):
    def __init__(self):
        super().__init__(nama_file_gambar="assets/elite.png", hp=8, speed=2.5, ukuran=(75, 65), skor_poin=100)