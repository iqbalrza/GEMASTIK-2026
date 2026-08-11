# PRD: Sistem AI — IoT Soil Probe for P2L
**Product Requirements Document**  
**Project:** GEMASTIK 2026 — IoT for Food Estate (AI & Mobile App Sub-Team)  
**Version:** 1.0  
**Date:** 8 Agustus 2026  

---

## 1. Ringkasan Produk

Sistem AI ini merupakan *backend intelligence* dari aplikasi mobile yang terintegrasi dengan alat IoT handheld soil probe. AI menerima data sensor tanah (pH, Kelembapan/Humidity, Suhu/Temperature) via Bluetooth dan menyediakan **tiga mode analisis** yang menggabungkan **Traditional ML + LLM (Gemini API)**:

1. **Plant-First (Evaluator + Gemini)** — Validasi kesesuaian lahan + insight natural language dari Gemini
2. **Soil-First (Recommender + Gemini)** — Rekomendasi tanaman otomatis + rangkuman bahasa sederhana
3. **Chatbot Konsultasi Pertanian (Gemini)** — Tanya-jawab bebas seputar pertanian berbasis konteks sensor

### Arsitektur AI Hybrid

```
┌─────────────────────────────────────────────────────┐
│                   AI ENGINE                          │
│                                                      │
│  ┌──────────────┐    ┌───────────────────────────┐   │
│  │ Traditional  │    │ LLM Layer (Gemini API)    │   │
│  │ ML/Rule-Based│    │                           │   │
│  │              │    │ • Natural Language Insight │   │
│  │ • KNN Model  │───►│ • Insight Summarization   │   │
│  │ • Rule-Based │    │ • Chatbot Pertanian       │   │
│  │   Evaluator  │    │                           │   │
│  └──────────────┘    └───────────────────────────┘   │
│         ▲                        │                    │
│         │                        ▼                    │
│    Sensor Data              User-Friendly             │
│    (temp, hum, ph)          Response (Bahasa          │
│                             Indonesia)                │
└─────────────────────────────────────────────────────┘
```

> **Referensi:** Dokumen ini disusun berdasarkan [IoT_FoodEstate_Research_Notes.md](file:///c:/Users/iqbal/Documents/Code%20Labs/GEMASTIK%2020206/IoT_FoodEstate_Research_Notes.md) Bagian §13–§16.

---

## 2. Struktur Folder Proyek

```
GEMASTIK 20206/
│
├── 📄 IoT_FoodEstate_Research_Notes.md        # Dokumentasi riset utama
├── 📄 PRD_AI_System.md                        # Dokumen ini
├── 📄 .env                                    # API keys (GEMINI_API_KEY) — JANGAN commit!
├── 📄 .env.example                            # Template environment variables
│
├── 📂 data/                                   # Dataset & data processing
│   ├── raw/
│   │   └── Crop_recommendation.csv            # Dataset asli (7 kolom)
│   ├── processed/
│   │   └── Crop_recommendation_simple.csv     # Dataset terfilter (4 kolom)
│   └── crop_profiles/
│       └── crop_ideal_ranges.json             # Rentang ideal per tanaman (Mode 1)
│
├── 📂 ai/                                     # Core AI Engine
│   ├── models/
│   │   ├── recommender/
│   │   │   ├── train_model.py                 # Script training model Soil-First
│   │   │   ├── model.pkl                      # Model tersimpan (KNN/Decision Tree)
│   │   │   └── model_evaluation.py            # Evaluasi akurasi model
│   │   └── evaluator/
│   │       ├── evaluator_engine.py            # Logika Plant-First (rule-based)
│   │       └── remediation_rules.json         # Database saran perbaikan tanah
│   ├── llm/                                   # 🆕 LLM Layer (Gemini API)
│   │   ├── gemini_client.py                   # Wrapper/client untuk Gemini API
│   │   ├── prompts/
│   │   │   ├── insight_generation.py           # Prompt template: Natural Language Insight
│   │   │   ├── summarization.py               # Prompt template: Insight Summarization
│   │   │   └── chatbot_system.py              # Prompt template: System prompt chatbot
│   │   ├── chatbot.py                         # 🆕 Chatbot Konsultasi Pertanian
│   │   └── summarizer.py                      # 🆕 Insight Summarization engine
│   ├── preprocessing/
│   │   ├── data_cleaner.py                    # Pembersihan & normalisasi data
│   │   └── feature_engineering.py             # Ekstraksi fitur tambahan
│   ├── utils/
│   │   ├── constants.py                       # Konstanta global (threshold, label mapping)
│   │   └── helpers.py                         # Fungsi utilitas umum
│   └── tests/
│       ├── test_recommender.py                # Unit test Mode 2
│       ├── test_evaluator.py                  # Unit test Mode 1
│       ├── test_chatbot.py                    # 🆕 Unit test Mode 3 (Chatbot)
│       └── test_gemini_client.py              # 🆕 Unit test Gemini integration
│
├── 📂 api/                                    # API layer (Mobile App ↔ AI)
│   ├── app.py                                 # Entry point API (FastAPI)
│   ├── routes/
│   │   ├── plant_first.py                     # Endpoint Mode 1: POST /api/evaluate
│   │   ├── soil_first.py                      # Endpoint Mode 2: POST /api/recommend
│   │   └── chatbot.py                         # 🆕 Endpoint Mode 3: POST /api/chat
│   ├── schemas/
│   │   ├── request_models.py                  # Skema input (Pydantic)
│   │   └── response_models.py                 # Skema output (Pydantic)
│   └── middleware/
│       └── validation.py                      # Validasi range sensor input
│
├── 📂 mobile/                                 # Mobile App (placeholder — tim terpisah)
│   └── README.md                              # Referensi integrasi untuk tim Mobile
│
├── 📂 docs/                                   # Dokumentasi tambahan
│   ├── api_reference.md                       # Dokumentasi endpoint API
│   ├── algorithm_notes.md                     # Catatan teknis algoritma
│   ├── gemini_integration.md                  # 🆕 Panduan integrasi Gemini API
│   └── bluetooth_protocol.md                  # Spesifikasi protokol BLE data format
│
├── 📄 requirements.txt                        # Dependensi Python
└── 📄 README.md                               # Overview proyek
```

---

## 3. Spesifikasi Dataset

### 3.1 Sumber Data
- **Dataset:** Crop Recommendation Dataset (Kaggle)
- **File asli:** `Crop_recommendation.csv` — 7 kolom, 2200 baris
- **File terfilter:** `Crop_recommendation_simple.csv` — 4 kolom, 2200 baris

### 3.2 Kolom yang Digunakan

| Kolom | Tipe | Satuan | Deskripsi | Korelasi Sensor IoT |
|---|---|---|---|---|
| `temperature` | float | °C | Suhu lingkungan/tanah | DS18B20 Waterproof Temp Sensor |
| `humidity` | float | % | Kelembapan relatif | Capacitive Moisture Sensor |
| `ph` | float | 0–14 | Tingkat keasaman tanah | Soil pH Sensor (analog) + DMS |
| `label` | string | — | Nama tanaman (22 kelas) | — (target prediksi) |

### 3.3 Label Tanaman (22 Kelas)

| # | Label | # | Label | # | Label |
|---|---|---|---|---|---|
| 1 | apple | 9 | jute | 17 | orange |
| 2 | banana | 10 | kidneybeans | 18 | papaya |
| 3 | blackgram | 11 | lentil | 19 | pigeonpeas |
| 4 | chickpea | 12 | maize | 20 | pomegranate |
| 5 | coconut | 13 | mango | 21 | rice |
| 6 | coffee | 14 | mothbeans | 22 | watermelon |
| 7 | cotton | 15 | mungbean | | |
| 8 | grapes | 16 | muskmelon | | |

### 3.4 Kolom yang Dihapus (alasan)

| Kolom | Alasan Dihapus |
|---|---|
| `N` (Nitrogen) | Tidak diukur oleh sensor MVP (NPK sensor deferred ke V2) |
| `P` (Fosfor) | Tidak diukur oleh sensor MVP |
| `K` (Kalium) | Tidak diukur oleh sensor MVP |
| `rainfall` | Tidak diukur oleh sensor handheld (bukan parameter tanah real-time) |

---

## 4. Spesifikasi AI Mode 1: Plant-First (Evaluator)

### 4.1 Deskripsi
Pengguna yang **sudah memiliki target tanaman** dapat memvalidasi apakah kondisi tanah mereka cocok. Sistem memberikan evaluasi kesesuaian + saran perbaikan (*actionable insight*).

### 4.2 Alur Sistem

```
┌──────────────┐    ┌──────────────┐    ┌───────────────────┐    ┌──────────────────┐
│ User memilih │───►│ Probe IoT    │───►│ Evaluator Engine  │───►│ Actionable       │
│ tanaman      │    │ kirim data   │    │ bandingkan dengan │    │ Insight + Saran  │
│ (e.g. Tomat) │    │ (BLE)        │    │ ideal range       │    │ Perbaikan        │
└──────────────┘    └──────────────┘    └───────────────────┘    └──────────────────┘
```

### 4.3 Pendekatan: Rule-Based Evaluator + Gemini LLM

Menggunakan pendekatan **hybrid** (rule-based + LLM):
- **Rule-based** untuk evaluasi logis (perbandingan nilai vs rentang ideal) — cepat, deterministik
- **Gemini API** untuk menghasilkan penjelasan natural language yang kontekstual dan edukatif
- Hasil rule-based menjadi *structured input* ke Gemini, bukan sebaliknya (LLM tidak menentukan verdict)

### 4.4 Data Referensi: `crop_ideal_ranges.json`

Rentang ideal per tanaman dihitung dari **statistik deskriptif dataset** (mean ± 1 std) atau dari literatur agronomi.

```json
{
  "rice": {
    "temperature": { "min": 20.0, "max": 27.0, "unit": "°C" },
    "humidity":    { "min": 80.0, "max": 85.0, "unit": "%" },
    "ph":          { "min": 5.0,  "max": 8.0,  "unit": "" }
  },
  "maize": {
    "temperature": { "min": 22.0, "max": 28.0, "unit": "°C" },
    "humidity":    { "min": 55.0, "max": 75.0, "unit": "%" },
    "ph":          { "min": 5.5,  "max": 7.5,  "unit": "" }
  }
}
```

### 4.5 Logika Evaluasi

Untuk setiap parameter (`temperature`, `humidity`, `ph`):

```
Jika nilai_aktual berada dalam [min, max]   → STATUS: ✅ IDEAL
Jika deviasi ≤ 10% dari batas terdekat     → STATUS: ⚠️ MARGINAL
Jika deviasi > 10% dari batas terdekat     → STATUS: ❌ TIDAK COCOK
```

**Skor keseluruhan:**

| Kondisi | Verdict | Ikon |
|---|---|---|
| Semua parameter ✅ | TANAH SANGAT COCOK | 😊 |
| Ada parameter ⚠️, tidak ada ❌ | TANAH CUKUP COCOK (perlu penyesuaian) | 😐 |
| Ada parameter ❌ | TANAH TIDAK COCOK (perlu tindakan) | 😟 |

### 4.6 Saran Perbaikan (Remediation Rules — Fallback)

Setiap kondisi ❌ atau ⚠️ memiliki template saran sebagai **fallback** jika Gemini API tidak tersedia:

| Parameter | Kondisi | Saran Template (Fallback) |
|---|---|---|
| pH | Terlalu asam (< ideal min) | "Taburkan kapur dolomit untuk menaikkan pH" |
| pH | Terlalu basa (> ideal max) | "Tambahkan belerang atau pupuk kompos untuk menurunkan pH" |
| Humidity | Terlalu kering (< ideal min) | "Siram tanah lebih sering atau tambahkan mulsa untuk menjaga kelembapan" |
| Humidity | Terlalu basah (> ideal max) | "Perbaiki drainase tanah atau kurangi frekuensi penyiraman" |
| Temperature | Terlalu dingin (< ideal min) | "Gunakan mulsa hitam untuk meningkatkan suhu tanah" |
| Temperature | Terlalu panas (> ideal max) | "Tambahkan naungan atau mulsa tebal untuk menurunkan suhu tanah" |

### 4.7 Gemini LLM Enhancement: Natural Language Insight

Setelah rule-based engine menghasilkan verdict + template saran, data tersebut dikirim ke **Gemini API** untuk menghasilkan penjelasan yang lebih kaya dan kontekstual.

#### Prompt Template (`insight_generation.py`)

```python
INSIGHT_PROMPT = """
Kamu adalah ahli agronomi Indonesia yang menjelaskan kondisi tanah kepada petani pemula.

Data sensor tanah saat ini:
- Suhu: {temperature}°C
- Kelembapan: {humidity}%
- pH: {ph}

Tanaman target: {crop_name}
Rentang ideal: Suhu {temp_min}-{temp_max}°C, Kelembapan {hum_min}-{hum_max}%, pH {ph_min}-{ph_max}

Hasil evaluasi sistem:
{evaluation_result}

Berdasarkan data di atas, berikan:
1. Penjelasan singkat mengapa kondisi tanah ini cocok/tidak cocok untuk {crop_name}
2. Langkah perbaikan yang spesifik dan praktis (jika diperlukan)
3. Tips tambahan untuk perawatan {crop_name} di kondisi ini

Gunakan bahasa Indonesia yang sederhana dan mudah dipahami oleh masyarakat umum.
Batasi jawaban maksimal 150 kata.
"""
```

#### Alur Hybrid (Rule-Based → Gemini)

```
┌─────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│ Sensor Data │────►│ Rule-Based       │────►│ Gemini API          │
│ + Crop      │     │ Evaluator        │     │ (Insight Generation)│
│             │     │                  │     │                     │
│             │     │ Output:          │     │ Output:             │
│             │     │ • Verdict (✅❌⚠️) │     │ • Penjelasan natural│
│             │     │ • Skor           │     │ • Tips kontekstual  │
│             │     │ • Template saran │     │ • Saran praktis     │
└─────────────┘     └──────────────────┘     └─────────────────────┘
                           │                          │
                           │    ┌─────────────────┐   │
                           └───►│ FINAL RESPONSE  │◄──┘
                                │ (Structured +   │
                                │  Natural Lang.) │
                                └─────────────────┘
```

### 4.8 Contoh Response (dengan Gemini Enhancement)

```json
{
  "mode": "plant-first",
  "selected_crop": "rice",
  "sensor_data": {
    "temperature": 25.5,
    "humidity": 70.0,
    "ph": 5.5
  },
  "overall_verdict": "CUKUP COCOK",
  "overall_icon": "😐",
  "parameters": [
    {
      "name": "temperature",
      "value": 25.5,
      "ideal_range": [20.0, 27.0],
      "status": "IDEAL",
      "icon": "✅"
    },
    {
      "name": "humidity",
      "value": 70.0,
      "ideal_range": [80.0, 85.0],
      "status": "TIDAK COCOK",
      "icon": "❌",
      "deviation_percent": -12.5
    },
    {
      "name": "ph",
      "value": 5.5,
      "ideal_range": [5.0, 8.0],
      "status": "IDEAL",
      "icon": "✅"
    }
  ],
  "gemini_insight": {
    "summary": "Tanah Anda cukup cocok untuk padi, tapi kelembapan perlu ditingkatkan.",
    "explanation": "Suhu 25.5°C dan pH 5.5 sudah pas untuk padi. Namun, kelembapan tanah 70% masih kurang dari kebutuhan padi yang idealnya 80-85%. Padi membutuhkan tanah yang cukup basah karena sistem perakaran padi berkembang optimal di kondisi lembap.",
    "action_steps": [
      "Siram tanah secara merata hingga kelembapan naik ke 80%",
      "Tambahkan mulsa jerami di permukaan untuk menahan uap air",
      "Pertimbangkan sistem pengairan sederhana jika lahan cukup luas"
    ],
    "tips": "Untuk padi di pekarangan, gunakan pot/wadah besar berisi air setinggi 2-3 cm agar kelembapan selalu terjaga.",
    "model_used": "gemini-2.0-flash"
  }
}
```

---

## 5. Spesifikasi AI Mode 2: Soil-First (Recommender + Gemini Summarization)

### 5.1 Deskripsi
Pengguna **tanpa target tanaman** cukup menancapkan probe ke tanah. AI memindai seluruh dataset dan menampilkan daftar tanaman yang paling cocok. **Gemini** kemudian merangkum hasil rekomendasi ke bahasa yang mudah dipahami.

### 5.2 Alur Sistem

```
┌──────────────┐    ┌──────────────────┐    ┌──────────────────┐    ┌───────────────┐    ┌────────────┐
│ Probe IoT    │───►│ Data diterima    │───►│ ML Model         │───►│ Gemini API    │───►│ Ranking +  │
│ kirim data   │    │ oleh Mobile App  │    │ (KNN / Decision  │    │ Summarizer    │    │ Ringkasan  │
│ (BLE)        │    │ (temp, hum, ph)  │    │  Tree)           │    │               │    │ Natural    │
└──────────────┘    └──────────────────┘    └──────────────────┘    └───────────────┘    └────────────┘
```

### 5.3 Kandidat Algoritma

| Algoritma | Kelebihan | Kekurangan | Prioritas |
|---|---|---|---|
| **K-Nearest Neighbors (KNN)** | Sederhana, interpretable, natural untuk similarity matching | Lambat di dataset besar (bukan masalah di 2200 baris) | ⭐ **Utama** |
| **Decision Tree** | Cepat, menghasilkan rules yang readable | Rentan overfitting tanpa pruning | Alternatif |
| **Random Forest** | Akurasi lebih tinggi, robust | Kurang interpretable untuk user-facing explanation | Alternatif |

### 5.4 Pendekatan Rekomendasi (KNN-Based)

#### Training Phase
1. Load `Crop_recommendation_simple.csv`
2. Preprocessing: normalisasi fitur menggunakan `StandardScaler` atau `MinMaxScaler`
3. Train KNN classifier dengan `n_neighbors` optimal (tuning via cross-validation)
4. Simpan model ke `model.pkl`

#### Inference Phase
1. Terima input sensor: `{ temperature, humidity, ph }`
2. Normalisasi input dengan scaler yang sama
3. Hitung jarak ke semua titik data (Euclidean distance)
4. Ambil K tetangga terdekat
5. Hitung probabilitas per kelas tanaman dari K tetangga
6. Kembalikan **Top-N tanaman** dengan probabilitas tertinggi

### 5.5 Metrik Evaluasi Model

| Metrik | Target | Deskripsi |
|---|---|---|
| Accuracy | ≥ 85% | Ketepatan prediksi kelas teratas |
| Precision (weighted) | ≥ 80% | Relevansi rekomendasi per kelas |
| Recall (weighted) | ≥ 80% | Cakupan per kelas tanaman |
| F1-Score (weighted) | ≥ 80% | Harmonic mean precision & recall |

### 5.6 Gemini Summarization Layer

#### Prompt Template (`summarization.py`)

```python
SUMMARIZATION_PROMPT = """
Kamu adalah ahli pertanian yang merangkum hasil analisis tanah untuk petani pemula.

Kondisi tanah saat ini:
- Suhu: {temperature}°C
- Kelembapan: {humidity}%
- pH: {ph}

Hasil rekomendasi sistem (berdasarkan Machine Learning):
{ranking_list}

Buatkan ringkasan dalam bahasa Indonesia sederhana yang mencakup:
1. Gambaran umum kondisi tanah dalam 1-2 kalimat
2. Mengapa tanaman peringkat 1 paling cocok
3. Tips singkat untuk memulai menanam tanaman yang direkomendasikan

Batasi jawaban maksimal 120 kata. Gunakan bahasa yang ramah dan memotivasi.
"""
```

### 5.7 Contoh Response (dengan Gemini Summarization)

```json
{
  "mode": "soil-first",
  "sensor_data": {
    "temperature": 25.5,
    "humidity": 70.0,
    "ph": 6.5
  },
  "top_recommendations": [
    {
      "rank": 1,
      "crop": "maize",
      "confidence": 0.92,
      "confidence_percent": "92%",
      "ideal_match": {
        "temperature": "✅ Cocok",
        "humidity": "✅ Cocok",
        "ph": "✅ Cocok"
      }
    },
    {
      "rank": 2,
      "crop": "cotton",
      "confidence": 0.78,
      "confidence_percent": "78%"
    },
    {
      "rank": 3,
      "crop": "coffee",
      "confidence": 0.65,
      "confidence_percent": "65%"
    }
  ],
  "total_crops_evaluated": 22,
  "gemini_summary": {
    "overview": "Tanah Anda dalam kondisi baik dengan suhu hangat dan pH netral. Ini cocok untuk berbagai jenis tanaman!",
    "top_pick_reason": "Jagung (Maize) jadi pilihan terbaik karena ketiga parameter tanah Anda — suhu, kelembapan, dan pH — semuanya pas di rentang idealnya. Jagung juga termasuk tanaman yang mudah dirawat untuk pemula.",
    "quick_tips": "Mulai dengan menanam 3-5 biji jagung per lubang, kedalaman 3 cm, jarak antar lubang 25 cm. Siram setiap pagi dan sore. Dalam 7-10 hari, tunas akan mulai muncul!",
    "model_used": "gemini-2.0-flash"
  }
}
```

---

## 6. Spesifikasi AI Mode 3: Chatbot Konsultasi Pertanian (Gemini)

### 6.1 Deskripsi
Fitur chatbot memungkinkan pengguna bertanya bebas seputar pertanian menggunakan bahasa natural. Chatbot memiliki **konteks data sensor** sehingga jawaban relevan dengan kondisi tanah yang baru diukur.

### 6.2 Alur Sistem

```
┌────────────────┐    ┌──────────────────────────────────────────┐
│ User bertanya: │    │            Gemini API                    │
│ "Kenapa daun   │───►│                                          │
│  tomat saya    │    │ System Prompt:                           │
│  menguning?"   │    │ • Persona: Ahli agronomi Indonesia       │
│                │    │ • Konteks: Data sensor terakhir          │
│ + sensor_data  │    │ • Batasan: Hanya topik pertanian         │
│   (opsional)   │    │                                          │
└────────────────┘    │ Output: Jawaban natural + saran praktis  │
                      └──────────────────────────────────────────┘
```

### 6.3 System Prompt (`chatbot_system.py`)

```python
CHATBOT_SYSTEM_PROMPT = """
Kamu adalah "TaniBot", asisten pertanian cerdas berbahasa Indonesia yang ramah dan sabar.

Peranmu:
- Membantu petani pemula dan masyarakat program P2L (Pekarangan Pangan Lestari)
- Menjawab pertanyaan tentang persiapan tanah, penanaman, perawatan, hama, dan panen
- Memberikan saran praktis yang bisa dilakukan di pekarangan rumah

Konteks sensor IoT (jika tersedia):
{sensor_context}

Aturan:
1. Jawab HANYA pertanyaan seputar pertanian, tanaman, dan tanah
2. Jika pertanyaan di luar topik, tolak dengan sopan dan arahkan kembali ke pertanian
3. Gunakan bahasa Indonesia yang sederhana, hindari istilah teknis berlebihan
4. Berikan jawaban praktis yang bisa langsung diterapkan
5. Jika data sensor tersedia, kaitkan jawaban dengan kondisi tanah pengguna
6. Batasi jawaban maksimal 200 kata
7. Jika tidak yakin, katakan jujur dan sarankan konsultasi ke penyuluh pertanian
"""
```

### 6.4 Fitur Chatbot

| Fitur | Deskripsi |
|---|---|
| **Context-Aware** | Jawaban dikaitkan dengan data sensor terakhir (jika ada) |
| **Conversation History** | Menyimpan riwayat chat per session (max 10 turn) |
| **Topic Guard** | Menolak pertanyaan di luar topik pertanian |
| **Bahasa Indonesia** | Respons selalu dalam bahasa Indonesia sederhana |
| **Quick Suggestions** | Menyediakan 3 pertanyaan lanjutan yang relevan |

### 6.5 Contoh Interaksi

**Input:**
```json
{
  "message": "Kenapa daun tomat saya menguning?",
  "sensor_context": {
    "temperature": 32.0,
    "humidity": 45.0,
    "ph": 5.2
  },
  "conversation_history": []
}
```

**Response:**
```json
{
  "mode": "chatbot",
  "response": "Daun tomat menguning bisa disebabkan beberapa hal. Melihat data sensor tanah Anda, ada 2 kemungkinan utama:\n\n1. **pH terlalu asam (5.2)** — Tomat butuh pH 6.0-7.0. pH rendah membuat tanaman sulit menyerap nutrisi, terutama nitrogen, sehingga daun menguning dari bawah. Solusi: tambahkan kapur dolomit 100-150 gram per m².\n\n2. **Kelembapan rendah (45%)** — Tanah terlalu kering membuat akar stres. Siram secara teratur pagi dan sore.\n\nSuhu 32°C juga agak tinggi untuk tomat. Coba pasang paranet untuk mengurangi panas.",
  "suggestions": [
    "Berapa banyak kapur dolomit yang harus saya taburkan?",
    "Kapan waktu terbaik menyiram tomat?",
    "Bagaimana cara membuat paranet sederhana?"
  ],
  "model_used": "gemini-2.0-flash"
}
```

---

## 7. Gemini API Integration Details

### 7.1 Tech Stack

| Komponen | Teknologi | Alasan |
|---|---|---|
| API Framework | **FastAPI** (Python) | Async, auto-docs (Swagger), Pydantic validation |
| ML Library | **scikit-learn** | KNN, Decision Tree, preprocessing pipeline |
| LLM Provider | **Google Gemini API** | Gratis (tier free), bahasa Indonesia bagus, fast inference |
| Gemini SDK | **google-genai** | Official Python SDK untuk Gemini API |
| Serialization | **joblib / pickle** | Menyimpan trained model |
| Data Processing | **pandas, numpy** | Manipulasi dataset |

### 7.2 Gemini Client Wrapper (`gemini_client.py`)

```python
import os
from google import genai
from google.genai import types

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = "gemini-2.0-flash"  # Fast, free-tier friendly
    
    async def generate_insight(self, prompt: str) -> str:
        """Generate natural language insight from structured data."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.7,
                max_output_tokens=500,
            )
        )
        return response.text
    
    async def chat(self, messages: list, system_prompt: str) -> str:
        """Multi-turn chatbot conversation."""
        response = self.client.models.generate_content(
            model=self.model,
            contents=messages,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.8,
                max_output_tokens=600,
            )
        )
        return response.text
```

### 7.3 Model Selection

| Model | Use Case | Alasan |
|---|---|---|
| `gemini-2.0-flash` | Insight, Summarization, Chatbot | Cepat, murah/gratis, cukup untuk text generation |
| `gemini-2.5-flash` | Fallback jika butuh reasoning lebih | Thinking model, lebih akurat untuk analisis kompleks |

### 7.4 Rate Limiting & Error Handling

| Skenario | Handling |
|---|---|
| Gemini API down / timeout | Fallback ke template saran statis dari `remediation_rules.json` |
| Rate limit exceeded (free tier) | Queue + retry dengan exponential backoff |
| Response tidak relevan | Validate output, retry 1x jika gagal |
| API key tidak valid | Return error 503 + log warning |

### 7.5 Environment Variables

```env
# .env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.0-flash
GEMINI_MAX_TOKENS=500
GEMINI_TEMPERATURE=0.7
```

---

## 8. Spesifikasi API Endpoints

### 8.1 Endpoints Overview

| Method | Endpoint | Mode | Deskripsi |
|---|---|---|---|
| `POST` | `/api/evaluate` | Mode 1 | Plant-First + Gemini Insight |
| `POST` | `/api/recommend` | Mode 2 | Soil-First + Gemini Summary |
| `POST` | `/api/chat` | Mode 3 | Chatbot Konsultasi Pertanian |
| `GET` | `/api/crops` | Utility | Daftar tanaman tersedia |
| `GET` | `/api/health` | Utility | Health check |

### 8.2 `POST /api/evaluate` — Mode 1: Plant-First

**Request Body:**
```json
{
  "crop": "rice",
  "temperature": 25.5,
  "humidity": 70.0,
  "ph": 5.5
}
```

**Response:** Lihat §4.8

**Validasi Input:**
| Field | Tipe | Range Valid | Required |
|---|---|---|---|
| `crop` | string | Salah satu dari 22 label | ✅ |
| `temperature` | float | 0.0 – 60.0 °C | ✅ |
| `humidity` | float | 0.0 – 100.0 % | ✅ |
| `ph` | float | 0.0 – 14.0 | ✅ |

---

### 8.3 `POST /api/recommend` — Mode 2: Soil-First

**Request Body:**
```json
{
  "temperature": 25.5,
  "humidity": 70.0,
  "ph": 6.5,
  "top_n": 5
}
```

**Response:** Lihat §5.7

**Validasi Input:**
| Field | Tipe | Range Valid | Required |
|---|---|---|---|
| `temperature` | float | 0.0 – 60.0 °C | ✅ |
| `humidity` | float | 0.0 – 100.0 % | ✅ |
| `ph` | float | 0.0 – 14.0 | ✅ |
| `top_n` | int | 1 – 22 | ❌ (default: 5) |

---

### 8.4 `POST /api/chat` — Mode 3: Chatbot 🆕

**Request Body:**
```json
{
  "message": "Kenapa daun tomat saya menguning?",
  "sensor_context": {
    "temperature": 32.0,
    "humidity": 45.0,
    "ph": 5.2
  },
  "conversation_history": [
    { "role": "user", "content": "Halo" },
    { "role": "assistant", "content": "Halo! Saya TaniBot..." }
  ]
}
```

**Response:** Lihat §6.5

**Validasi Input:**
| Field | Tipe | Deskripsi | Required |
|---|---|---|---|
| `message` | string | Pertanyaan user (max 500 char) | ✅ |
| `sensor_context` | object | Data sensor terakhir | ❌ (nullable) |
| `conversation_history` | array | Riwayat chat (max 10 turns) | ❌ (default: []) |

---

### 8.5 `GET /api/crops` — Daftar Tanaman

**Response:**
```json
{
  "total": 22,
  "crops": [
    { "id": 1, "name": "apple", "display_name": "Apel" },
    { "id": 2, "name": "banana", "display_name": "Pisang" },
    "..."
  ]
}
```

---

### 8.6 `GET /api/health` — Health Check

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "gemini_status": "connected",
  "version": "1.0.0"
}
```

---

## 9. Alur Data End-to-End (Updated)

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                        ALUR DATA LENGKAP (v2 — dengan Gemini)                │
│                                                                               │
│  [SENSOR]          [ESP32]           [BLE]          [MOBILE APP]             │
│                                                                               │
│  pH Sensor ──┐                                                                │
│  Moisture  ──┼──► ESP32-S3 ──► Bluetooth ──► App menerima JSON:             │
│  DS18B20   ──┘    │                          { temp, humidity, ph }          │
│                   │                                  │                        │
│                   ▼                                  ▼                        │
│              OLED Display                     ┌─────────────┐                │
│              (Indikator Cepat)                │ User memilih│                │
│              😊 / 😐 / 😟                     │ mode:       │                │
│                                               │             │                │
│                                               ├─► Mode 1 (Plant-First)       │
│                                               ├─► Mode 2 (Soil-First)        │
│                                               └─► Mode 3 (Chatbot) 🆕       │
│                                                             │                │
│                                    ┌────────────────────────┘                │
│                                    ▼                                          │
│                    ┌──────────────────────────────┐                           │
│                    │     AI ENGINE (Hybrid)        │                           │
│                    │                              │                           │
│                    │  ┌────────────┐  ┌────────┐  │                           │
│                    │  │ Rule-Based │  │  KNN   │  │                           │
│                    │  │ Evaluator  │  │ Model  │  │                           │
│                    │  └─────┬──────┘  └───┬────┘  │                           │
│                    │        │             │        │                           │
│                    │        ▼             ▼        │                           │
│                    │  ┌────────────────────────┐  │                           │
│                    │  │   Gemini API (LLM)     │  │                           │
│                    │  │  • Insight Generation  │  │                           │
│                    │  │  • Summarization       │  │                           │
│                    │  │  • Chatbot (TaniBot)   │  │                           │
│                    │  └────────────────────────┘  │                           │
│                    └──────────────────────────────┘                           │
│                                    │                                          │
│                                    ▼                                          │
│                           [HASIL DITAMPILKAN]                                │
│                           di layar Mobile App                                │
│                           (Natural Language 🇮🇩)                              │
└───────────────────────────────────────────────────────────────────────────────┘
```

---

## 10. Bluetooth Data Format (ESP32 → Mobile App)

### 10.1 Format Payload (JSON via BLE Serial)

```json
{
  "device_id": "SOILPROBE-001",
  "timestamp": 1723075200,
  "readings": {
    "temperature": 25.5,
    "humidity": 70.0,
    "ph": 6.5
  },
  "device_status": {
    "battery_percent": 85,
    "oled_verdict": "SEHAT"
  }
}
```

### 10.2 BLE Characteristics

| Characteristic | UUID (Placeholder) | Deskripsi |
|---|---|---|
| Soil Reading | `0000FFE1-...` | Payload JSON sensor reading |
| Device Status | `0000FFE2-...` | Battery level, device health |

---

## 11. Dependensi (`requirements.txt`)

```
# Core
fastapi>=0.100.0
uvicorn>=0.23.0
pydantic>=2.0.0

# Data Science & ML
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
joblib>=1.3.0

# LLM — Gemini API
google-genai>=1.0.0       # Official Google Gemini SDK

# Utilities
python-dotenv>=1.0.0

# Testing
pytest>=7.4.0
pytest-asyncio>=0.23.0   # Async test support (untuk Gemini calls)
httpx>=0.24.0             # Untuk testing FastAPI
```

---

## 12. Milestones & Timeline

| Phase | Task | Durasi | Output |
|---|---|---|---|
| **Phase 1** | Setup proyek + eksplorasi data | 2 hari | Folder structure, EDA notebook, `crop_ideal_ranges.json` |
| **Phase 2** | Implementasi Mode 1 (Plant-First Evaluator) | 3 hari | `evaluator_engine.py`, `remediation_rules.json`, unit tests |
| **Phase 3** | Training & evaluasi model Mode 2 (Soil-First) | 4 hari | `train_model.py`, `model.pkl`, evaluation report |
| **Phase 4** | Gemini API integration (LLM Layer) | 3 hari | `gemini_client.py`, prompt templates, insight & summarization |
| **Phase 5** | Implementasi Mode 3 (Chatbot TaniBot) | 3 hari | `chatbot.py`, system prompt, conversation handling |
| **Phase 6** | API development (FastAPI) | 3 hari | Semua endpoint (`/evaluate`, `/recommend`, `/chat`, `/crops`, `/health`) |
| **Phase 7** | Integrasi dengan Mobile App | 4 hari | BLE protocol, API integration, end-to-end testing |
| **Phase 8** | Testing & optimasi | 3 hari | Unit tests, edge case, Gemini fallback testing |

---

## 13. Risiko & Mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| Dataset hanya 3 fitur (tanpa NPK, rainfall) → akurasi menurun | Rekomendasi kurang akurat | Evaluasi akurasi model 3-fitur vs 7-fitur; jika < 70%, tambah literatur-based ranges |
| Sensor reading noise / outlier dari IoT | Prediksi salah | Input validation + outlier detection di preprocessing |
| Bluetooth latency / packet loss | Data tidak sampai ke app | Retry mechanism + fallback ke OLED display |
| Tanaman di dataset tidak sesuai konteks P2L Indonesia | Rekomendasi tidak relevan | Filter/mapping label ke tanaman P2L (sayuran, buah, obat) |
| **🆕 Gemini API downtime / rate limit** | Fitur LLM tidak bisa dipakai | Fallback ke template statis (`remediation_rules.json`) |
| **🆕 Gemini free tier quota habis** | Chatbot & insight mati | Monitor usage, set daily cap, prioritaskan Mode 1 & 2 |
| **🆕 LLM hallucination (jawaban salah)** | Petani mendapat saran keliru | Validasi output + disclaimer di UI + batasi scope via system prompt |
| **🆕 Latency Gemini API (network)** | UX lambat | Tampilkan data ML dulu (instan), Gemini insight lazy-load setelahnya |

---

## 14. Strategi Fallback (Offline / Gemini Down)

Sistem dirancang agar **Mode 1 & 2 tetap berfungsi tanpa Gemini**:

```
┌─────────────────────────────────────────────────┐
│           FALLBACK STRATEGY                      │
│                                                  │
│  Gemini API Available?                           │
│        │                                         │
│   ┌────┴────┐                                    │
│   │  YES    │  → Full experience:                │
│   │         │    ML result + Gemini insight       │
│   │         │    + Chatbot aktif                  │
│   └─────────┘                                    │
│   ┌─────────┐                                    │
│   │  NO     │  → Degraded (masih fungsional):    │
│   │         │    ML result + template saran       │
│   │         │    + Chatbot disabled (tampil pesan)│
│   └─────────┘                                    │
└─────────────────────────────────────────────────┘
```

| Fitur | Gemini Available ✅ | Gemini Down ❌ |
|---|---|---|
| Mode 1: Verdict (✅/⚠️/❌) | ✅ Berjalan (rule-based) | ✅ Berjalan (rule-based) |
| Mode 1: Natural Language Insight | ✅ Gemini-generated | ⚠️ Fallback ke template statis |
| Mode 2: Ranking List | ✅ Berjalan (KNN model) | ✅ Berjalan (KNN model) |
| Mode 2: Summarization | ✅ Gemini-generated | ⚠️ Tidak ada ringkasan |
| Mode 3: Chatbot | ✅ Aktif | ❌ Disabled (pesan: "Chatbot sedang tidak tersedia") |

---

## 15. Catatan untuk Tim Mobile App

> **Penting:** AI Engine menggunakan arsitektur **hybrid**:
> - **ML model (KNN)** bisa di-deploy **on-device** (convert ke TFLite/ONNX) untuk offline support
> - **Gemini API** wajib **online** — membutuhkan koneksi internet
> 
> **Rekomendasi untuk MVP:** Gunakan pendekatan **full API-based** (semua di server), lalu migrasikan ML model ke on-device di versi final untuk offline fallback.

> **Catatan Keamanan:**
> - **JANGAN** embed `GEMINI_API_KEY` langsung di kode mobile app
> - Gemini API harus dipanggil **melalui backend** (FastAPI), bukan langsung dari app
> - Tambahkan rate limiting per user di backend untuk mencegah abuse
