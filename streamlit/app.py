import streamlit as st
import pandas as pd
import numpy as np
import os

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Telco Churn Risk Dashboard",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
html, body, [class*="css"] { font-family: 'Segoe UI', sans-serif; }

.main-header {
    background: linear-gradient(135deg, #0f2942 0%, #1a4a7a 100%);
    padding: 2rem 2.5rem 1.5rem; border-radius: 16px;
    margin-bottom: 1.5rem; color: white;
}
.main-header h1 {
    font-size: 2rem; font-weight: 700; color: white !important;
    margin: 0 0 0.4rem 0; letter-spacing: -0.5px;
}
.main-header p { color: #a8c8f0; font-size: 1rem; margin: 0; }
.main-header .badge {
    display: inline-block; background: rgba(255,255,255,0.15);
    color: #e0f0ff; padding: 4px 12px; border-radius: 20px;
    font-size: 0.78rem; margin-bottom: 0.8rem;
    border: 1px solid rgba(255,255,255,0.2);
}
.metric-card {
    background: white; border-radius: 14px; padding: 1.4rem 1.6rem;
    border: 1px solid #e8eef4; box-shadow: 0 2px 12px rgba(0,0,0,0.06); height: 100%;
}
.metric-card .label {
    font-size: 0.78rem; font-weight: 600; color: #7a8fa6;
    text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 0.5rem;
}
.metric-card .value {
    font-size: 2rem; font-weight: 700; color: #0f2942;
    line-height: 1.1; margin-bottom: 0.3rem;
}
.metric-card .sub { font-size: 0.85rem; color: #5a7a99; }
.result-card-churn {
    background: linear-gradient(135deg, #fff0f0, #ffe0e0);
    border: 2px solid #ff4444; border-radius: 16px;
    padding: 1.8rem 2rem; text-align: center;
}
.result-card-safe {
    background: linear-gradient(135deg, #f0fff4, #e0ffe8);
    border: 2px solid #22cc66; border-radius: 16px;
    padding: 1.8rem 2rem; text-align: center;
}
.result-title { font-size: 1.6rem; font-weight: 700; margin-bottom: 0.3rem; }
.result-title.churn { color: #cc0000; }
.result-title.safe  { color: #008844; }
.result-desc { font-size: 0.92rem; color: #4a5a6a; margin-top: 0.5rem; }
.risk-badge {
    display: inline-block; padding: 0.5rem 1.4rem; border-radius: 30px;
    font-size: 1.1rem; font-weight: 700; letter-spacing: 0.05em;
}
.risk-high   { background: #ff4444; color: white; }
.risk-medium { background: #ff9900; color: white; }
.risk-low    { background: #22cc66; color: white; }
.prob-bar-wrap {
    background: #e8eef4; border-radius: 10px; height: 14px;
    margin: 0.6rem 0; overflow: hidden;
}
.prob-bar-fill { height: 100%; border-radius: 10px; }
.section-header {
    font-size: 1.05rem; font-weight: 700; color: #0f2942;
    padding: 0.5rem 0; margin: 1.2rem 0 0.8rem;
    border-bottom: 2px solid #e0e8f0;
}
.exec-box {
    background: #f4f8ff; border-left: 4px solid #2271b3;
    border-radius: 0 12px 12px 0; padding: 1.2rem 1.5rem; margin: 0.5rem 0;
}
.exec-box ul { margin: 0; padding-left: 1.2rem; }
.exec-box li { color: #1a3a5c; font-size: 0.95rem; margin-bottom: 0.4rem; line-height: 1.5; }
.rec-box { border-radius: 12px; padding: 1.2rem 1.5rem; margin-top: 0.5rem; }
.rec-box.high   { background: #fff5f5; border: 1px solid #ffcccc; }
.rec-box.medium { background: #fffbf0; border: 1px solid #ffd966; }
.rec-box.low    { background: #f0fff6; border: 1px solid #99eebb; }
.rec-box h4 { margin: 0 0 0.7rem 0; font-size: 0.95rem; font-weight: 700; }
.rec-box.high h4   { color: #cc0000; }
.rec-box.medium h4 { color: #996600; }
.rec-box.low h4    { color: #007733; }
.rec-box ul { margin: 0; padding-left: 1.2rem; }
.rec-box li { font-size: 0.9rem; margin-bottom: 0.35rem; color: #2a3a4a; line-height: 1.5; }
.guide-box {
    background: #f8faff; border-radius: 12px;
    padding: 1.2rem 1.5rem; border: 1px solid #d0e0f0;
}
.guide-box h4 { color: #1a4a7a; font-size: 0.95rem; margin: 0 0 0.8rem 0; }
.guide-item { display: flex; align-items: flex-start; gap: 0.7rem; margin-bottom: 0.6rem; }
.guide-dot { width: 10px; height: 10px; border-radius: 50%; margin-top: 5px; flex-shrink: 0; }
.guide-text { font-size: 0.88rem; color: #3a5a7a; line-height: 1.5; }
[data-testid="stSidebar"] { background: #f5f8fc; border-right: 1px solid #dde8f0; }
.custom-divider { border: none; border-top: 1px solid #e0e8f2; margin: 1.2rem 0; }
.empty-state { text-align: center; padding: 3rem 2rem; color: #7a9ab8; }
.empty-state h3 { color: #1a4a7a; font-size: 1.2rem; margin-bottom: 0.5rem; }
.empty-state p  { font-size: 0.9rem; color: #7a9ab8; max-width: 320px; margin: 0 auto; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# BUILD & CACHE MODEL — langsung dari CSV
# Tidak butuh file .pkl sama sekali
# ─────────────────────────────────────────────
@st.cache_resource(show_spinner="⏳ Menyiapkan model prediksi...")
def build_model():
    from sklearn.pipeline import Pipeline
    from sklearn.compose import ColumnTransformer
    from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
    from sklearn.impute import SimpleImputer
    from imblearn.over_sampling import SMOTE
    from xgboost import XGBClassifier

    CSV = "data_telco_customer_churn_cleaned.csv"
    if not os.path.exists(CSV):
        return None, "CSV tidak ditemukan"

    df = pd.read_csv(CSV)
    X  = df.drop(columns=["Churn"])
    y  = df["Churn"].map({"Yes": 1, "No": 0}).astype(int)

    binary_feats  = ["Dependents", "PaperlessBilling"]
    nominal_feats = ["OnlineSecurity", "OnlineBackup", "InternetService",
                     "DeviceProtection", "TechSupport", "Contract"]
    num_feats     = ["tenure", "MonthlyCharges"]

    binary_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("enc", OrdinalEncoder(
            categories=[["No","Yes"], ["No","Yes"]],
            handle_unknown="use_encoded_value", unknown_value=-1
        )),
    ])
    nominal_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="most_frequent")),
        ("enc", OneHotEncoder(drop="first", handle_unknown="ignore")),
    ])
    num_pipe = Pipeline([
        ("imp", SimpleImputer(strategy="median")),
        ("sc",  StandardScaler()),
    ])

    preprocessor = ColumnTransformer([
        ("bin", binary_pipe,  binary_feats),
        ("nom", nominal_pipe, nominal_feats),
        ("num", num_pipe,     num_feats),
    ], remainder="drop")

    # Preprocess → SMOTE → XGBoost
    X_prep = preprocessor.fit_transform(X)
    sm = SMOTE(random_state=42)
    X_res, y_res = sm.fit_resample(X_prep, y)

    clf = XGBClassifier(
        n_estimators=200, max_depth=5, learning_rate=0.1,
        subsample=0.8, colsample_bytree=0.8,
        random_state=42, n_jobs=-1,
    )
    clf.fit(X_res, y_res)

    # Bungkus dalam Pipeline lengkap untuk inference
    final_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("classifier",   clf),
    ])
    return final_pipeline, "ok"


model, status = build_model()


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
FEATURE_COLS = [
    "Dependents", "tenure", "OnlineSecurity", "OnlineBackup",
    "InternetService", "DeviceProtection", "TechSupport",
    "Contract", "PaperlessBilling", "MonthlyCharges",
]

def predict(input_df):
    pred  = model.predict(input_df)[0]
    proba = model.predict_proba(input_df)[0][1]
    return int(pred), float(proba)

def get_risk_segment(proba):
    if proba >= 0.70:  return "High Risk",   "high"
    if proba >= 0.40:  return "Medium Risk", "medium"
    return "Low Risk", "low"

def prob_bar_html(proba, color):
    pct = round(proba * 100, 1)
    return f"""
    <div class="prob-bar-wrap">
      <div class="prob-bar-fill" style="width:{pct}%; background:{color};"></div>
    </div>"""


# ─────────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
  <div class="badge">📡 Business Decision Support Tool</div>
  <h1>Telco Customer Churn Risk Dashboard</h1>
  <p>Identifikasi customer yang berisiko berhenti berlangganan lebih awal —
     bantu tim retention mengambil tindakan yang tepat sebelum terlambat.</p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error(
        "❌ File `data_telco_customer_churn_cleaned.csv` tidak ditemukan. "
        "Pastikan file CSV ada di folder yang sama dengan app.py.",
        icon="🚨"
    )
    st.stop()
else:
    st.success("✅ Model siap — dibangun langsung dari data CSV", icon="🤖")


# ─────────────────────────────────────────────
# SIDEBAR — INPUT
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔍 Input Data Customer")
    st.markdown("Isi profil customer, lalu klik tombol analisis.")

    st.markdown("**👤 Profil Customer**")
    dependents = st.selectbox(
        "Memiliki Tanggungan Keluarga?",
        ["No","Yes"], format_func=lambda x: "Tidak" if x=="No" else "Ya"
    )
    tenure = st.slider("Lama Berlangganan (bulan)", 0, 72, 12)

    st.markdown("---")
    st.markdown("**🌐 Layanan yang Digunakan**")
    internet_service = st.selectbox(
        "Jenis Layanan Internet",
        ["DSL","Fiber optic","No"],
        format_func=lambda x: {"DSL":"DSL","Fiber optic":"Fiber Optik","No":"Tidak Ada"}[x]
    )
    online_security = st.selectbox(
        "Menggunakan Keamanan Online?",
        ["No","Yes","No internet service"],
        format_func=lambda x: {"No":"Tidak","Yes":"Ya","No internet service":"Tidak Ada Internet"}[x]
    )
    online_backup = st.selectbox(
        "Menggunakan Backup Online?",
        ["No","Yes","No internet service"],
        format_func=lambda x: {"No":"Tidak","Yes":"Ya","No internet service":"Tidak Ada Internet"}[x]
    )
    device_protection = st.selectbox(
        "Menggunakan Proteksi Perangkat?",
        ["No","Yes","No internet service"],
        format_func=lambda x: {"No":"Tidak","Yes":"Ya","No internet service":"Tidak Ada Internet"}[x]
    )
    tech_support = st.selectbox(
        "Menggunakan Tech Support?",
        ["No","Yes","No internet service"],
        format_func=lambda x: {"No":"Tidak","Yes":"Ya","No internet service":"Tidak Ada Internet"}[x]
    )

    st.markdown("---")
    st.markdown("**💳 Kontrak & Tagihan**")
    contract = st.selectbox(
        "Jenis Kontrak",
        ["Month-to-month","One year","Two year"],
        format_func=lambda x: {
            "Month-to-month":"Bulanan","One year":"1 Tahun","Two year":"2 Tahun"
        }[x]
    )
    paperless_billing = st.selectbox(
        "Tagihan Digital?",
        ["No","Yes"], format_func=lambda x: "Tidak" if x=="No" else "Ya"
    )
    monthly_charges = st.number_input(
        "Tagihan Bulanan (USD)", min_value=0.0, max_value=200.0, value=65.0, step=0.5
    )

    st.markdown("---")
    analyze_btn = st.button("🔎 Analyze Customer Risk", type="primary", use_container_width=True)


# ─────────────────────────────────────────────
# MAIN DASHBOARD
# ─────────────────────────────────────────────
if not analyze_btn:
    st.markdown("""
    <div class="empty-state">
      <div style="font-size:3rem; margin-bottom:1rem;">📋</div>
      <h3>Belum Ada Analisis</h3>
      <p>Isi data customer di sidebar kiri, lalu klik <strong>Analyze Customer Risk</strong>.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📖 Cara Membaca Hasil Analisis</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""<div class="guide-box"><h4>📊 Probabilitas Churn</h4>
        <div class="guide-item"><div class="guide-dot" style="background:#2271b3;"></div>
        <div class="guide-text">Persentase peluang customer akan berhenti berlangganan dalam waktu dekat.</div></div>
        <div class="guide-item"><div class="guide-dot" style="background:#2271b3;"></div>
        <div class="guide-text">Semakin tinggi angkanya, semakin besar kemungkinan customer pergi.</div></div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="guide-box"><h4>🎯 Segmentasi Risiko</h4>
        <div class="guide-item"><div class="guide-dot" style="background:#ff4444;"></div>
        <div class="guide-text"><strong>High Risk (≥70%)</strong> — Perlu tindakan segera.</div></div>
        <div class="guide-item"><div class="guide-dot" style="background:#ff9900;"></div>
        <div class="guide-text"><strong>Medium Risk (40–70%)</strong> — Perlu dipantau.</div></div>
        <div class="guide-item"><div class="guide-dot" style="background:#22cc66;"></div>
        <div class="guide-text"><strong>Low Risk (&lt;40%)</strong> — Relatif aman.</div></div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown("""<div class="guide-box"><h4>⚙️ Cara Kerja Model</h4>
        <div class="guide-item"><div class="guide-dot" style="background:#0f2942;"></div>
        <div class="guide-text">Model dilatih dengan algoritma <strong>XGBoost + SMOTE</strong> dari data historis pelanggan.</div></div>
        <div class="guide-item"><div class="guide-dot" style="background:#0f2942;"></div>
        <div class="guide-text">Faktor terpenting: tenure, jenis kontrak, tagihan bulanan, internet, dan layanan tambahan.</div></div>
        </div>""", unsafe_allow_html=True)

else:
    # ── Build input DataFrame ──
    input_df = pd.DataFrame([{
        "Dependents":       dependents,
        "tenure":           tenure,
        "OnlineSecurity":   online_security,
        "OnlineBackup":     online_backup,
        "InternetService":  internet_service,
        "DeviceProtection": device_protection,
        "TechSupport":      tech_support,
        "Contract":         contract,
        "PaperlessBilling": paperless_billing,
        "MonthlyCharges":   float(monthly_charges),
    }])[FEATURE_COLS]

    # ── Predict ──
    try:
        pred_label, churn_proba = predict(input_df)
        risk_label, risk_class  = get_risk_segment(churn_proba)
        churn_pct = round(churn_proba * 100, 1)
    except Exception as e:
        st.error(f"❌ Prediksi gagal: {e}", icon="🚨")
        st.stop()

    risk_colors = {"high": "#ff4444", "medium": "#ff9900", "low": "#22cc66"}
    bar_color   = risk_colors[risk_class]

    # ── ROW 1 — 4 Metric Cards ──
    st.markdown('<div class="section-header">📊 Ringkasan Hasil Analisis</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        if pred_label == 1:
            st.markdown("""<div class="metric-card" style="border-top:4px solid #ff4444;">
              <div class="label">Status Prediksi</div>
              <div class="value" style="color:#cc0000;font-size:1.4rem;">⚠️ Churn</div>
              <div class="sub">Customer berisiko pergi</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="metric-card" style="border-top:4px solid #22cc66;">
              <div class="label">Status Prediksi</div>
              <div class="value" style="color:#008844;font-size:1.4rem;">✅ Aman</div>
              <div class="sub">Customer relatif loyal</div></div>""", unsafe_allow_html=True)

    with c2:
        st.markdown(f"""<div class="metric-card" style="border-top:4px solid {bar_color};">
          <div class="label">Probabilitas Churn</div>
          <div class="value" style="color:{bar_color};">{churn_pct}%</div>
          {prob_bar_html(churn_proba, bar_color)}</div>""", unsafe_allow_html=True)

    with c3:
        sub_text = {"high":"Tindakan segera","medium":"Pantau & beri penawaran","low":"Pertahankan engagement"}[risk_class]
        st.markdown(f"""<div class="metric-card" style="border-top:4px solid {bar_color};">
          <div class="label">Segmen Risiko</div>
          <div style="margin-top:0.5rem;"><span class="risk-badge risk-{risk_class}">{risk_label}</span></div>
          <div class="sub" style="margin-top:0.6rem;">{sub_text}</div></div>""", unsafe_allow_html=True)

    with c4:
        tenure_label = "Baru (<1 thn)" if tenure < 12 else "Sedang (1–3 thn)" if tenure < 36 else "Loyal (>3 thn)"
        st.markdown(f"""<div class="metric-card" style="border-top:4px solid #2271b3;">
          <div class="label">Lama Berlangganan</div>
          <div class="value" style="color:#0f2942;">{tenure}</div>
          <div class="sub">Bulan · {tenure_label}</div></div>""", unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── ROW 2 — Prediction Card + Probability ──
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown('<div class="section-header">🎯 Hasil Prediksi</div>', unsafe_allow_html=True)
        if pred_label == 1:
            st.markdown(f"""<div class="result-card-churn">
              <div style="font-size:3rem;margin-bottom:0.5rem;">⚠️</div>
              <div class="result-title churn">Customer Berisiko Churn</div>
              <div style="margin:0.8rem 0;"><span class="risk-badge risk-{risk_class}">{risk_label}</span></div>
              <div class="result-desc">Model memprediksi peluang churn <strong>{churn_pct}%</strong>.
              Segera lakukan tindakan pencegahan.</div></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""<div class="result-card-safe">
              <div style="font-size:3rem;margin-bottom:0.5rem;">✅</div>
              <div class="result-title safe">Customer Relatif Aman</div>
              <div style="margin:0.8rem 0;"><span class="risk-badge risk-{risk_class}">{risk_label}</span></div>
              <div class="result-desc">Risiko churn <strong>{churn_pct}%</strong>.
              Pertahankan kualitas layanan dan lakukan upselling ringan.</div></div>""", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="section-header">📈 Detail Probabilitas</div>', unsafe_allow_html=True)
        safe_pct = round(100 - churn_pct, 1)
        interp = (
            "Probabilitas churn sangat tinggi. Butuh intervensi segera dari tim retention." if churn_pct >= 70 else
            "Probabilitas churn level waspada. Pantau dan berikan penawaran personal." if churn_pct >= 40 else
            "Probabilitas churn rendah. Fokus pada program loyalitas dan upselling."
        )
        st.markdown(f"""<div class="metric-card">
          <div style="margin-bottom:1rem;">
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
              <span style="font-size:0.88rem;font-weight:600;color:#cc0000;">⚠️ Kemungkinan Churn</span>
              <span style="font-size:0.88rem;font-weight:700;color:#cc0000;">{churn_pct}%</span>
            </div>{prob_bar_html(churn_proba,"#ff4444")}</div>
          <div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
              <span style="font-size:0.88rem;font-weight:600;color:#008844;">✅ Kemungkinan Tetap</span>
              <span style="font-size:0.88rem;font-weight:700;color:#008844;">{safe_pct}%</span>
            </div>{prob_bar_html(1-churn_proba,"#22cc66")}</div>
          <hr class="custom-divider">
          <div style="font-size:0.88rem;color:#4a6a8a;line-height:1.6;">
            <strong>Interpretasi:</strong><br>{interp}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── ROW 3 — Executive Summary + Rekomendasi ──
    col_exec, col_action = st.columns(2)

    with col_exec:
        st.markdown('<div class="section-header">📋 Executive Summary</div>', unsafe_allow_html=True)
        contract_lbl = {"Month-to-month":"kontrak bulanan","One year":"kontrak 1 tahun","Two year":"kontrak 2 tahun"}[contract]
        internet_lbl = {"DSL":"layanan DSL","Fiber optic":"layanan Fiber Optik","No":"tanpa layanan internet"}[internet_service]
        addons = [s for s, v in [("Online Security",online_security),("Tech Support",tech_support),
                                  ("Online Backup",online_backup),("Device Protection",device_protection)] if v == "Yes"]
        addon_text = ", ".join(addons) if addons else "tidak ada layanan tambahan"

        b1 = f"Customer menggunakan {internet_lbl} dengan {contract_lbl} dan tagihan bulanan <strong>USD {monthly_charges:,.2f}</strong>."
        b2 = f"Risiko churn level <strong>{risk_label}</strong> — probabilitas <strong>{churn_pct}%</strong> — {'perlu tindakan segera' if risk_class=='high' else 'perlu dipantau' if risk_class=='medium' else 'relatif aman'}."
        b3 = ("Disarankan retention call dan penawaran kontrak jangka panjang segera." if risk_class=="high" else
              "Disarankan personalized offer dan monitoring 1 bulan ke depan." if risk_class=="medium" else
              "Disarankan program loyalitas dan upselling layanan tambahan secara ringan.")
        st.markdown(f"""<div class="exec-box"><ul>
          <li>{b1}</li><li>{b2}</li><li>{b3}</li>
        </ul></div>""", unsafe_allow_html=True)

        st.markdown('<div style="margin-top:1rem;"><div class="section-header">👤 Profil Layanan Customer</div></div>', unsafe_allow_html=True)
        for k, v in {
            "Lama Berlangganan": f"{tenure} bulan",
            "Jenis Internet": internet_lbl,
            "Jenis Kontrak": contract_lbl,
            "Tagihan Bulanan": f"USD {monthly_charges:,.2f}",
            "Tagihan Digital": "Ya" if paperless_billing=="Yes" else "Tidak",
            "Layanan Tambahan": addon_text,
        }.items():
            st.markdown(f"""<div style="display:flex;justify-content:space-between;padding:0.4rem 0;
              border-bottom:1px solid #f0f4f8;font-size:0.88rem;">
              <span style="color:#5a7a99;font-weight:600;">{k}</span>
              <span style="color:#1a3a5c;font-weight:500;">{v}</span></div>""", unsafe_allow_html=True)

    with col_action:
        st.markdown('<div class="section-header">💼 Rekomendasi Action Bisnis</div>', unsafe_allow_html=True)
        if risk_class == "high":
            st.markdown("""<div class="rec-box high">
              <h4>🚨 High Risk — Tindakan Segera (1–3 Hari)</h4><ul>
              <li>📞 Hubungi customer via telepon atau WhatsApp dalam waktu dekat</li>
              <li>🎁 Berikan <strong>retention offer eksklusif</strong>: diskon 20–30% atau free upgrade layanan</li>
              <li>📝 Tawarkan <strong>kontrak jangka panjang (1–2 tahun)</strong> dengan harga spesial</li>
              <li>🔍 Review complaint history — cek keluhan yang belum terselesaikan</li>
              <li>👥 Eskalasikan ke Customer Success Manager untuk penanganan personal</li>
              </ul></div>""", unsafe_allow_html=True)
        elif risk_class == "medium":
            st.markdown("""<div class="rec-box medium">
              <h4>⚠️ Medium Risk — Pantau & Beri Penawaran (1–2 Minggu)</h4><ul>
              <li>📧 Kirimkan <strong>email/SMS personalized</strong> dengan penawaran relevan</li>
              <li>📊 Monitor penggunaan layanan selama 30 hari ke depan</li>
              <li>💡 Edukasi benefit layanan tambahan yang belum digunakan</li>
              <li>📦 Tawarkan <strong>paket bundling</strong> yang lebih sesuai kebutuhan</li>
              <li>🔄 Ajukan opsi upgrade kontrak dari bulanan ke tahunan</li>
              </ul></div>""", unsafe_allow_html=True)
        else:
            st.markdown("""<div class="rec-box low">
              <h4>✅ Low Risk — Pertahankan & Kembangkan</h4><ul>
              <li>🌟 Daftarkan ke <strong>program loyalitas</strong> atau VIP customer club</li>
              <li>📈 Lakukan <strong>upselling</strong> layanan premium secara ringan</li>
              <li>🎂 Kirimkan ucapan anniversary berlangganan dengan reward kecil</li>
              <li>💬 Minta <strong>testimoni atau referral</strong></li>
              <li>📋 Lakukan satisfaction survey untuk menjaga kepuasan jangka panjang</li>
              </ul></div>""", unsafe_allow_html=True)

    st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

    # ── ROW 4 — Guide ──
    st.markdown('<div class="section-header">📖 Cara Membaca Hasil Ini</div>', unsafe_allow_html=True)
    g1, g2, g3 = st.columns(3)
    with g1:
        st.markdown("""<div class="guide-box"><h4>📊 Apa itu Probabilitas Churn?</h4>
        <div class="guide-item"><div class="guide-dot" style="background:#2271b3;"></div>
        <div class="guide-text">Persentase peluang customer akan berhenti berlangganan.</div></div>
        <div class="guide-item"><div class="guide-dot" style="background:#2271b3;"></div>
        <div class="guide-text">75% artinya dari 100 customer serupa, sekitar 75 diprediksi akan pergi.</div></div>
        </div>""", unsafe_allow_html=True)
    with g2:
        st.markdown("""<div class="guide-box"><h4>🎯 Apa itu Segmen Risiko?</h4>
        <div class="guide-item"><div class="guide-dot" style="background:#ff4444;"></div>
        <div class="guide-text"><strong>High Risk (≥70%)</strong>: Butuh intervensi segera.</div></div>
        <div class="guide-item"><div class="guide-dot" style="background:#ff9900;"></div>
        <div class="guide-text"><strong>Medium Risk (40–70%)</strong>: Perlu dipantau.</div></div>
        <div class="guide-item"><div class="guide-dot" style="background:#22cc66;"></div>
        <div class="guide-text"><strong>Low Risk (&lt;40%)</strong>: Customer relatif loyal.</div></div>
        </div>""", unsafe_allow_html=True)
    with g3:
        st.markdown("""<div class="guide-box"><h4>⚙️ Bagaimana Model Bekerja?</h4>
        <div class="guide-item"><div class="guide-dot" style="background:#0f2942;"></div>
        <div class="guide-text">Dilatih dengan <strong>XGBoost + SMOTE</strong> dari data historis pelanggan.</div></div>
        <div class="guide-item"><div class="guide-dot" style="background:#0f2942;"></div>
        <div class="guide-text">Faktor terpenting: tenure, kontrak, tagihan, internet, dan layanan tambahan.</div></div>
        <div class="guide-item"><div class="guide-dot" style="background:#0f2942;"></div>
        <div class="guide-text">Gunakan sebagai <strong>panduan keputusan</strong>, bukan kepastian absolut.</div></div>
        </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<hr style="border:none;border-top:1px solid #e0e8f2;margin:2rem 0 1rem;">
<div style="text-align:center;color:#8a9ab8;font-size:0.82rem;padding-bottom:1rem;">
  Telco Customer Churn Risk Dashboard &nbsp;|&nbsp;
  Powered by XGBoost + SMOTE &nbsp;|&nbsp;
  Capstone Project — Data Science
</div>
""", unsafe_allow_html=True)
