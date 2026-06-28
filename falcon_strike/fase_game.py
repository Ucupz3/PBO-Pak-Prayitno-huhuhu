import pygame
import sys
import math
import random
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PUTIH
from pesawat import PesawatBiasa, PesawatBomber, PesawatRaptor
from sistem_save import simpan_skor_pemain, ambil_high_score_pemain
from background import Background, BackgroundPadangPasir

# DEFINISI PALET WARNA MILITER PREMIUM
HIJAU_ARMY   = (75, 83, 32)
HIJAU_LUMUT  = (85, 107, 47)
COKLAT_TANAH = (139, 90, 43)
BG_MILITER   = (18, 22, 15)
EMAS_TAKTIK  = (212, 175, 55)


def _play(ui_sounds, key):
    snd = ui_sounds.get(key) if ui_sounds else None
    if snd:
        snd.play()


def _gambar_background_taktis_lokal(layar):
    layar.fill(BG_MILITER)
    for x in range(0, SCREEN_WIDTH, 40):
        pygame.draw.line(layar, (30, 38, 24), (x, 0), (x, SCREEN_HEIGHT), 1)
    for y in range(0, SCREEN_HEIGHT, 40):
        pygame.draw.line(layar, (30, 38, 24), (0, y), (SCREEN_WIDTH, y), 1)
    pygame.draw.rect(layar, HIJAU_ARMY,   (15, 15, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30), 2)
    pygame.draw.rect(layar, COKLAT_TANAH, (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 1)


# ======================================================================== #
#  MENU PILIHAN PESAWAT                                                     #
# ======================================================================== #
def menu_pilihan(layar, font, nama_pemain, ui_sounds=None):
    pilih = True
    clock = pygame.time.Clock()

    daftar_pesawat = [
        {"nama": "P-38 Lightning",     "kelas": "PESAWAT_BIASA",   "objek": PesawatBiasa},
        {"nama": "B-29 Superfortress", "kelas": "PESAWAT_BOMBER",  "objek": PesawatBomber},
        {"nama": "F22 Raptor",         "kelas": "PESAWAT_RAPTOR",  "objek": PesawatRaptor},
    ]

    pilihan_sekarang = 0
    font_hud         = pygame.font.SysFont("Consolas", 16)

    while pilih:
        clock.tick(30)
        _gambar_background_taktis_lokal(layar)

        teks1 = font.render(f"AIRCRAFT SELECT:", True, PUTIH)
        layar.blit(teks1, (45, 130))
        pygame.draw.line(layar, COKLAT_TANAH, (45, 175), (SCREEN_WIDTH - 45, 175), 1)

        hs_data = {
            "PESAWAT_BIASA":  ambil_high_score_pemain(nama_pemain, "PESAWAT_BIASA"),
            "PESAWAT_BOMBER": ambil_high_score_pemain(nama_pemain, "PESAWAT_BOMBER"),
            "PESAWAT_RAPTOR": ambil_high_score_pemain(nama_pemain, "PESAWAT_RAPTOR"),
        }

        margin_kiri  = 45
        margin_kanan = SCREEN_WIDTH - 45

        for i, pesawat in enumerate(daftar_pesawat):
            is_selected      = (i == pilihan_sekarang)
            warna_teks       = EMAS_TAKTIK if is_selected else (180, 190, 170)
            teks_nama_armada = f"> {pesawat['nama']}" if is_selected else f"  {pesawat['nama']}"
            y_pos_item       = 220 + (i * 70)

            if is_selected:
                lebar_box  = margin_kanan - margin_kiri
                tinggi_box = 45
                y_box      = y_pos_item - 8
                s = pygame.Surface((lebar_box, tinggi_box), pygame.SRCALPHA)
                s.fill((75, 83, 32, 80))
                layar.blit(s, (margin_kiri, y_box))
                pygame.draw.rect(layar, HIJAU_LUMUT, (margin_kiri, y_box, lebar_box, tinggi_box), 1)

            render_nama = font.render(teks_nama_armada, True, warna_teks)
            layar.blit(render_nama, (margin_kiri + 10, y_pos_item))

            skor_pesawat = hs_data[pesawat['kelas']]
            render_hs    = font_hud.render(
                f"HIGHSCORE: {skor_pesawat} PTS", True,
                EMAS_TAKTIK if is_selected else (130, 140, 120)
            )
            rect_hs = render_hs.get_rect(topright=(margin_kanan - 10, y_pos_item + 5))
            layar.blit(render_hs, rect_hs)

        x_awal = 45
        y_pos  = SCREEN_HEIGHT - 50
        teks_esc      = font_hud.render("[ESC] BACK", True, (200, 80, 80))
        layar.blit(teks_esc, (x_awal, y_pos))
        lebar_esc     = teks_esc.get_width()
        teks_navigasi = font_hud.render("  |  [UP/DOWN] NAVIGATION", True, HIJAU_LUMUT)
        layar.blit(teks_navigasi, (x_awal + lebar_esc, y_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pilihan_sekarang = (pilihan_sekarang - 1) % len(daftar_pesawat)
                    _play(ui_sounds, "pilih")
                elif event.key == pygame.K_DOWN:
                    pilihan_sekarang = (pilihan_sekarang + 1) % len(daftar_pesawat)
                    _play(ui_sounds, "pilih")
                elif event.key == pygame.K_RETURN:
                    _play(ui_sounds, "oke")
                    pesawat_dipilih = daftar_pesawat[pilihan_sekarang]
                    return (
                        pesawat_dipilih["objek"](SCREEN_WIDTH // 2, 600),
                        pesawat_dipilih["kelas"]
                    )
                elif event.key == pygame.K_ESCAPE:
                    _play(ui_sounds, "leave")
                    return None, None


# ======================================================================== #
#  MENU PILIHAN MEDAN PERANG                                                #
# ======================================================================== #
def menu_pilihan_medan(layar, font, nama_pemain, ui_sounds=None):
    """
    Layar pemilihan medan perang dengan preview live background.
    Return: "LAUT" | "HUTAN" | None (ESC)
    """
    clock    = pygame.time.Clock()
    font_hud = pygame.font.SysFont("Consolas", 16)
    font_med = pygame.font.SysFont("Arial", 20, bold=True)

    daftar_medan = [
        {
            "key"   : "SEA",
            "nama"  : "PACIFIC OCEAN",
            "desc"  : ["Open battlefield over the ocean.",
                    "High visibility, no terrain obstacles.",
                    "Dynamic weather: clear → storm"],
            "bg"    : Background(speed=2),
            "warna" : (50, 120, 200),
        },
        {
            "key"   : "DESERT",
            "nama"  : "GOLDEN DESERT",
            "desc"  : ["Arid battlefield under blazing sun.",
                    "Light sandstorms with flying dust.",
                    "Lighting shifts: "
                    "daytime -> sunset."],
            "bg"    : BackgroundPadangPasir(speed=2),
            "warna" : (215, 175, 100),
        },
    ]

    pilihan_sekarang = 0
    running          = True

    while running:
        clock.tick(30)

        # Preview background aktif
        bg_aktif = daftar_medan[pilihan_sekarang]["bg"]
        bg_aktif.update()
        bg_aktif.draw(layar)

        # Overlay gelap
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        layar.blit(overlay, (0, 0))

        # Border frame militer
        pygame.draw.rect(layar, HIJAU_ARMY,   (15, 15, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30), 2)
        pygame.draw.rect(layar, COKLAT_TANAH, (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 1)

        # Header
        teks_header = font.render(f"CHOOSE OPERATION AREA:", True, PUTIH)
        layar.blit(teks_header, (45, 40))
        pygame.draw.line(layar, COKLAT_TANAH, (45, 80), (SCREEN_WIDTH - 45, 80), 1)

        # Panel kiri: daftar medan
        panel_kiri_w = 260
        panel_kiri_x = 45

        for i, medan in enumerate(daftar_medan):
            is_selected = (i == pilihan_sekarang)
            y_item      = 110 + i * 90

            if is_selected:
                s_box = pygame.Surface((panel_kiri_w, 75), pygame.SRCALPHA)
                s_box.fill((*medan["warna"], 60))
                layar.blit(s_box, (panel_kiri_x, y_item - 5))
                pygame.draw.rect(layar, medan["warna"],
                                (panel_kiri_x, y_item - 5, panel_kiri_w, 75), 2)

            warna_teks  = EMAS_TAKTIK if is_selected else (160, 170, 150)
            prefix      = "> " if is_selected else "  "
            render_nama = font.render(f"{prefix}{medan['nama']}", True, warna_teks)
            layar.blit(render_nama, (panel_kiri_x + 10, y_item + 5))

            label = font_hud.render(
                f"[ZONA {i + 1}]  {'<- AKTIF' if is_selected else ''}",
                True, EMAS_TAKTIK if is_selected else (100, 110, 90)
            )
            layar.blit(label, (panel_kiri_x + 10, y_item + 38))

        # Panel kanan: deskripsi medan aktif
        desc_x = 50
        desc_y = 340
        desc_w = 400
        desc_h = 200

        s_desc = pygame.Surface((desc_w, desc_h), pygame.SRCALPHA)
        s_desc.fill((10, 15, 10, 180))
        layar.blit(s_desc, (desc_x, desc_y))
        pygame.draw.rect(layar, daftar_medan[pilihan_sekarang]["warna"],
                         (desc_x, desc_y, desc_w, desc_h), 2)

        # Dekorasi sudut
        pygame.draw.line(layar, EMAS_TAKTIK, (desc_x, desc_y),           (desc_x + 20, desc_y), 3)
        pygame.draw.line(layar, EMAS_TAKTIK, (desc_x, desc_y),           (desc_x, desc_y + 20), 3)
        pygame.draw.line(layar, EMAS_TAKTIK, (desc_x + desc_w, desc_y),  (desc_x + desc_w - 20, desc_y), 3)
        pygame.draw.line(layar, EMAS_TAKTIK, (desc_x + desc_w, desc_y),  (desc_x + desc_w, desc_y + 20), 3)

        render_judul = font_med.render(daftar_medan[pilihan_sekarang]["nama"], True, EMAS_TAKTIK)
        layar.blit(render_judul, (desc_x + 15, desc_y + 18))
        pygame.draw.line(layar, COKLAT_TANAH,
                         (desc_x + 15, desc_y + 50), (desc_x + desc_w - 15, desc_y + 50), 1)

        for j, baris in enumerate(daftar_medan[pilihan_sekarang]["desc"]):
            render_d = font_hud.render(f"- {baris}", True, (200, 210, 195))
            layar.blit(render_d, (desc_x + 15, desc_y + 65 + j * 28))

        render_prev = font_hud.render("", True, (80, 180, 80))
        layar.blit(render_prev, render_prev.get_rect(
            center=(desc_x + desc_w // 2, desc_y + desc_h - 18)
        ))

        # Footer
        x_awal = 45
        y_foot = SCREEN_HEIGHT - 50
        teks_esc = font_hud.render("[ESC] BACK", True, (200, 80, 80))
        layar.blit(teks_esc, (x_awal, y_foot))
        lebar_esc = teks_esc.get_width()
        teks_nav  = font_hud.render("  |  [UP/DOWN] NAVIGATION", True, HIJAU_LUMUT)
        layar.blit(teks_nav, (x_awal + lebar_esc, y_foot))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pilihan_sekarang = (pilihan_sekarang - 1) % len(daftar_medan)
                    _play(ui_sounds, "pilih")
                elif event.key == pygame.K_DOWN:
                    pilihan_sekarang = (pilihan_sekarang + 1) % len(daftar_medan)
                    _play(ui_sounds, "pilih")
                elif event.key == pygame.K_RETURN:
                    _play(ui_sounds, "oke")
                    return daftar_medan[pilihan_sekarang]["key"]
                elif event.key == pygame.K_ESCAPE:
                    _play(ui_sounds, "leave")
                    return None


# ======================================================================== #
#  LOADING SCREEN                                                           #
# ======================================================================== #
def loading_screen(layar, clock, nama_medan):
    """
    Loading screen animasi ~2.5 detik sebelum game dimulai.
    Progress bar dengan pesan bergaya militer.
    """
    font_besar = pygame.font.SysFont("Impact", 52)
    font_med   = pygame.font.SysFont("Consolas", 18)
    font_kecil = pygame.font.SysFont("Consolas", 14)

    label_medan = {
        "LAUT"  : "LAUTAN PASIFIK",
        "DESERT" : "PADANG PASIR EMAS",
    }.get(nama_medan, nama_medan)

    pesan_loading = [
        "Initializing weapon systems...",
        "Loading battlefield map...",
        "Calibrating tactical radar...",
        "Checking fuel & ammunition...",
        "Contacting command center...",
        "Systems ready. Awaiting takeoff clearance...",
        "MISSION STARTED. GOOD LUCK, PILOT!",
    ]

    total_durasi = 2500
    waktu_mulai  = pygame.time.get_ticks()
    bar_w_total  = 400
    bar_h        = 22
    bar_x        = SCREEN_WIDTH // 2 - bar_w_total // 2
    bar_y        = SCREEN_HEIGHT // 2 + 60

    grain = [
        (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
         random.randint(1, 3), random.randint(30, 80))
        for _ in range(120)
    ]

    while True:
        clock.tick(60)
        elapsed  = pygame.time.get_ticks() - waktu_mulai
        progress = min(elapsed / total_durasi, 1.0)

        # Background gelap bertekstur
        layar.fill((8, 12, 8))
        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(layar, (18, 25, 14), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(layar, (18, 25, 14), (0, y), (SCREEN_WIDTH, y), 1)

        for (gx, gy, gs, ga) in grain:
            s = pygame.Surface((gs, gs), pygame.SRCALPHA)
            s.fill((80, 120, 60, ga))
            layar.blit(s, (gx, gy))

        pygame.draw.rect(layar, HIJAU_ARMY,   (15, 15, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30), 2)
        pygame.draw.rect(layar, COKLAT_TANAH, (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 1)

        teks_loading = font_besar.render("LOADING MISI", True, PUTIH)
        layar.blit(teks_loading, teks_loading.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))

        teks_medan = font_med.render(f"ZONA OPERASI : {label_medan}", True, EMAS_TAKTIK)
        layar.blit(teks_medan, teks_medan.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30)))

        # Progress bar
        pygame.draw.rect(layar, (30, 40, 25), (bar_x - 2, bar_y - 2, bar_w_total + 4, bar_h + 4))
        pygame.draw.rect(layar, (50, 70, 40), (bar_x, bar_y, bar_w_total, bar_h))

        bar_w_isi = int(bar_w_total * progress)
        if bar_w_isi > 0:
            r = int(60 + 150 * progress)
            g = int(160 - 20 * progress)
            b = 40
            pygame.draw.rect(layar, (r, g, b), (bar_x, bar_y, bar_w_isi, bar_h))
            if bar_w_isi > 10:
                shimmer_x = bar_x + bar_w_isi - 8
                s_shim = pygame.Surface((8, bar_h), pygame.SRCALPHA)
                s_shim.fill((255, 255, 200, 100))
                layar.blit(s_shim, (shimmer_x, bar_y))

        pygame.draw.rect(layar, HIJAU_LUMUT, (bar_x - 2, bar_y - 2, bar_w_total + 4, bar_h + 4), 2)

        teks_pct = font_med.render(f"{int(progress * 100)}%", True, EMAS_TAKTIK)
        layar.blit(teks_pct, teks_pct.get_rect(center=(SCREEN_WIDTH // 2, bar_y + bar_h + 22)))

        idx_pesan   = min(int(progress * len(pesan_loading)), len(pesan_loading) - 1)
        teks_status = font_kecil.render(pesan_loading[idx_pesan], True, (140, 170, 120))
        layar.blit(teks_status, teks_status.get_rect(center=(SCREEN_WIDTH // 2, bar_y + bar_h + 50)))

        titik_count = (elapsed // 400) % 4
        teks_titik  = font_kecil.render("STAND BY" + "." * titik_count, True, (80, 130, 70))
        layar.blit(teks_titik, (SCREEN_WIDTH - 160, SCREEN_HEIGHT - 45))

        pygame.display.flip()

        if progress >= 1.0:
            pygame.time.wait(350)
            return


# ======================================================================== #
#  LAYAR GAME OVER                                                          #
# ======================================================================== #
def layar_game_over(layar, clock, font, font_besar,
                    nama_pemain, skor_akhir,
                    grup_ledakan, bg_langit,
                    jenis_pesawat, sound_hancur,
                    ui_sounds=None):
    simpan_skor_pemain(nama_pemain, jenis_pesawat, skor_akhir)

    if sound_hancur:
        sound_hancur.play()

    for _ in range(30):
        clock.tick(FPS)
        bg_langit.update()
        grup_ledakan.update()
        bg_langit.draw(layar)
        grup_ledakan.draw(layar)
        pygame.display.flip()

    over     = True
    font_hud = pygame.font.SysFont("Consolas", 16)

    while over:
        clock.tick(30)
        layar.fill((20, 12, 12))

        for x in range(0, SCREEN_WIDTH, 40):
            pygame.draw.line(layar, (38, 24, 24), (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.line(layar, (38, 24, 24), (0, y), (SCREEN_WIDTH, y), 1)
        pygame.draw.rect(layar, (120, 40, 40),  (15, 15, SCREEN_WIDTH - 30, SCREEN_HEIGHT - 30), 2)
        pygame.draw.rect(layar, COKLAT_TANAH,   (10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), 1)

        teks_go = font_besar.render("GAME OVER", True, (220, 50, 50))
        layar.blit(teks_go, teks_go.get_rect(center=(SCREEN_WIDTH // 2, 160)))

        teks_status = font_hud.render("OPERATION STATUS: DEFEAT (PILOT DOWN)", True, (160, 160, 160))
        layar.blit(teks_status, teks_status.get_rect(center=(SCREEN_WIDTH // 2, 215)))

        box_w, box_h = 340, 100
        box_x        = SCREEN_WIDTH // 2 - box_w // 2
        box_y        = 260
        pygame.draw.rect(layar, (30, 20, 20),  (box_x, box_y, box_w, box_h))
        pygame.draw.rect(layar, (150, 50, 50), (box_x, box_y, box_w, box_h), 1)

        teks_skor = font.render(f"FINAL SCORE: {nama_pemain}", True, PUTIH)
        layar.blit(teks_skor, teks_skor.get_rect(center=(SCREEN_WIDTH // 2, 290)))

        teks_angka_skor = font.render(f"{skor_akhir} PTS", True, EMAS_TAKTIK)
        layar.blit(teks_angka_skor, teks_angka_skor.get_rect(center=(SCREEN_WIDTH // 2, 325)))

        y_pos      = SCREEN_HEIGHT - 50
        x_kiri     = 45
        x_pembatas = 500
        x_kanan    = 330

        teks_q        = font_hud.render("[Q] MAIN MENU", True, (200, 80, 80))
        teks_pembatas = font_hud.render("|",              True, (100, 100, 100))
        teks_r        = font_hud.render("[R] PLAY AGAIN",  True, HIJAU_LUMUT)

        layar.blit(teks_q,        (x_kiri, y_pos))
        layar.blit(teks_pembatas, (x_pembatas, y_pos))
        layar.blit(teks_r,        (x_kanan, y_pos))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    _play(ui_sounds, "oke")
                    return True
                if event.key == pygame.K_q:
                    _play(ui_sounds, "leave")
                    return False