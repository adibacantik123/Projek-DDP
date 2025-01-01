import streamlit as st

def pengeluaran_page():
    st.title("Pengeluaran Apotek")
    st.write("Halaman ini digunakan untuk melacak pengeluaran apotek.")
    # Tambahkan logika lainnya di sini

# Data username dan password yang valid
VALID_CREDENTIALS = {
    "Zaidaan": "zaid123",
    "Adiba": "adib123",
    "Fahri": "fhri123",
    "Zahra": "zhra123"
}

# Fungsi untuk memeriksa username dan password
def authenticate(username, password):
    return VALID_CREDENTIALS.get(username) == password

# Mengatur session state untuk login dan data lainnya
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "pengeluaran_harian" not in st.session_state:
    st.session_state.pengeluaran_harian = {
        "Senin, 11 Desember 2024": {"pengeluaran": 500000, "obat": ["Paracetamol"]},
        "Selasa, 12 Desember 2024": {"pengeluaran": 450000, "obat": ["Hufagrip", "Dexamethasone"]},
    }
if "riwayat_penghapusan" not in st.session_state:
    st.session_state.riwayat_penghapusan = []

# Sidebar untuk navigasi
st.sidebar.title("💊 Apotek Online")
menu = st.sidebar.radio("Pilih Menu", ["Beranda", "Login Karyawan"])

# Halaman Beranda
if menu == "Beranda":
    st.title("💊 Apotek Online")
    st.markdown("### Selamat datang di Apotek Online!")

# Halaman Login Karyawan
elif menu == "Login Karyawan":
    if not st.session_state.logged_in:
        st.title("👤 Login Karyawan")
        username = st.text_input("👤 Username", placeholder="Masukkan username")
        password = st.text_input("🔒 Password", placeholder="Masukkan password", type="password")
        
        if st.button("Login 🔑"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"✅ Selamat datang, {username}!")
                st.rerun()
            else:
                st.error("❌ Username atau password salah, dilarang masuk!!!")
    else:
        st.sidebar.title(f"Hai, {st.session_state.username}")
        submenu = st.sidebar.radio("Karyawan", ["Pengeluaran Harian", "Tambah Pengeluaran", "Hapus Pengeluaran"])

        # Menu Pengeluaran Harian
        if submenu == "Pengeluaran Harian":
            st.title("📊 Pengeluaran Harian")
            for hari, data in st.session_state.pengeluaran_harian.items():
                st.markdown(f"- {hari}: Rp {data['pengeluaran']:,} (Obat: {', '.join(data['obat'])})")

        # Menu Tambah Pengeluaran
        elif submenu == "Tambah Pengeluaran":
            st.title("➕ Tambah Pengeluaran Baru")
            with st.form("form_tambah_pengeluaran"):
                tanggal = st.date_input("Tanggal")
                pengeluaran = st.number_input("Pengeluaran", min_value=0)
                obat = st.multiselect("Obat", ["Paracetamol", "Dexamethasone", "Hufagrip"])
                submitted = st.form_submit_button("Simpan")
                if submitted and tanggal:
                    st.session_state.pengeluaran_harian[str(tanggal)] = {"pengeluaran": pengeluaran, "obat": obat}
                    st.success("Data berhasil ditambahkan!")

        # Menu Hapus Pengeluaran
        elif submenu == "Hapus Pengeluaran":
            st.title("🗑️ Hapus Pengeluaran")
            
            # Memastikan tanggal yang dipilih ada dalam daftar pengeluaran_harian
            tanggal_hapus = st.selectbox("Pilih tanggal untuk dihapus", list(st.session_state.pengeluaran_harian.keys()), key="hapus_tanggal")

            # Memeriksa apakah tanggal_hapus dipilih dengan benar
            if st.button("Hapus"):
                if tanggal_hapus and tanggal_hapus in st.session_state.pengeluaran_harian:
                    data_hapus = st.session_state.pengeluaran_harian[tanggal_hapus]
                    del st.session_state.pengeluaran_harian[tanggal_hapus]
                    st.session_state.riwayat_penghapusan.append(f"Pengeluaran pada {tanggal_hapus} sebesar Rp {data_hapus['pengeluaran']:,} dengan obat {', '.join(data_hapus['obat'])} telah dihapus.")
                    st.success(f"Pengeluaran pada {tanggal_hapus} sebesar Rp {data_hapus['pengeluaran']:,} dengan obat {', '.join(data_hapus['obat'])} berhasil dihapus!")
                else:
                    st.error("❌ Tanggal tidak valid atau belum dipilih!")
            
            # Menampilkan Riwayat Penghapusan
            st.subheader("Riwayat Penghapusan")
            if st.session_state.riwayat_penghapusan:
                for riwayat in st.session_state.riwayat_penghapusan:
                    st.write(riwayat)
            else:
                st.write("Tidak ada data yang dihapus.")

        # Logout Button
        if st.sidebar.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()