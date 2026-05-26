import streamlit as st
import plotly.express as px
from datetime import date
from model import Transaksi
from manajer_anggaran import AnggaranHarian
from konfigurasi import KATEGORI_PENGELUARAN

st.set_page_config(page_title="Pencatat Anggaran OOP", page_icon="💰", layout="wide")

if 'manajer' not in st.session_state:
    st.session_state.manajer = AnggaranHarian(anggaran_bulanan=5000000.0)

manajer = st.session_state.manajer

st.title("💰 Aplikasi Pengeluaran Harian Berbasis OOP")
st.markdown("Aplikasi pencatat keuangan interaktif dengan implementasi Enkapsulasi & Komposisi Python.")

st.sidebar.header("⚙️ Pengaturan Anggaran")
budget_input = st.sidebar.number_input(
    "Set Anggaran Bulanan (Rp):", 
    min_value=0.0, 
    value=manajer.anggaran_bulanan, 
    step=50000.0
)
manajer.anggaran_bulanan = budget_input

kolom_kiri, kolom_kanan = st.columns([1, 2])

with kolom_kiri:
    st.subheader("📝 Tambah Transaksi Baru")
    with st.form("form_transaksi", clear_on_submit=True):
        deskripsi = st.text_input("Deskripsi Pengeluaran:", placeholder="Misal: Nasi Goreng")
        jumlah = st.number_input("Jumlah Uang (Rp):", min_value=0.0, step=1000.0)
        kategori = st.selectbox("Kategori:", KATEGORI_PENGELUARAN)
        tanggal_pilih = st.date_input("Tanggal:", date.today())
        
        tombol_simpan = st.form_submit_button("Simpan Transaksi")
        
        if tombol_simpan:
            if deskripsi.strip() == "" or jumlah <= 0:
                st.error("Gagal: Deskripsi tidak boleh kosong & Jumlah harus lebih dari 0!")
            else:
                transaksi_baru = Transaksi(
                    deskripsi=deskripsi, 
                    jumlah=jumlah, 
                    kategori=kategori, 
                    tanggal=tanggal_pilih
                )
                if manajer.tambah_transaksi(transaksi_baru):
                    st.success(f"Berhasil mencatat: '{deskripsi}'")
                    st.rerun()
                else:
                    st.error("Gagal menyimpan ke database.")

df_transaksi = manajer.ambil_semua_transaksi_df()
hari_ini = date.today()

total_pengeluaran_bulan_ini = manajer.hitung_total_pengeluaran(bulan=hari_ini.month, tahun=hari_ini.year)
sisa_anggaran_bulan_ini = manajer.hitung_sisa_anggaran(bulan=hari_ini.month, tahun=hari_ini.year)

with kolom_kanan:
    st.subheader("📊 Ringkasan Finansial Bulan Ini")
    k1, k2, k3 = st.columns(3)
    k1.metric("Anggaran Bulanan", f"Rp {manajer.anggaran_bulanan:,.0f}")
    k2.metric("Total Pengeluaran", f"Rp {total_pengeluaran_bulan_ini:,.0f}")
    k3.metric("Sisa Anggaran", f"Rp {sisa_anggaran_bulan_ini:,.0f}", 
              delta=f"{sisa_anggaran_bulan_ini if sisa_anggaran_bulan_ini >= 0 else 0}", 
              delta_color="normal" if sisa_anggaran_bulan_ini >= 0 else "inverse")

    st.markdown("---")
    
    if not df_transaksi.empty:
        st.subheader("🍕 Proporsi Pengeluaran per Kategori")
        fig = px.pie(df_transaksi, values='jumlah', names='kategori', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Belum ada data pengeluaran untuk membuat grafik visualisasi.")

st.markdown("---")
st.subheader("📜 Riwayat Transaksi")

if not df_transaksi.empty:
    df_tampilan = df_transaksi.copy()
    df_tampilan.columns = ['ID', 'Deskripsi', 'Jumlah Pengeluaran (Rp)', 'Kategori', 'Tanggal']
    st.dataframe(df_tampilan, use_container_width=True)
    
    st.markdown("### ❌ Menu Hapus Transaksi")
    col_id, col_btn = st.columns([1, 3])
    
    with col_id:
        id_hapus = st.number_input("Masukkan ID Transaksi:", min_value=1, step=1, key="id_hapus")
    
    with col_btn:
        st.write("")
        st.write("") 
        tombol_hapus = st.button("Hapus Transaksi Terpilih", type="primary")
    
    if tombol_hapus:
        if id_hapus in df_transaksi['id'].values:
            st.session_state.id_akan_dihapus = id_hapus
        else:
            st.error(f"Transaksi dengan ID {id_hapus} tidak ditemukan di database!")

    if 'id_akan_dihapus' in st.session_state and st.session_state.id_akan_dihapus is not None:
        id_target = st.session_state.id_akan_dihapus
        st.warning(f"⚠️ Apakah Anda yakin ingin menghapus permanen Transaksi dengan ID {id_target}?")
        
        c1, c2 = st.columns([1, 10])
        with c1:
            konfirmasi = st.button("Ya, Hapus", key="confirm_yes")
        with c2:
            batal = st.button("Batal", key="confirm_no")
            
        if konfirmasi:
            if manajer.hapus_transaksi(id_target):
                st.success(f"Sukses: Transaksi ID {id_target} berhasil dihapus!")
                st.session_state.id_akan_dihapus = None
                
                if hasattr(st, 'cache_data'):
                    st.cache_data.clear()
                st.rerun()
            else:
                st.error("Gagal menghapus transaksi dari database.")
                
        if batal:
            st.session_state.id_akan_dihapus = None
            st.rerun()
else:
    st.warning("Database masih kosong. Silakan tambahkan transaksi pertama Anda di menu sebelah kiri!")