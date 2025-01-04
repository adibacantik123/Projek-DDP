import streamlit as st
import base64
import pandas as pd

def get_base64_of_bin_file(file_path):
    with open(file_path, "rb") as file:
        data = file.read()
    return base64.b64encode(data).decode()

# Fungsi untuk menambahkan gambar latar belakang dari file lokal
def add_bg_from_local(file_path):
    base64_str = get_base64_of_bin_file(file_path)
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{base64_str}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Menambahkan latar belakang gambar
add_bg_from_local("bg2.jpg")

OBAT = {
    "Demam": {"Paracetamol": 120000, "Ibuprofen": 150000, "Panadol": 170000},
    "Batuk": {"Hufagrip": 100000, "Woods": 120000, "Komix": 140000},
    "Maag": {"Promag": 1500000, "Polysilane": 200000, "Mylanta": 180000},
}

# Inisialisasi state
if "pesanan" not in st.session_state:
    st.session_state.pesanan = {}

# Layout utama dengan sidebar
st.sidebar.title("Pengguna")
menu = st.sidebar.radio("Pilih Halaman:", ["Beranda", "Pemesanan", "Pembayaran"])

# 1. Halaman Beranda
if menu == "Beranda":
    st.title("Selamat Datang di E-Apotek!🏥")
    st.markdown("""
        Aplikasi E-Apotik mempermudah Anda dalam mencari dan memesan obat. 
        Navigasikan melalui menu di sebelah kiri untuk memilih kategori:
        - Pemesanan: Memilih obat berdasarkan kategori.
        - Pembayaran: Menyelesaikan pembayaran.
    """)

# 2. Halaman Pemesanan
elif menu == "Pemesanan":
    st.title("Pilih Obat Sesuai Kebutuhan Anda")
    
    # Memilih kategori obat
    # Pilih kategori penyakit
    kategori = st.selectbox("Pilih Kategori Penyakit:", ["", "Demam", "Batuk", "Maag"])

    if kategori:
    # Pilih obat berdasarkan kategori
     obat = st.multiselect("Pilih Obat:", list(OBAT[kategori].keys()))
    
    # Meminta alamat pengiriman hanya sekali
     alamat = st.text_area("Masukkan Alamat Pengiriman:", placeholder="Alamat lengkap Anda...")
    
     if obat:
        if alamat == "":  # Pastikan alamat diisi
            st.error("Alamat pengiriman harus diisi!")
        else:
            # Proses setiap obat yang dipilih
            for o in obat:
                jumlah = st.number_input(f"Jumlah untuk {o}:", min_value=1, step=1, key=f"jumlah_{o}")

                # Button untuk menambahkan obat ke keranjang
                if st.button(f"Tambahkan {o} ke Keranjang", key=f"tambah_{o}"):
                    if o in st.session_state.pesanan:
                        st.session_state.pesanan[o]["jumlah"] += jumlah
                    else:
                        st.session_state.pesanan[o] = {"jumlah": jumlah, "alamat": alamat}
                    st.success(f"{o} sebanyak {jumlah} telah ditambahkan ke pesanan. Alamat pengiriman: {alamat}")

# 3. Halaman Pembayaran
elif menu == "Pembayaran":
    st.title("Proses Pembayaran")
    if not st.session_state.pesanan:
        st.warning("Tidak ada item di pesanan. Silakan lakukan pemesanan terlebih dahulu.")
    else:
        total_harga = 0
        total_item = 0
        for obat, details in st.session_state.pesanan.items():
            jumlah = details["jumlah"]
            harga = [v for penyakit in OBAT.values() for k, v in penyakit.items() if k == obat][0]
            subtotal = jumlah * harga
            total_harga += subtotal
            total_item += jumlah
            st.write(f"- {obat} (x{jumlah}): Rp{subtotal:,}")
            st.write(f"Alamat pengiriman: {details['alamat']}")
        
        st.write(f"Total Harga: Rp{total_harga:,}")
        
        # Menambahkan pajak 22% jika pembelian lebih dari 10 item
        pajak_persen = 12  # Pajak 22% untuk operator
        pajak = 0
        if total_item > 0:  # Jika membeli lebih dari 10 item
            pajak = (pajak_persen / 100) * total_harga
            st.write(f"Pajak (12%): Rp{pajak:,}")
        
        total_setelah_pajak = total_harga + pajak

        st.write(f"Total setelah Pajak: Rp{total_setelah_pajak:,}")
        
        e_money = st.selectbox("Pilih Jenis E-Money:", ["", "OVO", "GoPay", "DANA"])
        nomor = st.number_input("Masukkan nomor {e_money} anda: ", min_value=0)
        
        # Input untuk memasukkan PIN
        pin = st.text_input("Masukkan PIN Anda:", type="password")
        
        # Setelah PIN dimasukkan, baru tampilkan input untuk pembayaran
        if pin and len(pin) >= 6:

            # Input untuk memasukkan nominal pembayaran
            jumlah_bayar = st.number_input("Masukkan jumlah pembayaran:", min_value=0)
            
            if st.button("Bayar"):
                if jumlah_bayar == total_setelah_pajak:
                    if not e_money:
                        st.error("Pilih jenis e-money terlebih dahulu.")
                    else:
                        alamat_pengiriman = ", ".join([details["alamat"] for details in st.session_state.pesanan.values()])
                        st.success(f"Pembayaran berhasil menggunakan {e_money}! Terima kasih telah menggunakan E-Apotik, semoga lekas sembuh. Pemesanan Anda akan segera dikirim ke alamat: {alamat_pengiriman}.")
                        st.session_state.pesanan.clear()
                elif jumlah_bayar < total_setelah_pajak:
                    st.error("Jumlah pembayaran kurang.")
                else:
                    st.warning("Nominal pembayaran melebihi total harga.")
        else:
            st.warning("Masukkan PIN terlebih dahulu (minimal 6 digit).")