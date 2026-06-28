import pygame
import sys
import random 
import os 

from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, PUTIH
from peluru import Peluru, PeluruSerong, Laser, LaserGanda, LaserSerong
from musuh import MusuhKroco, MusuhTangguh, MusuhElite  
from booster import Booster  
from background import Background, BackgroundPadangPasir
from menu_utama import MenuUtama 

from efek import EfekLedakan
from fase_game import menu_pilihan, menu_pilihan_medan, loading_screen, layar_game_over

# Inisialisasi Pygame & Audio Mixer
pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)

layar      = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Falcon Strike")
clock      = pygame.time.Clock()
font       = pygame.font.SysFont("Arial", 24)
font_besar = pygame.font.SysFont("Arial", 48, bold=True)

NAMA_PEMAIN_SEKARANG = "GUEST"

# ============================================================
# SISTEM AUDIO TERPUSAT
# ============================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def _load_sound(nama_file, volume=1.0):
    try:
        path = os.path.join(BASE_DIR, "sound", nama_file)
        snd  = pygame.mixer.Sound(path)
        snd.set_volume(volume)
        return snd
    except Exception:
        return None

sound_tembak = _load_sound("shoot.wav",   volume=0.4)
sound_laser  = _load_sound("laser.wav",   volume=0.5)
sound_hancur = _load_sound("explode.wav", volume=0.6)
sound_leave  = _load_sound("leave.wav",   volume=0.8)
sound_pilih  = _load_sound("pilih.wav",   volume=0.7)
sound_oke    = _load_sound("oke.wav",     volume=0.8)

ui_sounds = {
    "leave" : sound_leave,
    "pilih" : sound_pilih,
    "oke"   : sound_oke,
}

SPAWN_MUSUH = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_MUSUH, 1000)


def _buat_background(medan):
    """Factory: buat objek background sesuai kunci medan."""
    if medan == "DESERT":
        return BackgroundPadangPasir(speed=2)
    return Background(speed=2)   # Default = LAUT (SEA)


def jalankan_game(medan="LAUT"):
    bg_langit = _buat_background(medan)

    pemain, jenis_pesawat = menu_pilihan(layar, font, NAMA_PEMAIN_SEKARANG, ui_sounds)
    if pemain is None:
        return "KEMBALI_PESAWAT"

    medan_dipilih = menu_pilihan_medan(layar, font, NAMA_PEMAIN_SEKARANG, ui_sounds)
    if medan_dipilih is None:
        return "KEMBALI_MEDAN"

    loading_screen(layar, clock, medan_dipilih)

    bg_langit = _buat_background(medan_dipilih)

    daftar_peluru  = []
    grup_musuh     = pygame.sprite.Group()
    grup_booster   = pygame.sprite.Group()
    grup_ledakan   = pygame.sprite.Group()

    skor                 = 0
    tipe_tembakan        = "biasa"
    tingkat_speed        = 1
    jeda_spawn_sekarang  = 1000

    waktu_mulai = pygame.time.get_ticks()

    running = True
    while running:
        clock.tick(FPS)
        detik_berjalan = (pygame.time.get_ticks() - waktu_mulai) // 1000

        jeda_target = 1000
        if detik_berjalan >= 60: jeda_target = 400
        elif detik_berjalan >= 30: jeda_target = 700

        if jeda_target != jeda_spawn_sekarang:
            jeda_spawn_sekarang = jeda_target
            pygame.time.set_timer(SPAWN_MUSUH, jeda_spawn_sekarang)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == SPAWN_MUSUH:
                pilihan_musuh = random.choices(
                    [MusuhKroco, MusuhTangguh, MusuhElite],
                    weights=[65, 25, 10], k=1
                )[0]
                grup_musuh.add(pilihan_musuh())

        bg_langit.update()
        pemain.kendalikan()
        grup_booster.update()
        grup_ledakan.update()

        tombol = pygame.key.get_pressed()
        if tombol[pygame.K_SPACE]:
            waktu_sekarang = pygame.time.get_ticks()
            cooldown_aktif = pemain.cooldown_tembak // tingkat_speed
            if cooldown_aktif < 5: cooldown_aktif = 5

            if waktu_sekarang - pemain.last_shot > cooldown_aktif:
                if tipe_tembakan == "biasa":
                    daftar_peluru.append(Peluru(pemain.rect.centerx, pemain.rect.top))
                elif tipe_tembakan == "ganda":
                    daftar_peluru.append(Peluru(pemain.rect.left + 10, pemain.rect.top))
                    daftar_peluru.append(Peluru(pemain.rect.right - 10, pemain.rect.top))
                elif tipe_tembakan == "serong":
                    daftar_peluru.append(PeluruSerong(pemain.rect.centerx, pemain.rect.top))
                elif tipe_tembakan == "laser":
                    daftar_peluru.append(Laser(pemain.rect.centerx, pemain.rect.top))
                elif tipe_tembakan == "laser_ganda":
                    daftar_peluru.append(LaserGanda(pemain.rect.centerx, pemain.rect.top))
                elif tipe_tembakan == "laser_serong":
                    daftar_peluru.append(LaserSerong(pemain.rect.centerx, pemain.rect.top))

                if tipe_tembakan in ("laser", "laser_ganda", "laser_serong"):
                    if sound_laser:
                        pygame.mixer.set_num_channels(64)
                        sound_laser.play()
                elif sound_tembak:
                    pygame.mixer.set_num_channels(64)
                    sound_tembak.play()
                pemain.last_shot = waktu_sekarang

        for peluru in daftar_peluru[:]:
            peluru.update()
            if hasattr(peluru, 'sub_peluru'):
                for sub in peluru.sub_peluru[:]:
                    if sub.rect.bottom < 0 or sub.rect.right < 0 or sub.rect.left > SCREEN_WIDTH:
                        peluru.sub_peluru.remove(sub)
                if len(peluru.sub_peluru) == 0: daftar_peluru.remove(peluru)
            else:
                if peluru.rect.bottom < 0: daftar_peluru.remove(peluru)

        grup_musuh.update()

        # Collision musuh
        for peluru in daftar_peluru[:]:
            if hasattr(peluru, 'sub_peluru'):
                for sub in peluru.sub_peluru[:]:
                    tabrakan = pygame.sprite.spritecollide(sub, grup_musuh, False)
                    if tabrakan:
                        peluru.sub_peluru.remove(sub)
                        for musuh in tabrakan:
                            musuh.hp -= 1
                            if musuh.hp <= 0:
                                if sound_hancur: sound_hancur.play()
                                grup_ledakan.add(EfekLedakan(musuh.rect.centerx, musuh.rect.centery, ukuran_maks=35))
                                if random.random() < 0.50:
                                    pool_booster = ["speed"]
                                    if detik_berjalan >= 60: pool_booster.extend(["ganda", "serong", "laser"])
                                    elif detik_berjalan >= 50: pool_booster.extend(["ganda", "serong"])
                                    elif detik_berjalan >= 30: pool_booster.append("ganda")
                                    grup_booster.add(Booster(musuh.rect.centerx, musuh.rect.centery, random.choice(pool_booster)))
                                musuh.kill()
                                skor += musuh.skor_poin
                if len(peluru.sub_peluru) == 0: daftar_peluru.remove(peluru)
            else:
                tabrakan = pygame.sprite.spritecollide(peluru, grup_musuh, False)
                if tabrakan:
                    if peluru in daftar_peluru: daftar_peluru.remove(peluru)
                    for musuh in tabrakan:
                        musuh.hp -= 1
                        if musuh.hp <= 0:
                            if sound_hancur: sound_hancur.play()
                            grup_ledakan.add(EfekLedakan(musuh.rect.centerx, musuh.rect.centery, ukuran_maks=35))
                            if random.random() < 0.50:
                                pool_booster = ["speed"]
                                if detik_berjalan >= 60: pool_booster.extend(["ganda", "serong", "laser"])
                                elif detik_berjalan >= 50: pool_booster.extend(["ganda", "serong"])
                                elif detik_berjalan >= 30: pool_booster.append("ganda")
                                grup_booster.add(Booster(musuh.rect.centerx, musuh.rect.centery, random.choice(pool_booster)))
                            musuh.kill()
                            skor += musuh.skor_poin

        # Booster
        tabrakan_booster = pygame.sprite.spritecollide(pemain, grup_booster, True)
        for bst in tabrakan_booster:
            if bst.jenis == "speed":
                max_speed = 4 if jenis_pesawat == "PESAWAT_RAPTOR" else 8
                if tingkat_speed < max_speed: tingkat_speed *= 2
            elif bst.jenis == "laser":
                # Kombinasi khusus berdasarkan senjata aktif
                if tipe_tembakan in ("serong", "laser_serong"):
                    tipe_tembakan = "laser_serong"   # serong + laser = 4 laser
                elif tipe_tembakan in ("ganda", "laser_ganda"):
                    tipe_tembakan = "laser_ganda"    # ganda + laser = 2 laser sejajar
                else:
                    tipe_tembakan = "laser"          # biasa -> laser tunggal
            elif bst.jenis == "ganda":
                # Kalau sudah laser, langsung upgrade ke laser_ganda
                if tipe_tembakan in ("laser", "laser_ganda"):
                    tipe_tembakan = "laser_ganda"
                else:
                    level_senjata = {"biasa": 1, "ganda": 2, "serong": 3, "laser": 4, "laser_ganda": 5, "laser_serong": 6}
                    if level_senjata.get(bst.jenis, 1) >= level_senjata.get(tipe_tembakan, 1):
                        tipe_tembakan = bst.jenis
            elif bst.jenis == "serong":
                # Kalau sudah laser, langsung upgrade ke laser_serong
                if tipe_tembakan in ("laser", "laser_ganda", "laser_serong"):
                    tipe_tembakan = "laser_serong"
                else:
                    level_senjata = {"biasa": 1, "ganda": 2, "serong": 3, "laser": 4, "laser_ganda": 5, "laser_serong": 6}
                    if level_senjata.get(bst.jenis, 1) >= level_senjata.get(tipe_tembakan, 1):
                        tipe_tembakan = bst.jenis

        # Player kena musuh
        tabrakan_player = pygame.sprite.spritecollide(pemain, grup_musuh, True)
        if tabrakan_player:
            pemain.hp     -= 1
            tipe_tembakan  = "biasa"
            tingkat_speed  = 1
            grup_ledakan.add(EfekLedakan(pemain.rect.centerx, pemain.rect.centery, ukuran_maks=45))
            if sound_hancur: sound_hancur.play()

            if pemain.hp <= 0:
                grup_ledakan.add(EfekLedakan(pemain.rect.centerx, pemain.rect.centery, ukuran_maks=90))
                pygame.time.set_timer(SPAWN_MUSUH, 1000)

                mau_restart = layar_game_over(
                    layar, clock, font, font_besar,
                    NAMA_PEMAIN_SEKARANG, skor,
                    grup_ledakan, bg_langit,
                    jenis_pesawat, sound_hancur, ui_sounds
                )
                return "RESTART" if mau_restart else "MENU_UTAMA"

        # Draw
        bg_langit.draw(layar)
        for peluru in daftar_peluru: peluru.draw(layar)
        grup_booster.draw(layar)
        grup_musuh.draw(layar)
        grup_ledakan.draw(layar)
        if pemain.hp > 0: pemain.gambar_ke_layar(layar)

        teks_hp     = font.render(f"HP: {pemain.hp}/{pemain.max_hp}", True, PUTIH)
        teks_waktu  = font.render(f"TIME: {detik_berjalan}s", True, (200, 200, 200))
        teks_skor   = font.render(f"SKOR: {skor}", True, PUTIH)
        string_senjata = tipe_tembakan.upper().replace("_", " ")
        if tingkat_speed > 1: string_senjata += f" + HYPER {tingkat_speed}X"
        teks_booster = font.render(f"SENJATA: {string_senjata}", True, (0, 255, 255))

        layar.blit(teks_hp,     (10, 10))
        layar.blit(teks_waktu,  (SCREEN_WIDTH // 2 - 40, 10))
        layar.blit(teks_skor,   (SCREEN_WIDTH - 180, 10))
        layar.blit(teks_booster,(10, SCREEN_HEIGHT - 35))
        pygame.display.flip()


def main_app():
    global NAMA_PEMAIN_SEKARANG
    menu = MenuUtama(layar, ui_sounds)

    while True:
        pilihan_menu = menu.tampilkan()

        if pilihan_menu == "NEW GAME":
            sambil_input = True
            while sambil_input:
                nama_baru = menu.input_nama_pemain()
                if nama_baru:
                    NAMA_PEMAIN_SEKARANG = nama_baru

                    status_game = "RESTART"
                    while status_game == "RESTART":
                        status_game = jalankan_game()

                    # ESC di pilih pesawat: kembali ke input nama
                    if status_game == "KEMBALI_PESAWAT":
                        continue
                    # ESC di pilih medan: kembali ke input nama (atau bisa ke pilih pesawat)
                    elif status_game == "KEMBALI_MEDAN":
                        continue
                    elif status_game == "MENU_UTAMA":
                        sambil_input = False
                else:
                    sambil_input = False

        elif pilihan_menu == "LOAD GAME":
            sambil_load = True
            while sambil_load:
                nama_load = menu.layar_load_game()
                if nama_load:
                    NAMA_PEMAIN_SEKARANG = nama_load

                    status_game = "RESTART"
                    while status_game == "RESTART":
                        status_game = jalankan_game()

                    if status_game in ("KEMBALI_PESAWAT", "KEMBALI_MEDAN"):
                        continue
                    elif status_game == "MENU_UTAMA":
                        sambil_load = False
                else:
                    sambil_load = False

        elif pilihan_menu == "EXIT":
            break

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_app()