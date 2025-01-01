import streamlit as st

class StokObat:
    def __init__(self):
        self.stok_obat = {
            "Maag 🥴": [
                {"nama": "Promag", "stok": 10000, "harga": 150000},
                {"nama": "Polysilane", "stok": 12000, "harga": 200000},
                {"nama": "Mylanta", "stok": 15000, "harga": 180000},
            ],
            "Demam 🤒": [
                {"nama": "Paracetamol", "stok": 5000, "harga": 120000},
                {"nama": "Ibuprofen", "stok": 8000, "harga": 150000},
                {"nama": "Panadol", "stok": 6000, "harga": 170000},
            ],
            "Batuk 😷": [
                {"nama": "Hufagrip", "stok": 15000, "harga": 100000},
                {"nama": "Woods", "stok": 14000, "harga": 120000},
                {"nama": "Komix", "stok": 5000, "harga": 140000},
            ],
        }

    def tampilkan_stok(self, penyakit):
        st.write(f"**Daftar Obat untuk {penyakit}:**")
        for index, obat in enumerate(self.stok_obat[penyakit]):
            st.write(f"### {index + 1}. {obat['nama']}")
            st.write(f"- Harga: Rp {obat['harga']}")
            st.write(f"- Stok tersedia: {obat['stok']}")

            # Tampilkan status ketersediaan
            if obat['stok'] > 0:
                st.success("Obat tersedia✅.")
            else:
                st.error("Obat tidak tersedia❌.")

            # Input jumlah pembelian
            jumlah = st.number_input(f"Masukkan jumlah yang ingin dibeli untuk {obat['nama']}:", 
                                    min_value=0, 
                                    max_value=obat['stok'], 
                                    step=1, 
                                    key=f"{penyakit}_{index}")

            # Tombol kurangi stok
            if st.button(f"Kurangi Stok {obat['nama']}", key=f"btn_{penyakit}_{index}"):
                if jumlah > 0:
                    obat['stok'] -= jumlah
                    st.success(f"Stok {obat['nama']} berhasil dikurangi sebanyak {jumlah}. Sisa stok: {obat['stok']}.")
                else:
                    st.warning("Masukkan jumlah yang valid untuk pembelian.")

    def tampilkan_stok_keseluruhan(self):
        st.write("\n### Daftar Stok Obat Keseluruhan")
        st.table([{"Penyakit": penyakit, "Nama Obat": obat["nama"], "Stok": obat["stok"], "Harga (Rp)": obat["harga"]} 
                  for penyakit, daftar_obat in self.stok_obat.items() 
                  for obat in daftar_obat])

def main():
    st.title("Aplikasi Kasir Stok Obat💊")
    stok_obat = StokObat()

    # Input penyakit untuk menampilkan obat yang relevan
    penyakit = st.selectbox("Pilih penyakit:", ["Maag 🥴", "Demam 🤒", "Batuk 😷"])

    if penyakit:
        stok_obat.tampilkan_stok(penyakit)
        stok_obat.tampilkan_stok_keseluruhan()

if __name__ == "__main__":
    main()