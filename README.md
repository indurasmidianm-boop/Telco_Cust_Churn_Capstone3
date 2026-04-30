# 📡 Telco Customer Churn Prediction

Capstone Project Module 3 — Purwadhika Digital Technology School
Machine Learning for Business

---

# 📌 Project Overview

Project ini bertujuan membangun model machine learning untuk memprediksi customer yang berisiko melakukan **churn** (berhenti berlangganan) pada perusahaan telekomunikasi.

Dengan adanya sistem prediksi churn, perusahaan dapat melakukan tindakan retensi lebih awal sebelum pelanggan benar-benar pergi.

Project ini mencakup:

* Business understanding
* Data preprocessing
* Feature engineering
* Handling imbalanced data
* Machine learning modeling
* Hyperparameter tuning
* Model interpretability
* Streamlit deployment dashboard

---

# 🎯 Business Problem

Customer churn merupakan salah satu masalah terbesar pada industri telekomunikasi karena:

* Biaya mendapatkan pelanggan baru 5–7× lebih mahal dibanding mempertahankan pelanggan lama
* Perusahaan sering terlambat mengetahui pelanggan akan churn
* Program retensi sering tidak tepat sasaran
* Kehilangan pelanggan berdampak langsung pada revenue perusahaan

Project ini mencoba menjawab pertanyaan:

> “Dari ribuan pelanggan yang ada, siapa yang perlu diprioritaskan untuk dihubungi sebelum terlambat?”

---

# 🎯 Project Goals

* Memprediksi customer churn dengan performa yang baik
* Mengidentifikasi pelanggan berisiko tinggi
* Memberikan business insight terkait faktor churn
* Membantu tim CRM & retention mengambil keputusan
* Menyediakan dashboard prediction berbasis Streamlit

---

# 📊 Dataset Information

Dataset: **Telco Customer Churn**

| Information     | Value |
| --------------- | ----- |
| Total Customers | 4,853 |
| Total Features  | 10    |
| Target Variable | Churn |
| Churn Rate      | 26.5% |

### Important Features

* tenure
* MonthlyCharges
* Contract
* InternetService
* TechSupport
* OnlineSecurity
* OnlineBackup
* DeviceProtection
* Dependents
* PaperlessBilling

---

# ⚙️ Data Preprocessing

Beberapa preprocessing yang dilakukan:

* Duplicate removal
* Encoding categorical features
* Feature scaling
* ColumnTransformer
* Pipeline integration
* Imbalanced handling using:

  * SMOTE
  * Random Over Sampling
  * Random Under Sampling
  * NearMiss

⚠️ Seluruh preprocessing dilakukan di dalam pipeline untuk menghindari data leakage.

---

# 🤖 Machine Learning Models

Model yang dibandingkan:

* Logistic Regression
* K-Nearest Neighbors
* Decision Tree
* Random Forest
* AdaBoost
* Gradient Boosting
* LightGBM
* XGBoost

---

# 🏆 Best Model

## XGBoost + SMOTE + RandomizedSearchCV

### Kenapa dipilih?

* Recall terbaik
* ROC AUC tinggi
* Tidak overfitting
* Support interpretability menggunakan SHAP

---

# 📈 Evaluation Metrics

Karena dataset bersifat imbalanced, metric utama yang digunakan adalah:

## Recall

Alasan:

* False Negative memiliki dampak bisnis terbesar
* Customer churn yang tidak terdeteksi dapat menyebabkan kehilangan revenue permanen

### Additional Metrics

* Precision
* F1 Score
* ROC AUC
* PR AUC

---

# 📌 Business Insights

Beberapa insight utama dari model:

### 1. Pelanggan baru memiliki risiko churn lebih tinggi

Pelanggan dengan tenure rendah cenderung belum memiliki loyalitas yang kuat.

### 2. Kontrak bulanan lebih mudah churn

Customer month-to-month memiliki fleksibilitas tinggi untuk pindah provider.

### 3. Monthly charges tinggi meningkatkan risiko churn

Pelanggan menjadi lebih sensitif terhadap harga dan promo kompetitor.

### 4. Pelanggan tanpa Tech Support lebih mudah churn

Kurangnya layanan tambahan membuat customer kurang terikat.

### 5. Fiber optic memiliki ekspektasi layanan lebih tinggi

Ketika ekspektasi tidak terpenuhi, pelanggan lebih mudah berpindah.

---

# 🚀 Streamlit Deployment

Project ini juga dilengkapi dengan dashboard Streamlit untuk prediksi churn secara real-time.

### Features:

* Input customer data
* Churn prediction
* Churn probability
* Risk segmentation
* Business recommendation

### Dashboard Preview

(Add screenshot here)

---

# 📂 Project Structure

```text
Telco_Cust_Churn_Capstone3/
│
├── notebook/
│   └── Telco_Customer_Churn_Capstone_FINALLL.ipynb
│
├── streamlit/
│   ├── app.py
│   ├── requirements.txt
│   ├── best_model.pkl
│   ├── xgboost_telco_churn_model.sav
│   └── data_telco_customer_churn_cleaned.csv
│
├── assets/
│   └── dashboard_preview.png
│
└── README.md
```

---

# 🖥️ How to Run Locally

## Clone Repository

```bash
git clone https://github.com/USERNAME/Telco_Cust_Churn_Capstone3.git
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Run Streamlit App

```bash
streamlit run streamlit/app.py
```

---

# ☁️ Streamlit Cloud Deployment

This project is deployed using:

* GitHub
* Streamlit Community Cloud

---

# 📌 Recommendations

## Business

* Jalankan model secara berkala untuk mendeteksi pelanggan berisiko
* Prioritaskan pelanggan baru dan kontrak bulanan
* Fokus pada customer dengan churn probability tinggi

## Model

* Threshold optimization
* Ensemble improvement
* Monitoring model drift

## Data

Tambahkan:

* Customer complaint history
* Usage behavior
* Net Promoter Score (NPS)

---

# 👤 Author

**Indurasmi Dian Mulyastuti**
Purwadhika Digital Technology School
Capstone Project Module 3 — Machine Learning for Business

# 🚀 Streamlit Deployment

This project is deployed using Streamlit Cloud.

## Live App
👉[ https://telco-cust-churn-capstone3.streamlit.app](https://telcocustchurncapstone3-hrppjwgxhmjvprlqk886at.streamlit.app/)
