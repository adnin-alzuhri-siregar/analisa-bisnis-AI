import streamlit as st
import pandas as pd
import plotly.express as px
import joblib
import numpy as np

# KONFIGURASI HALAMAN
st.set_page_config(page_title="Super App: Sales AI & Analytics", page_icon="🚀", layout="wide")
st.title("🚀 Super App: Sales Analytics & AI Predictor")
st.markdown("---")

# MEMBUAT DUA TAB UTAMA
tab_analisa, tab_prediksi = st.tabs(["📈 Analisa Historis", "🤖 Simulator Prediksi AI"])

# ==========================================
# TAB 1: ANALISA BISNIS
# ==========================================
with tab_analisa:
    @st.cache_data
    def load_data():
        try:
            # Membaca data aman yang sudah Anda buat sebelumnya
            df = pd.read_csv('DATA_SALES_AMAN_PORTFOLIO.csv')
            if 'Call Date' in df.columns:
                df['Call Date'] = pd.to_datetime(df['Call Date'])
            return df
        except:
            return pd.DataFrame()

    df = load_data()
    
    if not df.empty:
        st.info("💡 Grafik analisa historis Anda ditampilkan di sini.")
        if 'Result' in df.columns:
            status_count = df['Result'].value_counts().reset_index()
            status_count.columns = ['Status_Call', 'count']
            fig_bar = px.bar(status_count, x='Status_Call', y='count', title="Distribusi Hasil Panggilan (Data Portofolio)")
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("File CSV tidak ditemukan.")

# ==========================================
# TAB 2: SIMULATOR PREDIKSI AI
# ==========================================
with tab_prediksi:
    st.header("🤖 Kalkulator Probabilitas Sales")
    st.write("Masukkan data rencana panggilan Anda di bawah ini:")
    
    try:
        ai_model = joblib.load('mesin_prediksi_sales_v1.pkl')
        model_siap = True
    except Exception as e:
        st.error(f"⚠️ Error memuat model: {e}")
        model_siap = False

    if model_siap:
        with st.form("form_prediksi_sales"):
            col1, col2 = st.columns(2)
            with col1:
                input_daerah = st.selectbox("Daerah Prospek", ["Jakarta", "Bandung", "Tangerang", "Bogor", "Serang", "Cirebon", "Bekasi", "Depok"])
                input_hari = st.selectbox("Rencana Hari Panggilan", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
                input_tanggal = st.slider("Tanggal Berapa?", 1, 31, 15)
            with col2:
                input_akhir_bulan = st.radio("Apakah ini akhir bulan (Tanggal 25 ke atas)?", ["Ya", "Tidak"])
                input_pembelian = st.number_input("Total Pembelian Historis (Rp)", min_value=0.0, value=15000000.0, step=1000000.0)
                input_durasi = st.number_input("Rata-rata Durasi Telepon (Menit)", min_value=0.0, value=10.0)
            
            tombol_prediksi = st.form_submit_button("🚀 Minta Prediksi AI", use_container_width=True)
            
        if tombol_prediksi:
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
            st.subheader("🎯 Hasil Analisis AI")
            
            if "Berhasil" in hasil_tebakan or "PO" in hasil_tebakan:
                st.success(f"🔥 **POTENSI TINGGI!** Prediksi AI: **{hasil_tebakan}**")
                st.balloons()
            elif "Visit" in hasil_tebakan or "SPH" in hasil_tebakan:
                st.info(f"⏳ **PROSPEK HANGAT.** Prediksi AI: **{hasil_tebakan}**")
            elif "Gagal" in hasil_tebakan or "Tidak Terhubung" in hasil_tebakan:
                st.warning(f"⚠️ **RISIKO GAGAL.** Prediksi AI: **{hasil_tebakan}**")
            else:
                st.error(f"🧊 **PROSPEK DINGIN.** Prediksi AI: **{hasil_tebakan}**.")
