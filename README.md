# TaniBot AI Engine — IoT Soil Probe for P2L

Backend intelligence untuk aplikasi mobile **Pekarangan Pangan Lestari (P2L)** yang terhubung dengan alat IoT *handheld soil probe*. Sistem ini menerima data sensor tanah (suhu, kelembapan, pH) dan menyediakan tiga mode analisis yang menggabungkan **Machine Learning (scikit-learn)** dengan **LLM (Groq API)**.

> Dikembangkan untuk **GEMASTIK 2026** — Sub-tim AI & Mobile App, kategori IoT for Food Estate.

---

## Fitur Utama

Sistem menyediakan tiga mode analisis melalui REST API (FastAPI):

| Mode | Endpoint | Deskripsi |
|---|---|---|
| **1. Plant-First** (Evaluator) | `POST /api/evaluate` | User memilih tanaman target → sistem membandingkan kondisi tanah dengan rentang ideal tanaman tersebut (rule-based) dan menghasilkan insight bahasa natural via LLM |
| **2. Soil-First** (Recommender) | `POST /api/recommend` | User cukup mengukur tanah → model KNN merekomendasikan tanaman yang paling cocok beserta ringkasan naratif dari LLM |
| **3. Chatbot** (TaniBot) | `POST /api/chat` | Konsultasi pertanian bebas berbasis LLM, dengan konteks data sensor terakhir |

Selain itu tersedia utilitas:
- `GET /api/crops` — daftar profil tanaman & rentang ideal (untuk dikirim ke perangkat IoT/mobile)
- `GET /health` — health check (status LLM & model)

Arsitektur bersifat **hybrid**: keputusan/verdict inti dihasilkan secara deterministik (rule-based / model ML), sedangkan LLM (Groq) hanya menambahkan penjelasan bahasa natural. Jika LLM tidak tersedia, endpoint tetap berfungsi tanpa insight/summary/chat.

---

## Arsitektur

```
Sensor (temp, humidity, pH)
        │
        ▼
┌───────────────────────────────────────────┐
│                 FastAPI (api/)             │
│  routes: plant_first · soil_first · chatbot│
└───────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────┐
│               AI Engine (ai/)              │
│                                             │
│  ┌─────────────────┐   ┌─────────────────┐ │
│  │ Rule-Based       │   │ KNN Recommender │ │
│  │ Evaluator        │   │ (scikit-learn)  │ │
│  │ (crop_ideal_     │   │ model.pkl +     │ │
│  │  ranges.json)    │   │ scaler.pkl      │ │
│  └────────┬─────────┘   └────────┬────────┘ │
│           │                      │           │
│           └──────────┬───────────┘           │
│                       ▼                       │
│           ┌────────────────────────┐          │
│           │  Groq LLM Client        │          │
│           │  • Insight Summarizer   │          │
│           │  • TaniBot Chatbot      │          │
│           └────────────────────────┘          │
└───────────────────────────────────────────┘
```

Streamlit (`streamlit_app.py`) disediakan sebagai dashboard pengujian manual yang mengonsumsi API secara langsung — berguna untuk demo tanpa perlu mobile app.

---

## Struktur Proyek

```
.
├── ai/                             # Core AI engine
│   ├── llm/
│   │   ├── groq_client.py          # Wrapper client Groq API (chat completions)
│   │   ├── summarizer.py           # Insight (Mode 1) & summary (Mode 2) generator
│   │   ├── chatbot.py              # TaniBot — chatbot konsultasi pertanian (Mode 3)
│   │   └── prompts/                # Template prompt (insight, summarization, system prompt chatbot)
│   ├── models/
│   │   ├── evaluator/
│   │   │   ├── evaluator_engine.py     # Logika Plant-First (rule-based)
│   │   │   └── remediation_rules.json  # Saran perbaikan tanah per parameter
│   │   └── recommender/
│   │       ├── train_model.py          # Script training KNN
│   │       ├── recommender_engine.py   # Inference Soil-First
│   │       ├── model.pkl / scaler.pkl  # Model & scaler hasil training (gitignored)
│   └── utils/
│       ├── constants.py            # Path, konfigurasi, threshold, enum status
│       └── helpers.py              # Fungsi utilitas (load_json, calculate_deviation, dll.)
├── api/                            # Lapisan API (FastAPI)
│   ├── app.py                      # Entry point, wiring service & router
│   ├── routes/                     # Endpoint per mode (plant_first, soil_first, chatbot)
│   └── schemas/                    # Pydantic request/response models
├── data/
│   ├── raw/P2L_Urban_Crop_Dataset.csv     # Dataset training (temperature, humidity, ph, label)
│   └── crop_profiles/crop_ideal_ranges.json  # Rentang ideal per tanaman (Mode 1)
├── streamlit_app.py                # Dashboard pengujian manual (UI untuk ketiga mode)
├── requirements.txt
├── .env.example                    # Template environment variable
├── PRD_AI_System.md                # Product Requirements Document (desain awal sistem)
└── IoT_FoodEstate_Research_Notes.md # Catatan riset IoT & food estate
```

---

## Tanaman yang Didukung

Dataset dan profil ideal (`data/crop_profiles/crop_ideal_ranges.json`) saat ini mencakup 15 komoditas sayuran pekarangan (P2L):

Cabai Rawit, Cabai Keriting, Tomat, Bayam, Kangkung, Selada, Terong, Timun, Bawang Merah, Bawang Putih, Sawi, Kacang Panjang, Seledri, Pare, Kemangi.

> Catatan: dataset ini (`P2L_Urban_Crop_Dataset.csv`) menggantikan dataset awal `Crop_recommendation.csv` (Kaggle, 22 kelas tanaman umum) yang masih tersimpan di root sebagai referensi/riwayat.

---

## Instalasi & Menjalankan

### 1. Prasyarat
- Python 3.10+

### 2. Setup environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 3. Konfigurasi environment variable

Salin `.env.example` menjadi `.env` lalu isi API key Groq:

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
GROQ_MAX_TOKENS=500
GROQ_TEMPERATURE=0.7
```

API key gratis dapat diperoleh di [console.groq.com](https://console.groq.com). Jika `GROQ_API_KEY` tidak diisi, endpoint ML (`/evaluate`, `/recommend`) tetap berjalan tanpa insight LLM, dan `/chat` tidak akan menghasilkan balasan.

### 4. Training model rekomendasi (Mode 2)

Model KNN belum tersedia sampai dilatih (`model.pkl`/`scaler.pkl` bersifat gitignored):

```bash
python -m ai.models.recommender.train_model
```

Script ini melatih `KNeighborsClassifier` dari `data/raw/P2L_Urban_Crop_Dataset.csv` menggunakan fitur `temperature`, `humidity`, `ph`, lalu menyimpan model & scaler ke `ai/models/recommender/`.

### 5. Menjalankan API

```bash
uvicorn api.app:app --reload
```

API berjalan di `http://localhost:8000`. Dokumentasi interaktif (Swagger) tersedia di `http://localhost:8000/docs`.

### 6. Menjalankan dashboard pengujian (opsional)

```bash
streamlit run streamlit_app.py
```

Dashboard ini (di `http://localhost:8501`) menyediakan slider simulasi data sensor dan UI untuk mencoba ketiga mode langsung ke API lokal.

---

## Contoh Pemakaian API

**Mode 1 — Plant-First:**
```bash
curl -X POST http://localhost:8000/api/evaluate \
  -H "Content-Type: application/json" \
  -d '{"crop_name": "tomat", "sensor_data": {"temperature": 25.5, "humidity": 70.0, "ph": 5.5}}'
```

**Mode 2 — Soil-First:**
```bash
curl -X POST http://localhost:8000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"sensor_data": {"temperature": 25.5, "humidity": 70.0, "ph": 6.5}, "top_n": 5}'
```

**Mode 3 — Chatbot:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Kenapa daun tomat saya menguning?", "sensor_context": {"temperature": 32.0, "humidity": 45.0, "ph": 5.2}}'
```

---

## Tech Stack

| Komponen | Teknologi |
|---|---|
| API Framework | FastAPI + Uvicorn |
| Validasi Data | Pydantic |
| Machine Learning | scikit-learn (KNN + StandardScaler), joblib |
| Data Processing | pandas, numpy |
| LLM Provider | Groq API (`llama-3.1-8b-instant`) |
| Dashboard Uji Coba | Streamlit |
| Konfigurasi | python-dotenv |
| Testing | pytest, pytest-asyncio, httpx |

---

## Dokumen Terkait

- [`PRD_AI_System.md`](PRD_AI_System.md) — spesifikasi produk lengkap (rancangan awal; beberapa detail seperti provider LLM dan skema request/response telah berevolusi dari implementasi aktual di atas)
- [`IoT_FoodEstate_Research_Notes.md`](IoT_FoodEstate_Research_Notes.md) — catatan riset seputar IoT & food estate
