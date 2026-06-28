import pygame
import sys
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PUTIH
from sistem_save import muat_semua_data

# DEFINISI PALET WARNA MILITER UTAMA
HIJAU_ARMY   = (75, 83, 32)
HIJAU_LUMUT  = (85, 107, 47)
COKLAT_TANAH = (139, 90, 43)
BG_MILITER   = (18, 22, 15)
EMAS_TAKTIK  = (212, 175, 55)

def _play(ui_sounds, key):
    """Helper aman: mainkan sound dari dict ui_sounds tanpa crash jika None"""
    snd = ui_sounds.get(key) if ui_sounds else None
    if snd:
        snd.play()

class MenuUtama:
    def __init__(self, layar, ui_sounds=None):
        self.layar      = layar
        self.ui_sounds  = ui_sounds

        self.font_judul    = pygame.font.SysFont("Impact", 65)
        self.font_subjudul = pygame.font.SysFont("Arial", 16, bold=True)
        self.font_pilihan  = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_kecil    = pygame.font.SysFont("Arial", 18)
        self.font_hud      = pygame.font.SysFont("Consolas", 16)

        self.opsi             = ["NEW GAME", "LOAD GAME", "EXIT"]
        self.pilihan_sekarang = 0

    #  HELPER INTERNAL
    def _play(self, key):
        _play(self.ui_sounds, key)

    def _gambar_background_taktis(self):
        """Background bertema military radar/grid interface"""
        self.layar.fill(BG_MILITER)
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(self.layar, (30, 38, 24), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(self.layar, (30, 38, 24), (0, y), (SCREEN_WIDTH, y), 1)
        pygame.draw.rect(self.layar, HIJAU_ARMY,    (15, 15, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30), 2)
        pygame.draw.rect(self.layar, COKLAT_TANAH,  (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 1)


    #  LAYAR MENU UTAMA
    def tampilkan(self):
        """Menu utama — navigasi ATAS/BAWAH + ENTER konfirmasi"""
        running_menu = True
        clock        = pygame.time.Clock()

        while running_menu:
            clock.tick(30)
            self._gambar_background_taktis()
            # --- Judul ---
            teks_shadow = self.font_judul.render("FALCON STRIKE", True, (10, 12, 8))
            self.layar.blit(teks_shadow, teks_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 4, 134)))
            teks_judul = self.font_judul.render("FALCON STRIKE", True, PUTIH)
            self.layar.blit(teks_judul, teks_judul.get_rect(center=(SCREEN_WIDTH // 2, 130)))
            teks_sub = self.font_subjudul.render("TACTICAL AIR COMBAT SYSTEM v1.0", True, HIJAU_LUMUT)
            self.layar.blit(teks_sub, teks_sub.get_rect(center=(SCREEN_WIDTH // 2, 185)))

            # --- Opsi Menu ---
            for i, opsi in enumerate(self.opsi):
                is_selected = (i == self.pilihan_sekarang)
                warna_teks  = EMAS_TAKTIK if is_selected else (180, 190, 170)
                teks_render = f"[ {opsi} ]" if is_selected else opsi

                if is_selected:
                    lebar_box, tinggi_box = 280, 45
                    x_box = SCREEN_WIDTH // 2 - lebar_box // 2
                    y_box = 280 + (i * 65) - 8
                    s = pygame.Surface((lebar_box, tinggi_box), pygame.SRCALPHA)
                    s.fill((75, 83, 32, 100))
                    self.layar.blit(s, (x_box, y_box))
                    pygame.draw.rect(self.layar, HIJAU_LUMUT, (x_box, y_box, lebar_box, tinggi_box), 2)

                render_opsi = self.font_pilihan.render(teks_render, True, warna_teks)
                self.layar.blit(render_opsi, render_opsi.get_rect(center=(SCREEN_WIDTH // 2, 290 + (i * 65))))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.pilihan_sekarang = (self.pilihan_sekarang - 1) % len(self.opsi)
                        self._play("pilih")

                    elif event.key == pygame.K_DOWN:
                        self.pilihan_sekarang = (self.pilihan_sekarang + 1) % len(self.opsi)
                        self._play("pilih")

                    elif event.key == pygame.K_RETURN:
                        self._play("oke")         
                        return self.opsi[self.pilihan_sekarang]

    #  LAYAR INPUT NAMA PEMAIN BARU
    def input_nama_pemain(self):
        """Input nama pilot baru — [ENTER] konfirmasi, [ESC] kembali"""
        nama      = ""
        inputting = True
        clock     = pygame.time.Clock()

        while inputting:
            clock.tick(30)
            self._gambar_background_taktis()

            teks_tanya = self.font_pilihan.render("ENLIST PILOT", True, PUTIH)
            self.layar.blit(teks_tanya, teks_tanya.get_rect(center=(SCREEN_WIDTH // 2, 180)))

            lebar_input, tinggi_input = 340, 60
            x_input = SCREEN_WIDTH // 2 - lebar_input // 2
            y_input = 240
            pygame.draw.rect(self.layar, (25, 30, 20), (x_input, y_input, lebar_input, tinggi_input))
            pygame.draw.rect(self.layar, COKLAT_TANAH, (x_input, y_input, lebar_input, tinggi_input), 2)

            teks_nama = self.font_pilihan.render(nama + "_", True, EMAS_TAKTIK)
            self.layar.blit(teks_nama, teks_nama.get_rect(center=(SCREEN_WIDTH // 2, 270)))

            teks_info = self.font_kecil.render("PRESS [ENTER] TO CONFIRM DATA", True, HIJAU_LUMUT)
            self.layar.blit(teks_info, teks_info.get_rect(center=(SCREEN_WIDTH // 2, 420)))

            # Footer
            teks_batal = self.font_hud.render("[ESC] BACK", True, (200, 80, 80))
            self.layar.blit(teks_batal, (45, SCREEN_HEIGHT - 50))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if nama.strip() != "":
                            self._play("oke")
                            return nama.strip().upper()

                    elif event.key == pygame.K_ESCAPE:
                        self._play("leave")
                        return None

                    elif event.key == pygame.K_BACKSPACE:
                        nama = nama[:-1]

                    else:
                        if len(nama) < 10 and event.unicode.isalnum():
                            nama += event.unicode

    #  LAYAR LOAD GAME
    def layar_load_game(self):
        """Layar Load Profile — pilih profil dari arsip log"""
        data        = muat_semua_data()
        daftar_nama = list(data.keys())

        # --- Database kosong ---
        if not daftar_nama:
            self._gambar_background_taktis()
            pygame.draw.rect(self.layar, (50, 15, 15),    (SCREEN_WIDTH // 2 - 200, 200, 400, 140))
            pygame.draw.rect(self.layar, (200, 50, 50),   (SCREEN_WIDTH // 2 - 200, 200, 400, 140), 2)

            teks  = self.font_pilihan.render("DATABASE IS EMPTY!", True, (255, 100, 100))
            teks2 = self.font_kecil.render("No save log file found.", True, PUTIH)
            teks3 = self.font_hud.render("Press any key to go back...", True, HIJAU_LUMUT)

            self.layar.blit(teks,  teks.get_rect(center=(SCREEN_WIDTH // 2, 235)))
            self.layar.blit(teks2, teks2.get_rect(center=(SCREEN_WIDTH // 2, 275)))
            self.layar.blit(teks3, teks3.get_rect(center=(SCREEN_WIDTH // 2, 315)))
            pygame.display.flip()

            menunggu = True
            while menunggu:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                    if event.type == pygame.KEYDOWN:
                        self._play("leave")
                        menunggu = False
            return None

        # tambah data
        pilihan_nama_idx = 0
        pilih_load       = True
        clock            = pygame.time.Clock()

        while pilih_load:
            clock.tick(30)
            self._gambar_background_taktis()

            teks_pilih = self.font_pilihan.render("FALCON PROFILE", True, PUTIH)
            self.layar.blit(teks_pilih, (50, 60))
            pygame.draw.line(self.layar, COKLAT_TANAH, (50, 100), (SCREEN_WIDTH - 50, 100), 2)

            # Daftar nama
            for i, nama in enumerate(daftar_nama):
                is_selected = (i == pilihan_nama_idx)
                warna       = EMAS_TAKTIK if is_selected else (160, 170, 150)

                if is_selected:
                    pygame.draw.rect(self.layar, HIJAU_ARMY,  (45, 132 + (i * 50), 150, 38))
                    pygame.draw.rect(self.layar, HIJAU_LUMUT, (45, 132 + (i * 50), 150, 38), 1)
                    teks_item = f"> {nama:<10}"
                else:
                    teks_item = f"  {nama:<10}"

                render_item = self.font_pilihan.render(teks_item, True, warna)
                self.layar.blit(render_item, (50, 135 + (i * 50)))

            # Panel info kanan mabre
            nama_sorot = daftar_nama[pilihan_nama_idx]
            stats      = data[nama_sorot]

            box_width, box_height = 250, 250
            x_box, y_box          = SCREEN_WIDTH - 290, 130

            s_box = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
            s_box.fill((35, 42, 30, 220))
            self.layar.blit(s_box, (x_box, y_box))
            pygame.draw.rect(self.layar, HIJAU_LUMUT, (x_box, y_box, box_width, box_height), 2)

            pygame.draw.line(self.layar, EMAS_TAKTIK, (x_box, y_box),      (x_box + 20, y_box), 3)
            pygame.draw.line(self.layar, EMAS_TAKTIK, (x_box, y_box),      (x_box, y_box + 20), 3)

            ts1 = self.font_kecil.render(f"AIRBASE DATA: {nama_sorot}", True, EMAS_TAKTIK)
            ts2 = self.font_kecil.render(f"P-38 LIGHTNING : {stats.get('PESAWAT_BIASA', 0)} PTS", True, PUTIH)
            ts3 = self.font_kecil.render(f"B-29 BOMBER    : {stats.get('PESAWAT_BOMBER', 0)} PTS", True, PUTIH)
            ts4 = self.font_kecil.render(f"F22 RAPTOR     : {stats.get('PESAWAT_RAPTOR', 0)} PTS", True, PUTIH)

            self.layar.blit(ts1, (x_box + 15, y_box + 25))
            pygame.draw.line(self.layar, COKLAT_TANAH,
                            (x_box + 15, y_box + 55), (x_box + box_width - 15, y_box + 55), 1)
            self.layar.blit(ts2, (x_box + 15, y_box + 75))
            self.layar.blit(ts3, (x_box + 15, y_box + 120))
            self.layar.blit(ts4, (x_box + 15, y_box + 165))

            # Buat Footer
            x_awal = 45
            y_pos  = SCREEN_HEIGHT - 50
            teks_esc_part   = self.font_hud.render("[ESC] BACK", True, (200, 80, 80))
            self.layar.blit(teks_esc_part, (x_awal, y_pos))
            lebar_esc       = teks_esc_part.get_width()
            teks_enter_part = self.font_hud.render("  |  [ENTER] SELECT PROFILE", True, HIJAU_LUMUT)
            self.layar.blit(teks_enter_part, (x_awal + lebar_esc, y_pos))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        pilihan_nama_idx = (pilihan_nama_idx - 1) % len(daftar_nama)
                        self._play("pilih")

                    elif event.key == pygame.K_DOWN:
                        pilihan_nama_idx = (pilihan_nama_idx + 1) % len(daftar_nama)
                        self._play("pilih")

                    elif event.key == pygame.K_RETURN:
                        self._play("oke")
                        return daftar_nama[pilihan_nama_idx]

                    elif event.key == pygame.K_ESCAPE:
                        self._play("leave")
                        return None