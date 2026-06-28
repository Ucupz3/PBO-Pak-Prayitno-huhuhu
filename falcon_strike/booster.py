import pygame
from config import SCREEN_HEIGHT

class Booster(pygame.sprite.Sprite):
    def __init__(self, x, y, jenis):
        super().__init__()
        self.jenis = jenis  # "ganda", "serong", "laser", atau "speed"
        
        # Font kecil untuk huruf penanda di dalam kotak item
        font_item = pygame.font.SysFont("Arial", 16, bold=True)
        
        # Membuat surface kotak transparan kecil ukuran 25x25 pixel
        self.image = pygame.Surface((25, 25), pygame.SRCALPHA)
        
        # Atur warna dan huruf inisial berdasarkan jenis booster
        if jenis == "ganda":
            warna = (255, 255, 0)   # Kuning
            huruf = "D"             # Double
        elif jenis == "serong":
            warna = (255, 50, 50)   # Merah
            huruf = "S"             # Spread / Serong
        elif jenis == "laser":
            warna = (0, 255, 255)   # Cyan / Biru Muda
            huruf = "L"             # Laser
        elif jenis == "speed":
            warna = (50, 255, 50)   # Hijau Neon (BARU!)
            huruf = "H"             # Hyper Speed
            
        # Gambar background kotak dengan sudut agak bulat (border_radius)
        pygame.draw.rect(self.image, warna, [0, 0, 25, 25], border_radius=5)
        
        # Cetak teks huruf di tengah kotak (huruf warna hitam)
        teks_huruf = font_item.render(huruf, True, (0, 0, 0))
        self.image.blit(teks_huruf, (7, 3))
        
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2  # Kecepatan booster meluncur jatuh ke bawah

    def update(self):
        # Booster bergerak turun perlahan
        self.rect.y += self.speed
        # Otomatis hapus dari memory kalau lolos dari layar bawah biar gak lag
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()