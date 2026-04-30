# 📡 Telco Customer Churn Risk Dashboard

Business Decision Support Tool untuk membantu tim retention mengidentifikasi customer yang berisiko berhenti berlangganan.

---

## 🚀 Cara Menjalankan Lokal

### 1. Clone / Download project
```bash
git clone https://github.com/username/telco-churn-streamlit.git
cd telco-churn-streamlit
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Jalankan aplikasi
```bash
streamlit run app.py
```

Buka browser di `http://localhost:8501`

---

## ☁️ Deploy ke Streamlit Cloud

1. Push semua file ke GitHub repository
2. Buka [share.streamlit.io](https://share.streamlit.io)
3. Klik **New app** → pilih repo → set **Main file path** ke `app.py`
4. Klik **Deploy**

> ⚠️ Pastikan `best_model.pkl` ikut di-push ke GitHub (ukuran ~830KB, masih dalam batas)

---

## 📁 Struktur Folder

```
telco-churn-streamlit/
│── app.py
│── requirements.txt
│── best_model.pkl
│── xgboost_telco_churn_model.sav
│── data_telco_customer_churn_cleaned.csv
│── README.md
```

---

## 🧠 Model

| Atribut | Detail |
|---|---|
| Algoritma | XGBoost + SMOTE + RandomizedSearchCV |
| Target | Churn (Yes/No) |
| Metrik Utama | Recall ≥ 75% |
| File Model | `best_model.pkl` (sklearn Pipeline) |

---

## 📊 Fitur Input

| Fitur | Deskripsi |
|---|---|
| Dependents | Memiliki tanggungan keluarga |
| tenure | Lama berlangganan (bulan) |
| InternetService | Jenis layanan internet |
| OnlineSecurity | Menggunakan keamanan online |
| OnlineBackup | Menggunakan backup online |
| DeviceProtection | Menggunakan proteksi perangkat |
| TechSupport | Menggunakan tech support |
| Contract | Jenis kontrak |
| PaperlessBilling | Tagihan digital |
| MonthlyCharges | Tagihan bulanan |

---

## 🎯 Segmentasi Risiko

| Segmen | Probabilitas | Tindakan |
|---|---|---|
| 🔴 High Risk | ≥ 70% | Retention call segera + diskon khusus |
| 🟡 Medium Risk | 40–70% | Personalized offer + monitoring 1 bulan |
| 🟢 Low Risk | < 40% | Loyalty program + upselling ringan |
