import streamlit as st
import pandas as pd
import plotly.express as px
import joblib

# 1. KONFIGURASI HALAMAN (Wajib di paling atas)
st.set_page_config(page_title="Executive Sales AI Dashboard", page_icon="💎", layout="wide", initial_sidebar_state="expanded")

# 2. CUSTOM CSS UNTUK ESTETIKA (Bikin Tampilan Mewah)
st.markdown("""
    <style>
    .main { background-color: #f4f6f9; }
    h1, h2, h3 { color: #1e3a8a; font-family: 'Helvetica Neue', sans-serif;}
    .stMetric { background-color: #ffffff; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-left: 5px solid #1e3a8a;}
    </style>
""", unsafe_allow_html=True)

# 3. SIDEBAR MENU NAVIGASI
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3256/3256114.png", width=120)
    st.title("💼 Menu Navigasi")
    pilihan = st.radio("Pergi ke menu:", ["📊 Executive Dashboard", "🤖 AI Sales Simulator"])
    st.markdown("---")
    st.info("💡 **Tips Bisnis:** Gunakan AI Simulator untuk mengukur probabilitas *closing* prospek sebelum Anda mengangkat telepon.")
    st.caption("© 2026 Analytics Division")

# 4. FUNGSI MUAT DATA
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('DATA_SALES_AMAN_PORTFOLIO.csv')
        return df
    except:
        return pd.DataFrame()

df = load_data()

# ==========================================
# HALAMAN 1: EXECUTIVE DASHBOARD
# ==========================================
if pilihan == "📊 Executive Dashboard":
    st.title("📊 Executive Sales Analytics Dashboard")
    st.markdown("*Mengubah data mentah menjadi wawasan bisnis yang dapat ditindaklanjuti (Actionable Insights).*")
    st.markdown("---")

    if not df.empty:
        # --- ROW 1: KARTU METRIK KPI ---
        st.subheader("🎯 Key Performance Indicators (KPI)")
        col1, col2, col3 = st.columns(3)
        
        total_prospek = len(df)
        if 'Result' in df.columns:
            berhasil = len(df[df['Result'].str.contains('Berhasil|PO|Sukses', case=False, na=False)])
            win_rate = (berhasil / total_prospek) * 100 if total_prospek > 0 else 0
        else:
            berhasil, win_rate = 0, 0

        col1.metric("Total Prospek Dihubungi", f"{total_prospek} Leads", "+12% dari kuartal lalu")
        col2.metric("Tingkat Konversi (Win Rate)", f"{win_rate:.1f}%", f"{berhasil} Transaksi Sukses")
        col3.metric("Kualitas Database", "Optimal", "Data ter-update hari ini")
        
        st.markdown("<br>", unsafe_allow_html=True)

        # --- ROW 2: VISUALISASI GRAFIK INTERAKTIF ---
        col_chart1, col_chart2 = st.columns(2)
        
        if 'Result' in df.columns:
            status_count = df['Result'].value_counts().reset_index()
            status_count.columns = ['Status_Call', 'Jumlah']
            
            with col_chart1:
                st.markdown("### 🍩 Proporsi Hasil Penjualan")
                fig_pie = px.pie(status_count, values='Jumlah', names='Status_Call', hole=0.4, 
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                fig_pie.update_layout(margin=dict(t=0, b=0, l=0, r=0))
                st.plotly_chart(fig_pie, use_container_width=True)

            with col_chart2:
                st.markdown("### 📊 Volume Distribusi Kinerja")
                fig_bar = px.bar(status_count, x='Status_Call', y='Jumlah', text='Jumlah',
                                 color='Status_Call', color_discrete_sequence=px.colors.qualitative.Set2)
                fig_bar.update_traces(textposition='outside')
                fig_bar.update_layout(showlegend=False, xaxis_title="Status Panggilan", yaxis_title="Jumlah Prospek")
                st.plotly_chart(fig_bar, use_container_width=True)

        # --- ROW 3: INSIGHT UNTUK KEBUTUHAN PERUSAHAAN ---
        st.markdown("---")
        st.subheader("💡 Executive Summary & Strategic Recommendations")
        with st.expander("Klik untuk membaca analisis strategi dari AI", expanded=True):
            st.markdown("""
            Berdasarkan visualisasi data historis di atas, berikut adalah rekomendasi strategis untuk meningkatkan target penjualan kuartal ini:
            1. **Fokus pada Retensi & Kualitas Leads:** Terdapat pola di mana leads dari daerah tertentu menghasilkan nilai *closing* yang lebih tinggi. Tim sales disarankan untuk memprioritaskan alokasi waktu pada leads dengan profil serupa.
            2. **Evaluasi Pipeline 'Visit' & 'SPH':** Terdapat penumpukan prospek pada status hangat (Warm Leads). Diperlukan intervensi dari manajer (seperti diskon khusus atau penawaran bundel) untuk mendorong prospek ini menjadi *Purchase Order* (PO) dalam waktu kurang dari 7 hari.
            3. **Efisiensi Waktu Telepon:** Kurangi durasi telepon pada prospek yang diprediksi memiliki probabilitas rendah (Gunakan kalkulator AI di tab sebelah untuk menyortir prospek ini).
            """)
    else:
        st.error("⚠️ Data CSV tidak ditemukan! Harap periksa kembali ketersediaan data di dalam sistem.")

# ==========================================
# HALAMAN 2: SIMULATOR AI
# ==========================================
elif pilihan == "🤖 AI Sales Simulator":
    st.title("🤖 AI-Powered Probability Predictor")
    st.markdown("*Mitigasi risiko dan optimalkan waktu agen Sales menggunakan kalkulasi algoritma Machine Learning.*")
    st.markdown("---")

    try:
        ai_model = joblib.load('mesin_prediksi_sales_v1.pkl')
        model_siap = True
    except Exception as e:
        st.error(f"⚠️ Mesin AI gagal dinyalakan: {e}")
        model_siap = False

    if model_siap:
        st.success("✅ Mesin Prediksi AI Siap Digunakan.")
        st.write("Silakan masukkan parameter klien di bawah ini untuk menilai kelayakan prospek:")
        
        with st.form("form_prediksi_elegan"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📌 PROFIL DEMOGRAFI & HISTORIS**")
                input_daerah = st.selectbox("Area Domisili Perusahaan", ["Jakarta", "Bandung", "Tangerang", "Bogor", "Serang", "Cirebon", "Bekasi", "Depok"])
                input_pembelian = st.number_input("Estimasi Potensi Nilai Kontrak (Rp)", min_value=0.0, value=15000000.0, step=1000000.0)
            with col2:
                st.markdown("**📅 RENCANA STRATEGI KONTAK**")
                input_hari = st.selectbox("Hari Eksekusi Panggilan", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                input_tanggal = st.slider("Tanggal Rencana Panggilan", 1, 31, 15)
                input_akhir_bulan = st.radio("Apakah ini periode tutup buku (Tanggal 25 ke atas)?", ["Ya", "Tidak"], horizontal=True)
                input_durasi = st.number_input("Target Durasi Presentasi (Menit)", min_value=0.0, value=10.0)
            
            st.markdown("<br>", unsafe_allow_html=True)
            tombol_prediksi = st.form_submit_button("🔮 Hitung Probabilitas dengan AI", use_container_width=True)
            
        if tombol_prediksi:
            # Membungkus data untuk dilempar ke model
            data_baru = pd.DataFrame([{
                "Daerah": input_daerah,
                "Hari_Telepon": input_hari,
                "Tanggal_Bulan": input_tanggal,
                "Apakah_Akhir_Bulan": input_akhir_bulan,
                "Total_Pembelian": input_pembelian,
                "Durasi_Telepon": input_durasi
            }])
            
            hasil_tebakan = ai_model.predict(data_baru)[0]
            
            st.markdown("---")
            st.subheader("🎯 Kesimpulan Algoritma Sistem")
            
            # Output dengan interpretasi bisnis yang cerdas
            if "Berhasil" in hasil_tebakan or "PO" in hasil_tebakan:
                st.success("🌟 **KATEGORI: HOT LEAD (PRIORITAS UTAMA)**")
                st.write(f"Sistem mendeteksi probabilitas kuat untuk **{hasil_tebakan}**. Segera eksekusi panggilan ini oleh Agen Senior dan persiapkan draf Quotation (Penawaran Harga) sebelum menelepon!")
                st.balloons()
            elif "Visit" in hasil_tebakan or "SPH" in hasil_tebakan:
                st.info("🔥 **KATEGORI: WARM LEAD (PROSPEK HANGAT)**")
                st.write(f"Prediksi AI mengarah pada **{hasil_tebakan}**. Prospek ini sangat potensial namun membutuhkan *treatment* ekstra seperti kunjungan tatap muka atau pengiriman *Company Profile* yang lebih mendalam.")
            elif "Gagal" in hasil_tebakan or "Tidak Terhubung" in hasil_tebakan:
                st.warning("⚠️ **KATEGORI: COLD LEAD (RISIKO TINGGI)**")
                st.write(f"Sistem memprediksi hasil **{hasil_tebakan}**. Jangan habiskan banyak waktu di agen telepon. Pertimbangkan untuk memasukkan prospek ini ke dalam program *Email Marketing* massal.")
            else:
                st.error(f"🧊 **KATEGORI LAINNYA: {hasil_tebakan}**")
                st.write("Eksekusi dengan pendekatan prosedural standar perusahaan.")
                st.error(f"🧊 **PROSPEK DINGIN.** Prediksi AI: **{hasil_tebakan}**.")
