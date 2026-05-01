# 🌱 LuntiAI — Pitch Materials
## Precision Agriculture for Tagum City, Davao del Norte

> *Prepared for the Technopreneurship Academic Festival 2026*

---

## 1. Statement of the Problem

### Problem 1: The Information Gap
Smallholder farmers in Tagum City and Davao del Norte lack access to **localized,
data-driven crop recommendations**. Most farming decisions are based on tradition,
guesswork, or outdated advice, leading to **crop-soil mismatches** that cause
estimated **20–30% yield losses** annually.

### Problem 2: The Accessibility Barrier
Professional soil testing through laboratory analysis costs **₱500–₱2,000 per sample**
and takes **2–4 weeks** for results. Precision agriculture tools designed for
large-scale commercial farms are too expensive and technical for the average
Filipino farmer managing 1–3 hectares.

### Problem 3: Climate Vulnerability
Unpredictable weather patterns driven by climate change (El Niño/La Niña cycles)
make traditional farming calendars obsolete. Farmers have no tool to correlate
**real-time weather conditions** with optimal crop selection, increasing the risk
of crop failure and financial loss.

---

## 2. Objectives

### General Objective
To develop **LuntiAI**, a mobile-first, AI-driven precision agriculture platform
that democratizes data-driven crop recommendation for smallholder farmers in
Tagum City and Davao del Norte.

### Specific Objectives
1. To create a **localized machine learning model** trained on Philippine soil and
   climate data that recommends optimal crops from 12 locally-relevant varieties
2. To integrate **real-time weather data** (OpenWeatherMap / PAGASA) to automate
   climate parameter inputs, reducing user friction for farmers
3. To provide **barangay-level soil profiles** for all 23 barangays of Tagum City,
   eliminating the need for expensive laboratory soil testing for basic decisions
4. To deliver **actionable fertilizer recommendations** with locally-available
   brands and stores, bridging the gap from "what to plant" to "how to grow it"
5. To achieve a model accuracy of **≥80%** validated through cross-validation on
   120,000+ synthetic data points based on Philippine agricultural research

---

## 3. Solution

### What is LuntiAI?
**LuntiAI** (from Filipino *"Luntian"* meaning green + AI) is a web-based precision
agriculture platform that helps farmers in Tagum City make data-driven crop
decisions.

### How It Works (3-Step Process)

1. **📍 Select Your Barangay**
   The farmer selects their barangay from a dropdown. The system automatically
   retrieves the pre-mapped soil profile (N, P, K, pH, soil type) and fetches
   live weather data.

2. **🤖 AI Analyzes the Data**
   Our Random Forest machine learning model — trained on 120,000+ data points
   based on Philippine agricultural research — processes the soil and climate
   inputs to predict the optimal crop.

3. **🌾 Get Actionable Recommendations**
   The farmer receives:
   - The **best crop** with confidence percentage
   - **Top 5 alternative crops** ranked by suitability
   - **Fertilizer advice** with specific products available at Tagum agrivet stores

### Key Innovation
Unlike generic crop calculators, LuntiAI **eliminates manual data entry**.
A farmer who doesn't know their exact soil pH or annual rainfall can still get
an accurate recommendation — we do the heavy lifting by pre-mapping 23 barangays
and integrating live weather APIs.

### Tech Stack
| Component | Technology |
|-----------|-----------|
| ML Model | Random Forest (scikit-learn) — 200 estimators, 82.93% accuracy |
| Dataset | 120,000 rows, 12 crops, 7 features — domain-constrained synthetic data |
| Backend | FastAPI (Python) — RESTful API with Swagger documentation |
| Frontend | HTML/CSS/JavaScript — Dark-mode premium UI, glassmorphism design |
| Weather | OpenWeatherMap API — Real-time temperature, humidity, conditions |
| Data Sources | BSWM, PAGASA, PhilRice, DA Technoguides, PCA |

---

## 4. Target User (Persona)

### 👨‍🌾 "Mang Kiko" — The Pragmatic Farmer

| Attribute | Detail |
|-----------|--------|
| **Name** | Ricardo "Kiko" Dela Cruz |
| **Age** | 48 years old |
| **Location** | Pagsabangan, Tagum City |
| **Occupation** | Smallholder farmer — 2-hectare family farm |
| **Education** | High school graduate |
| **Devices** | Android smartphone (budget model) |
| **Income** | ₱15,000–₱25,000/month (farming income) |
| **Family** | Married with 3 children |

### Empathy Map

| Category | Details |
|----------|---------|
| **Says** | "Mahirap mag-decide kung ano ang itanim ngayon kasi iba na ang panahon." |
| **Thinks** | "Gusto ko ma-maximize ang harvest ko pero wala akong access sa technology." |
| **Does** | Uses Facebook heavily. Asks neighbors what they are planting. Visits the DA office for subsidized seeds. Goes to the Tagum Public Market every Sunday. |
| **Feels** | Anxious about recouping seed and fertilizer investments. Frustrated that weather is unpredictable. Hopeful about new technology but intimidated by complex apps. |

### Pain Points
1. Cannot afford laboratory soil testing (₱500+/sample)
2. Fertilizer prices are rising — needs to optimize application
3. Climate change is making traditional planting calendars unreliable
4. Most agriculture apps are in English and designed for commercial farms

### What Mang Kiko Needs
- A **simple, one-step tool** that doesn't require technical knowledge
- **Tagalog/Bisaya-friendly** interface (future localization)
- Recommendations that mention **specific products** he can buy locally
- Data he can **show to his cooperative** to justify crop decisions

---

## 5. TAM / SAM / SOM

### Methodology: Top-Down Market Sizing

```
┌──────────────────────────────────────────────────┐
│                                                  │
│               TAM: ₱1.2 Billion                  │
│          2.4M Filipino farmers × ₱500/yr         │
│                                                  │
│       ┌──────────────────────────────┐           │
│       │                              │           │
│       │      SAM: ₱75 Million        │           │
│       │  150K Region XI farmers      │           │
│       │                              │           │
│       │    ┌──────────────────┐      │           │
│       │    │                  │      │           │
│       │    │  SOM: ₱500,000  │      │           │
│       │    │  1,000 farmers   │      │           │
│       │    │  Year 1 target  │      │           │
│       │    └──────────────────┘      │           │
│       └──────────────────────────────┘           │
└──────────────────────────────────────────────────┘
```

### TAM (Total Addressable Market) — ₱1.2 Billion/year
- **2.4 million** registered farmers in the Philippines (RSBSA 2024)
- Premium subscription model: **₱500/year** per farmer
- TAM = 2,400,000 × ₱500 = **₱1,200,000,000**

### SAM (Serviceable Available Market) — ₱75 Million/year
- Focus: **Davao Region (Region XI)** — the agricultural hub of Mindanao
- ~**150,000** registered farmers in Region XI
- SAM = 150,000 × ₱500 = **₱75,000,000**

### SOM (Serviceable Obtainable Market) — ₱500,000 ARR (Year 1)
- Beachhead market: **Tagum City + Davao del Norte**
- ~10,000 farmers in immediate target area
- Realistic Year 1 capture: **10%** = 1,000 farmers
- SOM = 1,000 × ₱500 = **₱500,000 ARR**

---

## 6. Revenue Model

| Stream | Description | Pricing |
|--------|------------|---------|
| **Freemium App** | Basic crop recommendation (3 queries/day) | Free |
| **Premium** | Unlimited queries, historical tracking, fertilizer price alerts | ₱500/year |
| **B2B: Fertilizer Companies** | Anonymized soil data insights per barangay | ₱50,000/quarter |
| **B2G: City Agriculture Office** | Dashboard of city-wide soil health & crop trends | ₱100,000/year |
| **IoT Integration** (Future) | Soil sensor hardware + data subscription | ₱2,500/sensor + ₱200/month |

---

## 7. Competitive Advantage

| Feature | LuntiAI | Generic Crop Apps | Lab Testing |
|---------|---------|-------------------|-------------|
| Cost to farmer | Free / ₱500/yr | Free | ₱500–2,000/test |
| Speed | Instant | Instant | 2–4 weeks |
| Localization | 23 Tagum barangays | Generic/Global | N/A |
| Weather integration | Live API | None | None |
| Fertilizer advice | Local brands & stores | Generic | Lab report only |
| Accessibility | Mobile web, 1-step | Complex forms | Physical lab visit |
| Explainability | Feature importance via AI | Black box | N/A |

---

## 8. Data Methodology (For Judges Who Ask)

> "We started with a **domain-constrained synthetic data generation** approach —
> a standard technique in data science when primary field data collection is
> infeasible. Our 120,000-row dataset is built using validated parameter ranges
> from **BSWM soil profiles**, **PAGASA climate normals**, **PhilRice crop manager
> data**, and **DA Region XI technoguides**. Each crop's NPK, pH, temperature,
> humidity, and rainfall ranges are sourced from these authoritative Philippine
> institutions. We then use truncated normal distributions with realistic
> correlations to generate training data."

> "Our next phase involves **field validation** — partnering with USeP Tagum-Mabini
> College of Agriculture and the Tagum City Agriculturist to collect actual soil
> samples and ground-truth our model against real field performance."

---

## 9. Roadmap

| Phase | Timeline | Milestone |
|-------|----------|-----------|
| MVP Launch | Q2 2026 | Web app live, 12 crops, 23 barangays |
| Field Validation | Q3 2026 | Partner with USeP, collect 500 real soil samples |
| Mobile App | Q4 2026 | Native Android app (offline-capable) |
| Localization | Q1 2027 | Bisaya and Tagalog language support |
| IoT Sensors | Q2 2027 | NPK soil sensor integration pilot |
| Expansion | Q3 2027 | Scale to all Davao del Norte municipalities |

---

*LuntiAI Team — Technopreneurship Academic Festival 2026*
*University of Mindanao — Tagum City*
