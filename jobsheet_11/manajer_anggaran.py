import pandas as pd
from model import Transaksi
import database as db

class AnggaranHarian:
    def __init__(self, anggaran_bulanan: float = 0.0):
        db.setup_database_initial()
        self._anggaran_bulanan = anggaran_bulanan

    @property
    def anggaran_bulanan(self) -> float:
        return self._anggaran_bulanan

    @anggaran_bulanan.setter
    def anggaran_bulanan(self, nilai: float):
        if nilai >= 0:
            self._anggaran_bulanan = nilai

    def tambah_transaksi(self, transaksi: Transaksi) -> bool:
        query = """
        INSERT INTO transaksi (deskripsi, jumlah, kategori, tanggal)
        VALUES (?, ?, ?, ?);
        """
        params = (transaksi.deskripsi, transaksi.jumlah, transaksi.kategori, str(transaksi.tanggal))
        last_id = db.execute_query(query, params)
        return last_id is not None

    def hapus_transaksi(self, id_transaksi: int) -> bool:
        """Menghapus transaksi berdasarkan ID dari database."""
        query = "DELETE FROM transaksi WHERE id = ?;"
        result = db.execute_query(query, (id_transaksi,))
        return result is not None

    def ambil_semua_transaksi_df(self) -> pd.DataFrame:
        query = "SELECT id, deskripsi, jumlah, kategori, tanggal FROM transaksi ORDER BY tanggal DESC, id DESC;"
        df = db.get_dataframe(query)
        if not df.empty and 'tanggal' in df.columns:
            df['tanggal'] = pd.to_datetime(df['tanggal']).dt.date
        return df

    def hitung_total_pengeluaran(self, bulan: int = None, tahun: int = None) -> float:
        if bulan and tahun:
            query = "SELECT SUM(jumlah) FROM transaksi WHERE strftime('%m', tanggal) = ? AND strftime('%Y', tanggal) = ?;"
            str_bulan = f"{bulan:02d}"
            result = db.fetch_query(query, (str_bulan, str(tahun)), fetch_all=False)
        else:
            query = "SELECT SUM(jumlah) FROM transaksi;"
            result = db.fetch_query(query, fetch_all=False)
            
        if result and result[0] is not None:
            return float(result[0])
        return 0.0

    def hitung_sisa_anggaran(self, bulan: int, tahun: int) -> float:
        total_pengeluaran = self.hitung_total_pengeluaran(bulan, tahun)
        return self._anggaran_bulanan - total_pengeluaran