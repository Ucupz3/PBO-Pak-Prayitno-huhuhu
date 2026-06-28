import pygame

class EfekLedakan(pygame.sprite.Sprite):
    def __init__(self, x, y, ukuran_maks=40):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = 5
        self.ukuran_maks = ukuran_maks
        self.speed_kembang = 3
        self.image = pygame.Surface((ukuran_maks * 2, ukuran_maks * 2), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        
    def update(self):
        self.radius += self.speed_kembang
        self.image.fill((0, 0, 0, 0)) 
        if self.radius < self.ukuran_maks:
            pygame.draw.circle(self.image, (255, 69, 0), (self.ukuran_maks, self.ukuran_maks), self.radius)
            pygame.draw.circle(self.image, (255, 215, 0), (self.ukuran_maks, self.ukuran_maks), max(1, self.radius - 8))
            pygame.draw.circle(self.image, (255, 255, 255), (self.ukuran_maks, self.ukuran_maks), max(1, self.radius - 15))
        else:
            self.kill() 

    def draw(self, permukaan):
        permukaan.blit(self.image, self.rect)