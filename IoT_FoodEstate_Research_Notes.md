# IoT for Food Estate — Research Discussion Notes
**Universitas Komputer Indonesia (UNIKOM) — Informatics Engineering**
**Date:** June 29, 2026
**Team Scope:** IoT Hardware + AI & Mobile App (separate sub-teams)

---

## 1. Idea Overview

A handheld IoT soil probe for home-based food cultivation (P2L), targeting non-technical general public. The system measures key soil parameters, interprets data via AI, and displays results on the device itself (OLED screen with smiley-face health indicators) and eventually on a mobile app.

**Product Analogy:** Like a digital thermometer — insert into soil for 10–30 seconds, read result, remove. Not a permanently deployed sensor.

---

## 2. Context: Food Estate → P2L

### National Food Estate
- Large-scale government program for national food self-sufficiency
- Revived in 2020 under President Jokowi post-COVID
- Key locations: Central Kalimantan, North Sumatra (Humbang Hasundutan), Papua
- Structural limitations: land conflicts, long supply chains, benefits concentrated in production zones

### Pekarangan Pangan Lestari (P2L)
- Household-level food cultivation program by Badan Pangan Nasional
- Evolution: KRPL (2016) → P2L (2020)
- Target: 3,600+ community groups across 34 provinces
- Focus: vegetables, fruits, medicinal plants, spices
- Beneficiaries: women's farmer groups (KWT), urban families
- Goals: household food availability, reduced food expenditure, improved nutrition, supplemental income

---

## 3. Key Problems in P2L Adoption (Literature-Based)

> ⚠️ **Note:** Citations below are indicative. Verify each reference independently via Google Scholar, Garuda (garuda.kemdikbud.go.id), or Sinta (sinta.kemdikbud.go.id) before using in academic submission.

| # | Problem | Description | Suggested Search Terms |
|---|---|---|---|
| 01 | Knowledge Deficit | Communities lack knowledge in soil preparation, fertilization, and cultivation techniques | "KRPL implementasi kendala", "P2L pengetahuan masyarakat" |
| 02 | No Real-Time Soil Feedback | Without soil data, growers make uninformed decisions leading to preventable crop failure | "monitoring tanah IoT", "soil monitoring ESP32" |
| 03 | Over-Reliance on Extension Workers | P2L success depends on penyuluh intensity, which is scarce in urban areas | "evaluasi P2L penyuluh", "P2L urban hambatan" |
| 04 | Low Motivation & Sustainability | Participation drops when plants fail without clear cause | "keberlanjutan P2L", "KRPL evaluasi keberhasilan" |

**Recommended databases for verification:**
- Google Scholar: `scholar.google.com`
- Garuda: `garuda.kemdikbud.go.id`
- Sinta: `sinta.kemdikbud.go.id`
- IEEE Xplore: `ieeexplore.ieee.org`

---

## 4. Existing IoT Solutions & Gaps

| System | Parameters | AI Support | Home-User Ready | Price Range | Gap |
|---|---|---|---|---|---|
| Academic IoT Prototypes (local) | Moisture, Temp | None | Partial | Low (DIY) | No recommendation layer |
| CropX / Precision Ag (commercial) | NPK, pH, Moisture, Temp, EC | Yes (ML) | No | High (USD 500–2000+) | Not affordable/accessible |
| Xiaomi Mi Flora / Consumer | Light, Moisture, Temp | Basic | Yes (indoor only) | Medium (USD 30–80) | Not for food crops/outdoor soil |
| **This Research (Proposed)** | pH, Moisture, Temp | Yes (AI engine) | Yes — core objective | Target: Low-Medium | Fills all gaps above |

---

## 5. Soil Health Parameters (MVP Scope)

Parameters selected for MVP — NPK excluded to maintain compact form factor and affordability.

| Parameter | Ideal Range (Vegetables) | Why It Matters | Risk if Unmonitored |
|---|---|---|---|
| **pH** | 6.0 – 7.0 | Controls nutrient availability; wrong pH locks out nutrients even with fertilizer | Stunted growth, yellowing leaves |
| **Soil Moisture** | 40 – 70% (crop-dependent) | Too dry = wilting; too wet = root rot | Most common cause of plant death in home gardens |
| **Soil Temperature** | 18 – 30°C (tropical vegetables) | Affects microbial activity, germination, root development | Cold soil slows growth; hot soil accelerates moisture loss |

> **NPK Note:** Excluded from MVP due to sensor size, cost (Rp 350K–800K), and form factor constraints. Recommended for V2.

---

## 6. Product Concept: Handheld Soil Probe

### Form Factor
- Compact stick/pen device (~15–18cm tall, ~3cm wide)
- Upper half: plastic body with OLED display + button
- Lower half: probe tip with sensor electrodes for soil insertion
- Similar to: digital thermometer, pen-style pH meter

### Usage Flow
```
Insert probe into soil
        ↓
Hold for 10–30 seconds
        ↓
Remove & read OLED display
        ↓
Icon shows soil status + parameter values
        ↓
(V2) Sync via Bluetooth to mobile app
        ↓
AI provides detailed recommendations + history
```

### Display Design (OLED 0.96")
Three-level status system:

| Condition | Icon | Color Indicator |
|---|---|---|
| All parameters in ideal range | 😊 TANAH SEHAT | Green |
| 1–2 parameters slightly off | 😐 PERLU PERHATIAN | Yellow |
| Critical parameter out of range | 😟 BUTUH TINDAKAN | Red |

Sample OLED layout:
```
┌─────────────────┐
│   SOIL CHECK    │
│                 │
│      😊         │
│   TANAH SEHAT   │
│                 │
│ pH: 6.5  💧:60% │
│ Suhu: 27°C      │
└─────────────────┘
```

---

## 7. Bill of Materials (BOM)

### IoT Components (Sensing & Processing)

| # | Component | Function | Measures | Est. Price (IDR) | Status |
|---|---|---|---|---|---|
| 1 | Soil pH Sensor (analog) + DMS | Measures soil acidity/alkalinity with signal conditioning | pH | Rp 300,000 | 🔍 Identified |
| 2 | Capacitive Moisture Sensor | Volumetric water content (capacitive, corrosion-resistant) | Moisture | Rp 15K–40K | ✅ Already owned |
| 3 | DS18B20 Waterproof Temp Sensor | Root zone temperature | Temperature | Rp 15K–35K | 🔍 To be sourced |
| 4 | ESP32-S3 DevKitC-1 N16R8 (Prototype) | Data acquisition, processing, WiFi | — (controller) | Rp 80K–150K | 🔍 To be sourced |
| 5 | OLED Display 0.96" | Display soil status icon + parameter values | — (display) | Rp 25K–60K | 🔍 To be sourced |

### Supporting Components (Non-IoT)

| # | Component | Function | Est. Price (IDR) | Status |
|---|---|---|---|---|
| 6 | Baterai 18650 (1x) + Holder | Portable power supply | Rp 20K–50K | 🔍 To be sourced |
| 7 | Enclosure Handheld (splash-proof) | Housing for outdoor use | Rp 25K–75K | 🔍 To be sourced |

### Cost Estimate Summary

| Scenario | Est. Total |
|---|---|
| MVP (pH + Moisture + Temp, prototype board) | Rp 480K – 710K |
| MVP with XIAO ESP32-C3 (compact, final form) | Rp 400K – 620K |

> Prices based on estimated Indonesian marketplace range (Tokopedia/Shopee). Verify before finalizing BOM.

---

## 8. Component Notes & Decisions

### pH Sensor
- **Selected:** Soil pH Sensor (analog) + DMS — Rp 300,000
- **Why:** Specifically designed for soil (not liquid), includes DMS signal conditioning for stable readings, explicitly supports ESP32, includes datasheet + calibration formula
- **Rejected options:**
  - PH-4502C (5V liquid probe — wrong application, voltage incompatibility)
  - Industrial CWT PH-V5 (technically correct but Rp 690K, no reviews)
- **Action required:** Confirm analog output max voltage with seller before purchase. If >3.3V, add voltage divider (2 resistors, <Rp 5K)

### Moisture Sensor
- **Type:** Capacitive (not resistive)
- **Why capacitive:** No exposed metal, corrosion-resistant, stable readings long-term
- **Avoid:** Resistive sensors (metal probes corrode within months even if marketed as "anti-rust")

### Microcontroller Strategy
- **For prototype/MVP:** ESP32-S3 DevKitC-1 — easier to wire, more pins, abundant tutorials
- **For final compact version:** Seeed Studio XIAO ESP32-C3 (21x17.5mm, fits handheld form factor)
- **Decision:** Use DevKitC-1 first, migrate to XIAO after code is stable

### Battery
- **Selected:** 1x 18650 + single holder
- **Why single cell:** Device only active 10–30 seconds per measurement session — single 18650 (~2500mAh) provides hundreds of measurement sessions before recharge
- **No solar panel needed** — not a permanently deployed sensor

### NPK Sensor (Deferred)
- Excluded from MVP due to: large probe size, high cost (Rp 350K–800K), form factor constraints
- Recommended for V2 roadmap

---

## 9. Marketplace Search Keywords

| Component | Search Keywords |
|---|---|
| pH Sensor (soil) | `sensor pH tanah arduino`, `soil pH sensor ESP32 DMS` |
| Capacitive Moisture | `capacitive soil moisture sensor v1.2`, `sensor kelembaban tanah kapasitif` |
| DS18B20 | `DS18B20 waterproof sensor suhu`, `sensor suhu tanah DS18B20` |
| ESP32-S3 DevKitC | `ESP32-S3 DevKitC-1 N16R8`, `ESP32 S3 development board type-c` |
| XIAO ESP32-C3 | `Seeed XIAO ESP32-C3`, `XIAO ESP32C3 seeedstudio` |
| OLED 0.96" | `OLED display 0.96 inch I2C arduino`, `layar OLED 0.96 arduino` |
| 18650 Battery | `baterai 18650 2500mAh`, `battery 18650 flat top` |
| 18650 Holder (1x) | `holder baterai 18650 single 1 slot`, `battery holder 18650 1x dengan kabel` |
| Enclosure | `box project plastik handheld`, `enclosure plastik tahan cipratan` |

---

## 10. System Architecture (Conceptual)

```
[Soil Sensors]         [Controller]        [Display]
pH Sensor       ──┐
Moisture Sensor ──┼──► ESP32-S3 ──────────► OLED 0.96"
DS18B20 Temp    ──┘    │                    (icon + values)
                       │
                       ▼ (V2 Roadmap)
                  [Bluetooth]
                       │
                       ▼
                  [Mobile App]
                       │
                       ▼
                  [AI Engine]
                  (Recommendations)
```

### Scope Split
- **This team (IoT):** Sensors + ESP32 + OLED display + local interpretation logic
- **Other team:** AI engine + Mobile App + Bluetooth integration

---

## 11. Presentation Structure (Gamma Prompt Ready)

Slide flow agreed for progress report:

1. Title Slide
2. Food Estate — National Context
3. Transition: Why National Is Not Enough
4. P2L Explanation
5. Key Problems in P2L Adoption (evidence-based)
6. Existing IoT Solutions
7. Comparison Table
8. Soil Health Parameters (with transition from comparison)
9. IoT Components & Estimated Cost (MVP without NPK)

---

## 12. Open Questions / Next Steps

- [ ] Confirm pH sensor output voltage with seller before purchase
- [ ] Source DS18B20, OLED, ESP32-S3 DevKitC-1
- [ ] Verify all literature citations via Garuda/Sinta/Google Scholar
- [ ] Decide enclosure form factor (dimensions based on component layout)
- [ ] Test sensor readings and calibration after components arrive
- [ ] Define threshold values per parameter for smiley-face logic (😊/😐/😟)
- [ ] Coordinate with AI/Mobile App team on data format and Bluetooth protocol

---

## 13. AI & Mobile App Integration Strategy

Sistem IoT yang dikembangkan dirancang sebagai *probe handheld* genggam yang mengukur parameter tanah (pH, Kelembapan, Suhu) selama 10–30 detik[cite: 1]. Untuk menjaga efisiensi alat fisik, pemrosesan analitik tingkat lanjut (AI) dipisahkan dan dieksekusi pada aplikasi *mobile*[cite: 1]. 

Layar OLED pada perangkat fisik tetap dipertahankan untuk menampilkan nilai parameter mentah secara instan. Awalnya direncanakan menggunakan indikator kesehatan tanah statis, namun sistem telah berevolusi menjadi **Komunikasi Dua Arah (Two-way Communication)**[cite: 1]:
1. **ESP32 ke HP (TX):** Mengirimkan data mentah (Suhu, Kelembapan, pH).
2. **HP ke ESP32 (RX):** Jika pengguna memilih tanaman tertentu di aplikasi (misal: Tomat), aplikasi akan mengirimkan batas bawah dan batas atas (threshold) untuk tanaman tersebut ke ESP32.
3. **Layar OLED Dinamis:** ESP32 akan menggunakan threshold baru ini untuk menampilkan ikon *smiley* (😊/😐/😟) yang sudah disesuaikan *khusus* untuk Tomat secara *real-time*.

---

## 14. AI Mode 1: *Plant-First* (Validasi Kesesuaian Lahan)

Metode ini dirancang untuk pengguna yang sudah memiliki target atau niat untuk menanam bibit spesifik, yang sejalan dengan fokus target komoditas P2L seperti sayuran, buah, atau tanaman obat[cite: 1].

*   **Alur Pengguna:** 
    1. Pengguna memilih target tanaman di aplikasi (misalnya: "Tomat").
    2. Pengguna menancapkan *probe* IoT ke tanah[cite: 1].
    3. Aplikasi menerima pembacaan sensor secara *real-time*[cite: 1].
*   **Logika AI (*Evaluator*):** 
    Algoritma mengevaluasi selisih antara data sensor aktual (Suhu, Kelembapan, pH) dengan rentang ideal dari tanaman yang dipilih[cite: 1].
*   **Output Aplikasi (*Actionable Insight*):** 
    AI tidak sekadar menampilkan angka, melainkan memberikan instruksi perbaikan. Hal ini dirancang untuk menyelesaikan permasalahan **Knowledge Deficit** (masyarakat yang kurang pengetahuan dalam persiapan tanah)[cite: 1]. 
    *   *Contoh:* "Tanah tidak ideal untuk Tomat karena pH terlalu asam (5.5). Saran: Taburkan kapur dolomit untuk menaikkan pH ke angka 6.5 sebelum memulai penanaman."

---

## 15. AI Mode 2: *Soil-First* (Sistem Rekomendasi Tanaman)

Metode ini dirancang untuk pengguna awam yang memiliki lahan kosong, namun tidak mengetahui jenis tanaman apa yang paling sesuai, guna mencegah kegagalan panen yang dapat menurunkan motivasi masyarakat[cite: 1].

*   **Alur Pengguna:**
    1. Pengguna menancapkan *probe* ke lahan secara langsung tanpa memilih tanaman[cite: 1].
    2. Alat mengekstrak parameter tanah dan mengirimkannya ke aplikasi.
    3. Aplikasi memunculkan daftar rekomendasi tanaman yang paling cocok.
*   **Logika AI (*Recommender System*):** 
    AI bertindak sebagai mesin pencari kecocokan (*matching engine*). Algoritma (misalnya KNN atau *Decision Tree*) akan mengambil nilai sensor saat ini dan memindai seluruh *dataset* tanaman agrikultur untuk menemukan kecocokan lingkungan tertinggi.
*   **Output Aplikasi (*Ranking List*):** 
    Menampilkan daftar tanaman berdasarkan probabilitas keberhasilan tumbuh tanpa perlu memodifikasi unsur hara tanah secara drastis. 
    *   *Contoh:* "Tanah Anda saat ini sangat cocok untuk: 1. Singkong (98%), 2. Terong (85%), 3. Cabai (75%)."

---

## 16. Pembaruan Arsitektur Sistem (System Architecture Update)

Pemisahan peran (*Scope Split*) antara tim *Hardware* dan tim *Mobile App*[cite: 1]:

```
[Alat IoT Handheld]                         [Aplikasi Mobile & AI]
Sensor (pH, Kelembapan, Suhu) ──┐
                                ├──► ESP32 ──(Bluetooth)──► Mobile App
Layar OLED (Indikator Cepat) ◄──┘                           │
                                                            ├──► AI Mode 1: Validasi Tanaman Target
                                                            └──► AI Mode 2: Rekomendasi Tanaman Otomatis
```
