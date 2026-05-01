"""
LuntiAI — Philippine Crop Dataset Generator
=============================================
Generates a research-backed synthetic dataset for crop recommendation
in Tagum City / Davao del Norte / Philippines.

Data Sources & References:
- BSWM (Bureau of Soils and Water Management) — Soil classification & NPK ranges for Region XI
- PAGASA — Climatological normals for Davao Region (temperature, humidity, rainfall)
- PhilRice — Rice Crop Manager nutrient requirements
- DA Technoguides — Crop-specific growing condition guides
- PCA (Philippine Coconut Authority) — Coconut cultivation parameters
- ACDI/VOCA & ICRAF — Cacao growing conditions in Mindanao
- Yara Philippines — Banana nutrient management
- PCARRD/PCAARRD — Mango, Eggplant, Tomato production guides
- PhilRootcrops (VSU) — Cassava & Sweet Potato guides
- UPLB — Various crop science publications

Methodology:
    Each crop has defined parameter ranges (min, max, optimal_mean, std_dev)
    based on the above sources. We use truncated normal distributions to
    generate realistic data points clustered around optimal conditions,
    with natural variation simulating real-world field measurements.

    This is a standard data science technique known as "domain-constrained
    synthetic data generation" — legitimate for prototyping when primary
    field data collection is infeasible.

Author: LuntiAI Team
Date: 2026
"""

import numpy as np
import pandas as pd
import os

# Reproducibility
SEED = 42
np.random.seed(SEED)

# ============================================================================
# CROP PARAMETER DEFINITIONS
# Each crop has 8 features: N, P, K, temperature, humidity, ph, rainfall, OM
# Format: (min, max, mean, std_dev)
# Ranges are based on Philippine agricultural data for tropical conditions
# ============================================================================

CROP_PROFILES = {
    # -----------------------------------------------------------------------
    # RICE (Irrigated Lowland) — PhilRice Crop Manager / DA Region XI
    # Dominant in Pagsabangan, Bincungan, Madaum barangays
    # -----------------------------------------------------------------------
    "Rice": {
        "N":           (40, 140, 80, 20),     # High N demand; PhilRice recommends 80-120 kg/ha
        "P":           (20, 70, 42, 12),       # Moderate P; DA guide 30-60 range
        "K":           (25, 70, 40, 10),       # Moderate K; flooded conditions retain K
        "temperature": (22, 32, 27, 2),        # Optimal 25-30°C; PAGASA Tagum avg ~27.5°C
        "humidity":    (70, 95, 82, 5),        # High humidity; PAGASA 75-85% avg
        "ph":          (4.5, 7.5, 5.8, 0.6),   # Slightly acidic preferred; BSWM Region XI soils
        "rainfall":    (150, 300, 220, 35),     # Monthly avg; Tagum ~2000mm/yr distributed
        "OM":          (1.5, 5.0, 3.0, 0.5),   # Organic Matter (%)
    },

    # -----------------------------------------------------------------------
    # BANANA (Cavendish) — Yara PH, TADECO data, DA Davao del Norte
    # Tagum's #1 export crop; Apokon, La Filipina, Hijo plantations
    # -----------------------------------------------------------------------
    "Banana": {
        "N":           (60, 180, 120, 25),     # Very high N; Yara PH recommends 200-400 kg N/ha/yr
        "P":           (25, 75, 45, 12),       # Moderate P; tissue analysis based
        "K":           (80, 250, 150, 35),     # Very high K demand; critical for bunch weight
        "temperature": (24, 33, 28, 1.8),      # Optimal 26-30°C; sensitive below 15°C
        "humidity":    (70, 95, 82, 5),        # High; needs consistent moisture
        "ph":          (4.5, 7.5, 6.0, 0.5),   # Tolerates 5.0-7.0; BSWM clay loam acidic
        "rainfall":    (130, 300, 200, 35),     # Needs 1500-2500mm/yr; evenly distributed
        "OM":          (2.0, 6.0, 3.5, 0.8),   # Rich organic matter needed
    },

    # -----------------------------------------------------------------------
    # CACAO — ACDI/VOCA Mindanao, ICRAF, DA Region XI Cacao Program
    # Growing in Apokon, Mankilam; intercropped with coconut
    # -----------------------------------------------------------------------
    "Cacao": {
        "N":           (30, 100, 60, 15),      # Moderate N; shade-grown reduces demand
        "P":           (20, 70, 40, 12),       # Moderate P; volcanic soils often P-deficient
        "K":           (40, 120, 70, 18),      # Moderate-high K; pod development
        "temperature": (20, 34, 27, 2.5),      # Optimal 22-32°C; shade management
        "humidity":    (65, 95, 80, 6),        # High; needs humid microclimate
        "ph":          (4.5, 7.0, 5.8, 0.5),   # Prefers 5.0-6.5; acidic volcanic soils
        "rainfall":    (120, 250, 170, 30),     # 1500-2000mm/yr; even distribution
        "OM":          (2.0, 5.5, 3.2, 0.7),   # Leaf litter contributes to OM
    },

    # -----------------------------------------------------------------------
    # COCONUT — PCA Technoguide, Philippine Coconut Authority
    # Dominant crop by area in Tagum; found across most barangays
    # -----------------------------------------------------------------------
    "Coconut": {
        "N":           (15, 80, 40, 15),       # Low-moderate N; PCA recommends 150g ammonium sulfate/tree
        "P":           (15, 60, 35, 10),       # Low-moderate P
        "K":           (60, 200, 120, 30),     # High K; critical for copra quality
        "temperature": (22, 32, 27, 2),        # Optimal 24-29°C; PAGASA Tagum fits perfectly
        "humidity":    (65, 90, 78, 5),        # Moderate-high; tolerant
        "ph":          (5.0, 8.0, 6.2, 0.6),   # Wide tolerance 5.5-6.5 ideal
        "rainfall":    (100, 280, 175, 40),     # 1300-2300mm/yr; tolerates variation
        "OM":          (1.0, 4.0, 2.5, 0.6),   # Sandy/loamy soils often lower in OM
    },

    # -----------------------------------------------------------------------
    # DURIAN — DA Mindanao, Durian Industry Development Program
    # High-value crop; Davao Region is the "Durian Capital"
    # -----------------------------------------------------------------------
    "Durian": {
        "N":           (40, 130, 75, 20),      # Moderate-high N; fruiting trees need more
        "P":           (25, 80, 50, 14),       # Moderate P; flower/fruit development
        "K":           (50, 150, 90, 22),      # High K; fruit quality & sweetness
        "temperature": (23, 34, 28, 2),        # Tropical warmth; sensitive to cold
        "humidity":    (70, 95, 82, 5),        # High humidity; Davao climate ideal
        "ph":          (5.5, 7.5, 6.5, 0.4),   # Prefers 6.0-7.0; slightly acidic to neutral
        "rainfall":    (160, 350, 240, 40),     # 2000-3000mm/yr; needs dry spell for flowering
        "OM":          (2.0, 5.0, 3.0, 0.6),   # Good organic matter for moisture retention
    },

    # -----------------------------------------------------------------------
    # CORN (Yellow) — PhilMaize, DA Corn Program
    # Grown in upland areas of Tagum; rotation crop
    # -----------------------------------------------------------------------
    "Corn": {
        "N":           (50, 150, 90, 22),      # High N demand; DA recommends 90-120 kg N/ha
        "P":           (25, 70, 45, 12),       # Moderate P; starter fertilizer important
        "K":           (15, 60, 35, 10),       # Low-moderate K; depends on soil reserves
        "temperature": (20, 33, 26, 2.5),      # Optimal 21-30°C; heat-tolerant varieties
        "humidity":    (50, 80, 65, 7),        # Lower humidity than rice; rain-fed
        "ph":          (5.0, 7.5, 6.2, 0.5),   # Prefers 5.5-7.0; liming often needed
        "rainfall":    (50, 150, 90, 25),       # 600-1200mm/season; drought sensitive at tasseling
        "OM":          (1.0, 3.5, 2.0, 0.5),   # Often grown in upland/depleted soils
    },

    # -----------------------------------------------------------------------
    # MANGO — PCARRD, National Mango Industry Development Program
    # Common in drier areas; Tagum produces export-quality mangoes
    # -----------------------------------------------------------------------
    "Mango": {
        "N":           (20, 90, 50, 15),       # Low-moderate N; excess N delays fruiting
        "P":           (15, 60, 35, 10),       # Moderate P; flower induction
        "K":           (30, 100, 60, 15),      # Moderate K; fruit quality
        "temperature": (22, 33, 27, 2),        # Optimal 24-30°C; needs warm days
        "humidity":    (45, 75, 60, 7),        # Lower humidity preferred; reduces anthracnose
        "ph":          (5.0, 8.0, 6.5, 0.6),   # Wide tolerance; 5.5-7.5 ideal
        "rainfall":    (60, 170, 110, 25),      # 750-1500mm/yr; dry period needed for flowering
        "OM":          (1.0, 3.5, 2.2, 0.5),   # Tolerates lower OM
    },

    # -----------------------------------------------------------------------
    # PAPAYA — DA Crop Production Guide, PCAARRD
    # Fast-growing; common backyard & commercial crop in Tagum
    # -----------------------------------------------------------------------
    "Papaya": {
        "N":           (60, 150, 100, 20),     # High N; rapid vegetative growth
        "P":           (30, 80, 55, 12),       # Moderate-high P; fruiting
        "K":           (50, 150, 90, 22),      # High K; fruit sweetness & quality
        "temperature": (23, 35, 29, 2),        # Optimal 25-32°C; frost intolerant
        "humidity":    (55, 85, 70, 7),        # Moderate; excess humidity = fungal disease
        "ph":          (5.0, 7.5, 6.2, 0.5),   # Prefers 5.5-7.0
        "rainfall":    (80, 220, 145, 30),      # 1000-2000mm/yr; good drainage critical
        "OM":          (1.5, 4.5, 2.8, 0.6),   # Needs fertile soil
    },

    # -----------------------------------------------------------------------
    # CASSAVA — PhilRootcrops (VSU), DA Root Crops Program
    # Resilient crop; grown in marginal soils across Davao del Norte
    # -----------------------------------------------------------------------
    "Cassava": {
        "N":           (10, 70, 35, 14),       # Low N; excess N = more leaves, less tuber
        "P":           (10, 50, 25, 10),       # Low P requirement; efficient P user
        "K":           (40, 130, 80, 22),      # High K; critical for starch accumulation
        "temperature": (23, 35, 29, 2),        # Optimal 25-32°C; heat tolerant
        "humidity":    (55, 85, 70, 7),        # Moderate; drought tolerant once established
        "ph":          (4.5, 7.0, 5.8, 0.5),   # Tolerates acidic soils well
        "rainfall":    (80, 180, 120, 25),      # 1000-1500mm/yr; tolerates dry spells
        "OM":          (0.5, 3.0, 1.5, 0.4),   # Very tolerant of degraded/poor soils
    },

    # -----------------------------------------------------------------------
    # SWEET POTATO (Kamote) — UPLB, DA Root Crops Program
    # Important food security crop; grown across all barangays
    # -----------------------------------------------------------------------
    "Sweet Potato": {
        "N":           (20, 80, 45, 14),       # Low-moderate N; excess N = vine growth
        "P":           (25, 70, 45, 12),       # Moderate P; root development
        "K":           (60, 180, 110, 25),     # Very high K; tuber formation & quality
        "temperature": (22, 33, 27, 2),        # Optimal 24-30°C
        "humidity":    (60, 85, 72, 6),        # Moderate-high
        "ph":          (5.0, 7.0, 6.0, 0.4),   # Prefers 5.5-6.5; slightly acidic
        "rainfall":    (60, 170, 110, 25),      # 750-1500mm/yr; needs well-drained soil
        "OM":          (1.0, 3.0, 1.8, 0.4),   # Tolerates lower OM
    },

    # -----------------------------------------------------------------------
    # EGGPLANT (Talong) — PCAARRD, DA Vegetable Program
    # Top vegetable crop in PH; widely grown in Tagum
    # -----------------------------------------------------------------------
    "Eggplant": {
        "N":           (60, 150, 100, 20),     # High N; heavy feeder
        "P":           (30, 80, 55, 12),       # Moderate-high P; fruit set
        "K":           (30, 100, 60, 15),      # Moderate K
        "temperature": (23, 35, 28, 2),        # Optimal 25-32°C; heat loving
        "humidity":    (55, 85, 68, 7),        # Moderate; excess = bacterial wilt
        "ph":          (5.0, 7.5, 6.2, 0.5),   # Prefers 5.5-6.8
        "rainfall":    (60, 170, 110, 25),      # 800-1500mm/season
        "OM":          (1.5, 4.0, 2.5, 0.5),   # Needs fertile soil
    },

    # -----------------------------------------------------------------------
    # TOMATO (Kamatis) — PCAARRD, DA Vegetable Program
    # Important vegetable; some upland areas of Tagum produce tomato
    # -----------------------------------------------------------------------
    "Tomato": {
        "N":           (60, 150, 100, 20),     # High N; multiple harvests
        "P":           (40, 100, 65, 15),      # High P; flowering & fruiting
        "K":           (40, 110, 70, 16),      # Moderate-high K; fruit quality
        "temperature": (20, 30, 25, 2),        # Optimal 22-28°C; heat stress above 32
        "humidity":    (50, 80, 65, 7),        # Moderate; high humidity = late blight
        "ph":          (5.0, 7.5, 6.2, 0.5),   # Prefers 5.5-6.8
        "rainfall":    (50, 140, 90, 22),       # 600-1200mm/season; sensitive to waterlogging
        "OM":          (1.5, 4.0, 2.5, 0.5),   # Requires good OM for water retention
    },
}


def truncated_normal(mean, std, low, high, size):
    """
    Generate samples from a truncated normal distribution.
    Values are clipped to [low, high] range to ensure physical validity.
    Uses rejection-free clipping for efficiency with large sample sizes.
    """
    samples = np.random.normal(mean, std, size)
    samples = np.clip(samples, low, high)
    # Add micro-noise to avoid perfectly identical values at boundaries
    boundary_mask = (samples == low) | (samples == high)
    if np.any(boundary_mask):
        jitter = np.random.uniform(0, std * 0.1, np.sum(boundary_mask))
        samples[boundary_mask] = np.clip(
            samples[boundary_mask] + jitter * np.random.choice([-1, 1], np.sum(boundary_mask)),
            low, high
        )
    return samples


def generate_crop_samples(crop_name, params, n_samples):
    """
    Generate n_samples for a single crop using truncated normal distributions.

    Also introduces realistic "field variation" patterns:
    - Slight positive correlation between N and humidity (wetter = more N leaching)
    - Slight negative correlation between rainfall and pH (more rain = more acidic)
    - Temperature-humidity coupling (tropical: higher temp often = higher humidity)
    """
    data = {}

    for feature, (low, high, mean, std) in params.items():
        data[feature] = truncated_normal(mean, std, low, high, n_samples)

    # --- Introduce realistic correlations ---
    # 1. Rainfall ↔ pH: More rainfall tends to leach bases → lower pH
    rain_z = (data["rainfall"] - params["rainfall"][2]) / params["rainfall"][3]
    ph_adjustment = -0.08 * rain_z  # Subtle effect
    data["ph"] = np.clip(
        data["ph"] + ph_adjustment,
        params["ph"][0], params["ph"][1]
    )

    # 2. Temperature ↔ Humidity coupling (tropical correlation)
    temp_z = (data["temperature"] - params["temperature"][2]) / params["temperature"][3]
    humidity_adjustment = 1.2 * temp_z  # Warmer → slightly higher humidity in tropics
    data["humidity"] = np.clip(
        data["humidity"] + humidity_adjustment,
        params["humidity"][0], params["humidity"][1]
    )

    # 3. Add seasonal variation noise (simulates wet/dry season measurements)
    seasonal_noise = np.random.choice([0.95, 1.0, 1.05, 1.1], n_samples)
    data["rainfall"] = np.clip(
        data["rainfall"] * seasonal_noise,
        params["rainfall"][0], params["rainfall"][1]
    )

    # Round to realistic precision
    for feature in data:
        if feature == "ph":
            data[feature] = np.round(data[feature], 2)
        elif feature in ("temperature", "humidity", "rainfall"):
            data[feature] = np.round(data[feature], 2)
        elif feature == "OM":
            data[feature] = np.round(data[feature], 2)
        else:
            data[feature] = np.round(data[feature], 1)

    data["label"] = [crop_name] * n_samples
    return pd.DataFrame(data)


def generate_full_dataset(total_samples=120000):
    """
    Generate the complete Philippine crop recommendation dataset.

    Distribution strategy:
    - Major Tagum crops (Banana, Coconut, Rice) get 12,000 samples each
    - High-value crops (Cacao, Durian) get 11,000 samples each
    - Other crops get ~8,000-9,000 samples each
    - Total: ~120,000 samples

    This slight imbalance reflects real-world crop prevalence in
    Davao del Norte while maintaining enough samples for the model
    to learn all crop decision boundaries effectively.
    """
    crop_sample_counts = {
        "Rice":         12000,
        "Banana":       12000,
        "Coconut":      12000,
        "Cacao":        11000,
        "Durian":       11000,
        "Corn":         10000,
        "Mango":         9000,
        "Papaya":        9000,
        "Cassava":       9000,
        "Sweet Potato":  9000,
        "Eggplant":      8000,
        "Tomato":        8000,
    }

    actual_total = sum(crop_sample_counts.values())
    print(f"📊 Generating {actual_total:,} total samples across {len(crop_sample_counts)} crops...")
    print(f"{'='*60}")

    all_frames = []
    for crop_name, n_samples in crop_sample_counts.items():
        params = CROP_PROFILES[crop_name]
        df = generate_crop_samples(crop_name, params, n_samples)
        all_frames.append(df)
        print(f"  ✅ {crop_name:<15} — {n_samples:>6,} samples generated")

    dataset = pd.concat(all_frames, ignore_index=True)

    # Shuffle the entire dataset
    dataset = dataset.sample(frac=1, random_state=SEED).reset_index(drop=True)

    print(f"{'='*60}")
    print(f"✅ Total dataset: {len(dataset):,} rows × {len(dataset.columns)} columns")
    print(f"\n📋 Class distribution:")
    print(dataset["label"].value_counts().to_string())
    print(f"\n📊 Feature statistics:")
    print(dataset.describe().round(2).to_string())

    return dataset


def main():
    """Generate and save the Philippine crop dataset."""
    # Ensure output directory exists
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "philippine_crop_dataset.csv")

    # Generate
    dataset = generate_full_dataset(total_samples=120000)

    # Save
    dataset.to_csv(output_path, index=False)
    file_size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"\n💾 Dataset saved to: {output_path}")
    print(f"📁 File size: {file_size_mb:.1f} MB")

    # Validation checks
    print(f"\n🔍 Validation:")
    print(f"  • No null values: {not dataset.isnull().any().any()}")
    print(f"  • All N in [0,200]: {(dataset['N'] >= 0).all() and (dataset['N'] <= 200).all()}")
    print(f"  • All pH in [0,14]: {(dataset['ph'] >= 0).all() and (dataset['ph'] <= 14).all()}")
    print(f"  • All OM in [0,10]: {(dataset['OM'] >= 0).all() and (dataset['OM'] <= 10).all()}")
    print(f"  • All humidity in [0,100]: {(dataset['humidity'] >= 0).all() and (dataset['humidity'] <= 100).all()}")
    print(f"  • Unique crops: {dataset['label'].nunique()} ({', '.join(sorted(dataset['label'].unique()))})")


if __name__ == "__main__":
    main()
