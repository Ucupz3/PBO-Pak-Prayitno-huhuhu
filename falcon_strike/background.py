import pygame
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT


# ======================================================================== #
#  KOMPONEN HUJAN & AWAN (untuk BackgroundLaut)                             #
# ======================================================================== #
class RintikHujanPixel:
    def __init__(self):
        self.x       = random.randint(0, SCREEN_WIDTH)
        self.y       = random.randint(-50, -10)
        self.lebar   = 2
        self.panjang = random.randint(15, 30)
        self.speed_y = random.randint(12, 18)
        self.speed_x = random.randint(-4, -2)
        self.warna   = (175, 215, 245)

    def update(self):
        self.y += self.speed_y
        self.x += self.speed_x

    def draw(self, permukaan):
        pygame.draw.line(permukaan, self.warna,
                        (self.x, self.y),
                        (self.x + self.speed_x, self.y + self.panjang),
                        self.lebar)


class AwanPixel:
    def __init__(self):
        self.x           = random.randint(-100, SCREEN_WIDTH)
        self.y           = random.randint(-120, -60)
        self.lebar_blok  = random.randint(60, 120)
        self.tinggi_blok = random.randint(25, 50)
        self.speed       = random.uniform(0.5, 1.0)

        self.surface_awan  = pygame.Surface((self.lebar_blok + 40, self.tinggi_blok + 30), pygame.SRCALPHA)
        self.waktu_mendung = False
        self.update_warna(mendung=False)

    def update_warna(self, mendung):
        self.waktu_mendung = mendung
        self.surface_awan.fill((0, 0, 0, 0))
        if mendung:
            c_utama  = (110, 125, 145, 180)
            c_bayang = (80,  95,  115, 140)
        else:
            c_utama  = (255, 255, 255,  65)
            c_bayang = (200, 220, 240,  40)
        w = self.lebar_blok
        h = self.tinggi_blok
        pygame.draw.rect(self.surface_awan, c_utama,  (20,  10, w,      h     ))
        pygame.draw.rect(self.surface_awan, c_utama,  (40,   0, w - 40, h     ))
        pygame.draw.rect(self.surface_awan, c_utama,  ( 0,  15, w + 30, h - 15))
        pygame.draw.rect(self.surface_awan, c_bayang, (10, h + 5, w,    8     ))

    def update(self):
        self.y += self.speed

    def draw(self, permukaan):
        permukaan.blit(self.surface_awan, (int(self.x), int(self.y)))


#  BACKGROUND LAUT (original)
class Background:
    """Background laut dengan siklus cuaca cerah → hujan setiap 90 detik."""

    def __init__(self, speed=2):
        self.daftar_hujan    = []
        self.daftar_awan     = []
        self.waktu_mulai     = pygame.time.get_ticks()
        self.status_cuaca_lama = False

        self.surface_cerah = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface_cerah.fill((30, 90, 150))

        self.surface_mendung = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface_mendung.fill((22, 55, 95))

        for y in range(0, SCREEN_HEIGHT, 4):
            for x in range(0, SCREEN_WIDTH, 4):
                if (x + y) % 8 == 0:
                    pygame.draw.rect(self.surface_cerah,   (40, 110, 175), (x, y, 2, 2))
                    pygame.draw.rect(self.surface_mendung, (28,  70, 115), (x, y, 2, 2))

        for _ in range(4):
            a   = AwanPixel()
            a.y = random.randint(0, SCREEN_HEIGHT)
            self.daftar_awan.append(a)

    def update(self):
        waktu_sekarang  = pygame.time.get_ticks()
        durasi_berjalan = waktu_sekarang - self.waktu_mulai
        durasi_siklus   = durasi_berjalan % 90000
        is_hujan        = durasi_siklus >= 60000

        if is_hujan != self.status_cuaca_lama:
            self.status_cuaca_lama = is_hujan
            for awan in self.daftar_awan:
                awan.update_warna(mendung=is_hujan)

        for rintik in self.daftar_hujan[:]:
            rintik.update()
            if rintik.y > SCREEN_HEIGHT or rintik.x < -20:
                self.daftar_hujan.remove(rintik)

        for awan in self.daftar_awan[:]:
            awan.update()
            if awan.y > SCREEN_HEIGHT:
                self.daftar_awan.remove(awan)

        if is_hujan:
            for _ in range(4):
                self.daftar_hujan.append(RintikHujanPixel())

        if random.random() < 0.008:
            awan_baru = AwanPixel()
            awan_baru.update_warna(mendung=is_hujan)
            self.daftar_awan.append(awan_baru)

    def draw(self, permukaan):
        if self.status_cuaca_lama:
            permukaan.blit(self.surface_mendung, (0, 0))
        else:
            permukaan.blit(self.surface_cerah, (0, 0))
        for awan in self.daftar_awan:
            awan.draw(permukaan)
        for rintik in self.daftar_hujan:
            rintik.draw(permukaan)


KECEPATAN_KAKTUS_SERAGAM = 2.2


#  KOMPONEN PADANG PASIR                                                  
class PartikelDebu:
    """Efek debu/pasir yang terbang horizontal ditiup angin gurun."""
    WARNA_PASIR = [
        (230, 190, 120),   
        (210, 160, 90),    
        (245, 215, 150),   
    ]

    def __init__(self):
        self.reset()

    def reset(self, dari_kanan=True):
        self.x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 50) if dari_kanan else random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.size_w = random.randint(4, 10)  
        self.size_h = random.randint(1, 3)
        self.speed_x = random.uniform(-4.0, -2.0)  
        self.speed_y = random.uniform(-0.2, 0.2)
        self.warna = random.choice(self.WARNA_PASIR)
        self.alpha = random.randint(100, 180)

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, permukaan):
        s = pygame.Surface((self.size_w, self.size_h), pygame.SRCALPHA)
        s.fill((*self.warna, self.alpha))
        permukaan.blit(s, (int(self.x), int(self.y)))


class KaktusLayer:
    """
    Layer tanaman kaktus yang bergerak maju secara VERTIKAL dengan 
    kecepatan lambat dan seragam.
    """
    def __init__(self, jumlah=5, y_range=(0, SCREEN_HEIGHT),
                warna_kaktus=(40, 110, 60), ukuran_range=(40, 70)):
        self.kaktus = []

        for _ in range(jumlah):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(y_range[0], y_range[1])
            ukuran = random.randint(*ukuran_range)
            self.kaktus.append({
                "x": x, "y": y,
                "ukuran": ukuran,
                "warna_k": warna_kaktus,
            })

    def update(self):
        for k in self.kaktus:
            k["y"] += KECEPATAN_KAKTUS_SERAGAM
            
            if k["y"] > SCREEN_HEIGHT + k["ukuran"]:
                k["y"] = -k["ukuran"]
                k["x"] = random.randint(0, SCREEN_WIDTH)

    def draw(self, permukaan):
        for k in self.kaktus:
            x, y, uk = int(k["x"]), int(k["y"]), k["ukuran"]
            w_k = k["warna_k"]
            w_k_gelap = tuple(max(0, c - 25) for c in w_k)

            w_batang = uk // 4
            h_batang = uk
            pygame.draw.rect(permukaan, w_k, (x - w_batang // 2, y - h_batang, w_batang, h_batang))
            pygame.draw.rect(permukaan, w_k_gelap, (x, y - h_batang, w_batang // 2, h_batang))

            if uk > 30:
                w_cabang = w_batang // 2
                h_cabang = h_batang // 2
                pygame.draw.rect(permukaan, w_k_gelap, (x - w_batang // 2 - w_cabang * 2, y - h_batang * 2 // 3, w_cabang * 2, w_cabang))
                pygame.draw.rect(permukaan, w_k, (x - w_batang // 2 - w_cabang * 2, y - h_batang * 2 // 3 - h_cabang, w_cabang, h_cabang))

            # 3. Cabang Kanan
            if uk > 45:
                w_cabang = w_batang // 2
                h_cabang = h_batang // 3
                pygame.draw.rect(permukaan, w_k_gelap, (x + w_batang // 2, y - h_batang // 2, w_cabang * 2, w_cabang))
                pygame.draw.rect(permukaan, w_k_gelap, (x + w_batang // 2 + w_cabang, y - h_batang // 2 - h_cabang, w_cabang, h_cabang))



#  BACKGROUND PADANG PASIR BERGERAK SERAGAM 
class BackgroundPadangPasir:
    """
    Background hamparan padang pasir dengan kaktus yang bergulir 
    secara seragam dan lambat ke bawah.
    """

    def __init__(self, speed=2):
        self.speed = speed
        self.waktu_mulai = pygame.time.get_ticks()

        self.daftar_debu = [PartikelDebu() for _ in range(35)]
        for d in self.daftar_debu:
            d.reset(dari_kanan=False)

        self.layer_jauh = KaktusLayer(
            jumlah=4, y_range=(0, int(SCREEN_HEIGHT * 0.3)),
            warna_kaktus=(80, 130, 95), ukuran_range=(20, 35)
        )
        self.layer_tengah = KaktusLayer(
            jumlah=3, y_range=(int(SCREEN_HEIGHT * 0.3), int(SCREEN_HEIGHT * 0.6)),
            warna_kaktus=(55, 115, 75), ukuran_range=(40, 55)
        )
        self.layer_dekat = KaktusLayer(
            jumlah=3, y_range=(int(SCREEN_HEIGHT * 0.6), SCREEN_HEIGHT),
            warna_kaktus=(35, 95, 55), ukuran_range=(65, 90)
        )

        self.surface_siang = self._buat_suasana_siang()
        self.surface_senja = self._buat_suasana_senja()
        self.fase_senja = False

    def _buat_suasana_siang(self):
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(235 + t * 15)
            g = int(200 + t * 20)
            b = int(120 - t * 30)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))
            
        for yy in range(0, SCREEN_HEIGHT, 6):
            for xx in range(0, SCREEN_WIDTH, 6):
                if (xx + yy) % 4 == 0:
                    pygame.draw.rect(surf, (215, 175, 100), (xx, yy, 2, 1))
        return surf

    def _buat_suasana_senja(self):
        surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        for y in range(SCREEN_HEIGHT):
            t = y / SCREEN_HEIGHT
            r = int(180 + t * 40)
            g = int(95 + t * 25)
            b = int(45 + t * 15)
            pygame.draw.line(surf, (r, g, b), (0, y), (SCREEN_WIDTH, y))

        for yy in range(0, SCREEN_HEIGHT, 6):
            for xx in range(0, SCREEN_WIDTH, 6):
                if (xx + yy) % 4 == 0:
                    pygame.draw.rect(surf, (150, 70, 30), (xx, yy, 2, 1))
        return surf

    def update(self):
        waktu_sekarang = pygame.time.get_ticks()
        durasi = (waktu_sekarang - self.waktu_mulai) % 90000
        self.fase_senja = durasi >= 60000

        self.layer_jauh.update()
        self.layer_tengah.update()
        self.layer_dekat.update()


        for d in self.daftar_debu:
            d.update()
            if d.x < -20:
                d.reset(dari_kanan=True)

    def draw(self, permukaan):
        if self.fase_senja:
            permukaan.blit(self.surface_senja, (0, 0))
        else:
            permukaan.blit(self.surface_siang, (0, 0))

        self.layer_jauh.draw(permukaan)
        self.layer_tengah.draw(permukaan)
        self.layer_dekat.draw(permukaan)

        for d in self.daftar_debu:
            d.draw(permukaan)