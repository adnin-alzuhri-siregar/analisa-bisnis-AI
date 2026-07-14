from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# 1. Inisialisasi Aplikasi
app = FastAPI(title="Mesin Prediksi Sales AI")

# 2. Muat Model (Pastikan file .pkl Anda sudah di-upload ke Colab!)
try:
    ai_model = joblib.load('mesin_prediksi_sales_v1.pkl')
except:
    ai_model = None # Menghindari error crash jika file belum diupload

# 3. Satpam Format Data
class DataPelanggan(BaseModel):
    Daerah: str
    Hari_Telepon: str
    Tanggal_Bulan: int
    Apakah_Akhir_Bulan: str
    Total_Pembelian: float
    Durasi_Telepon: float

# 4. Rute Utama API
@app.post("/prediksi")
def tebak_hasil_sales(data: DataPelanggan):
    if ai_model is None:
        return {"error": "Model .pkl belum ditemukan di Colab. Harap upload file mesin_prediksi_sales_v1.pkl!"}
        
    df_input = pd.DataFrame([data.dict()])
    hasil_tebakan = ai_model.predict(df_input)
    
    return {
        "status": "Sukses",
        "prediksi_status_call": hasil_tebakan[0]
    }
