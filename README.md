# LuntiAI — Precision Agriculture for Tagum City

> AI-powered crop recommendation system for farmers in Tagum City, Davao del Norte.
> Built for the Technopreneurship Academic Festival 2026.

## What is LuntiAI?

**LuntiAI** (*Luntian* + AI) is a web-based precision agriculture platform
that helps Filipino farmers make data-driven crop decisions. Simply select your
barangay, and our AI model recommends the best crop to plant based on your local
soil profile and live weather conditions.

### Key Features
- **23 Tagum Barangay Profiles** — Pre-mapped soil data (NPK, OM, pH, soil type)
- **Live Weather Integration** — Real-time temperature, humidity via OpenWeatherMap
- **Random Forest ML Model** — 85.62% accuracy, trained on 120,000+ data points
- **12 Philippine Crops** — Rice, Banana, Cacao, Coconut, Durian, Corn, Mango, Papaya, Cassava, Sweet Potato, Eggplant, Tomato
- **Explainable AI (SHAP)** — Understand *why* the AI chose a crop with positive/negative impact factors
- **UI Localization** — Supports English, Tagalog, and Bisaya
- **Fertilizer Advice & ROI** — Localized product recommendations and realistic Business ROI Calculator
- **Confidence Scoring** — Top-5 crop predictions with probability chart

---

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate Dataset (Optional — already included)
```bash
python data/generate_dataset.py
```

### 3. Train Model (Optional — already included)
```bash
python train_model.py
```

### 4. Run the Server
```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Open the App
- **Frontend:** http://localhost:8000/app
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## Project Structure

```
crop-random-forest-model/
├── api/
│   ├── main.py              # FastAPI backend server
│   ├── barangay_data.py      # 23 Tagum barangay soil profiles
│   └── weather_service.py    # OpenWeatherMap + PAGASA integration
├── data/
│   ├── generate_dataset.py   # Dataset generation script
│   ├── philippine_crop_dataset.csv  # 120,000-row training data
│   └── sources.md            # Data source citations
├── frontend/
│   ├── index.html            # Premium dark-mode UI
│   ├── styles.css            # Design system
│   ├── app.js                # Frontend logic
│   └── logo.png              # LuntiAI product logo
├── model/
│   ├── crop_model.pkl        # Trained Random Forest model
│   ├── label_encoder.pkl     # Label encoder
│   └── model_metadata.json   # Model performance metrics
├── pitch/
│   └── README.md             # Complete pitch materials
├── train_model.py            # Model training pipeline
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
└── README.md                 # This file
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/predict` | Predict optimal crop from soil & climate data |
| GET | `/barangays` | List all 23 barangay soil profiles |
| GET | `/weather/{name}` | Live weather for a barangay |
| GET | `/health` | System health check |
| GET | `/docs` | Interactive Swagger documentation |

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| ML Model | scikit-learn Random Forest (200 trees) |
| Backend | FastAPI + Uvicorn |
| Frontend | HTML5 / CSS3 / Vanilla JS + Chart.js |
| Weather API | OpenWeatherMap (free tier) |
| Data Sources | BSWM, PAGASA, PhilRice, DA, PCA |

---

## Model Performance

- **Accuracy:** 85.62%
- **Top Features:** Potassium (K), Nitrogen (N), Rainfall, Organic Matter (OM)
- **Training Data:** 120,000 samples across 12 Philippine crops (8 features)
- **Methodology:** Domain-constrained synthetic data from BSWM/PAGASA/DA sources

---

## Team

**LuntiAI Team** — University of Mindanao, Tagum City
Technopreneurship Course — Academic Festival 2026

---

## License

This project is for academic purposes. All agricultural data ranges are derived
from publicly available Philippine government sources (BSWM, PAGASA, DA, PhilRice, PCA).
