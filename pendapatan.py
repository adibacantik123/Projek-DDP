import streamlit as st

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
if "pendapatan_harian" not in st.session_state:
    st.session_state.pendapatan_harian = {
        "Senin, 11 Desember 2024": {"pendapatan": 500000, "obat": ["Paracetamol"]},
        "Selasa, 12 Desember 2024": {"pendapatan": 450000, "obat": ["Hufagrip", "Dexamethasone"]},
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
        submenu = st.sidebar.radio("Karyawan", ["Pendapatan Harian", "Tambah Pendapatan", "Hapus Pendapatan", "Riwayat Penghapusan"])
        
        if submenu == "Pendapatan Harian":
            st.title("📊 Pendapatan Harian")
            for hari, data in st.session_state.pendapatan_harian.items():
                st.markdown(f"- {hari}: Rp {data['pendapatan']:,} (Obat: {', '.join(data['obat'])})")
        
        elif submenu == "Tambah Pendapatan":
            st.title("➕ Tambah Pendapatan Baru")
            with st.form("form_tambah_pendapatan"):
                tanggal = st.text_input("Tanggal")
                pendapatan = st.number_input("Pendapatan", min_value=0)
                obat = st.multiselect("Obat", ["Paracetamol", "Dexamethasone", "Hufagrip"])
                submitted = st.form_submit_button("Simpan")
                if submitted and tanggal:
                    st.session_state.pendapatan_harian[tanggal] = {"pendapatan": pendapatan, "obat": obat}
                    st.success("Data berhasil ditambahkan!")
        
        elif submenu == "Hapus Pendapatan":
            st.title("🗑 Hapus Pendapatan")
            tanggal = st.selectbox("Pilih tanggal", list(st.session_state.pendapatan_harian.keys()))
            if st.button("Hapus"):
                if tanggal:
                    st.session_state.pendapatan_harian.pop(tanggal, None)
                    st.success("Data berhasil dihapus!")
        
        elif submenu == "Riwayat Penghapusan":
            st.title("📜 Riwayat Penghapusan")
            st.write(st.session_state.riwayat_penghapusan or "Belum ada data yang dihapus.")
        
        if st.sidebar.button("Logout 🚪"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()