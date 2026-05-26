from datetime import date, datetime

class Transaksi:
    def __init__(self, deskripsi: str, jumlah: float, kategori: str, tanggal=None, id_transaksi: int = None):
        self._id = id_transaksi
        self.deskripsi = deskripsi
        self.jumlah = jumlah
        self.kategori = kategori
        
        if tanggal is None:
            self.tanggal = date.today()
        elif isinstance(tanggal, str):
            self.tanggal = datetime.strptime(tanggal, "%Y-%m-%d").date()
        else:
            self.tanggal = tanggal

    @property
    def id(self) -> int | None:
        
        return self._id

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "deskripsi": self.deskripsi,
            "jumlah": self.jumlah,
            "kategori": self.kategori,
            "tanggal": self.tanggal.strftime("%Y-%m-%d") if isinstance(self.tanggal, date) else str(self.tanggal)
        }

    def __repr__(self) -> str:
        return f"Transaksi(ID={self._id}, Ket='{self.deskripsi}', Rp={self.jumlah}, Kat='{self.kategori}', Tgl={self.tanggal})"
    
# Kode uji bangh
if __name__ == "__main__":
    print("--- Memulai Tes Kelas Transaksi (model.py) ---")
    try:
        tes_transaksi = Transaksi(deskripsi="Beli Bakso", jumlah=15000.0, kategori="Makanan", id_transaksi=1)
        
        print(f"-> Berhasil membuat objek: {tes_transaksi}")
        print(f"-> Tes konversi ke Dictionary: {tes_transaksi.to_dict()}")
        print("-> TES BERHASIL: Model data Transaksi OOP berjalan sempurna!")
    except Exception as e:
        print(f"-> TES GAGAL: Terjadi kesalahan: {e}")