"""
LuntiAI — Barangay Soil Data
==============================
Hardcoded average soil profiles for Tagum City's 23 barangays.

Sources:
- BSWM Region XI soil classification data (Inceptisols/Alfisols/Ultisols)
- Tagum City Agriculture Office commodity profiles
- DA Region XI soil fertility assessment reports
- PAGASA climate normals for Davao del Norte

These are representative averages. Actual soil conditions vary by
specific plot, elevation, drainage, and land-use history.
"""

# Tagum City coordinates (center)
TAGUM_COORDS = {"lat": 7.4478, "lon": 125.8094}

# Barangay-level soil profiles
# N, P, K in mg/kg (ppm); pH unitless; soil_type from BSWM classification
TAGUM_BARANGAYS = {
    # OM values sourced from BSWM Region XI soil classification & PH soil fertility surveys
    # Alluvial/clay loam agricultural zones: 2.5–4.0%
    # Upland/sandy/Ultisol zones: 1.2–2.2%
    # Urban/peri-urban degraded soils: 1.5–2.5%
    # Plantation zones (banana/cacao) with organic inputs: 3.0–4.5%
    "Apokon": {
        "N": 65, "P": 48, "K": 60, "pH": 5.7, "OM": 3.8,
        "soil_type": "Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Banana", "Cacao", "Coconut"],
        "notes": "Major banana plantation area; Hijo Resources",
        "lat": 7.4231, "lon": 125.8395,
    },
    "Bincungan": {
        "N": 78, "P": 42, "K": 45, "pH": 5.5, "OM": 3.2,
        "soil_type": "Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Rice", "Banana", "Coconut"],
        "notes": "Lowland rice paddies; near Tagum-Liboganon River",
        "lat": 7.4620, "lon": 125.8340,
    },
    "Busaon": {
        "N": 55, "P": 35, "K": 70, "pH": 5.8, "OM": 1.8,
        "soil_type": "Sandy Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Coconut", "Banana", "Cassava"],
        "notes": "Coastal area; aquaculture and coconut",
        "lat": 7.4910, "lon": 125.8560,
    },
    "Canocotan": {
        "N": 70, "P": 45, "K": 55, "pH": 5.9, "OM": 2.8,
        "soil_type": "Loam",
        "classification": "Alfisol",
        "primary_crops": ["Banana", "Rice", "Corn"],
        "notes": "Mixed farming; banana and rice rotation",
        "lat": 7.4350, "lon": 125.7910,
    },
    "Cuambogan": {
        "N": 60, "P": 40, "K": 65, "pH": 5.6, "OM": 3.0,
        "soil_type": "Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Coconut", "Cacao", "Sweet Potato"],
        "notes": "Upland area; coconut-cacao intercropping common",
        "lat": 7.4100, "lon": 125.7850,
    },
    "La Filipina": {
        "N": 85, "P": 50, "K": 55, "pH": 5.8, "OM": 4.0,
        "soil_type": "Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Banana", "Rice", "Papaya"],
        "notes": "Large banana cooperatives; fertile soil",
        "lat": 7.4580, "lon": 125.7920,
    },
    "Liboganon": {
        "N": 72, "P": 38, "K": 50, "pH": 5.4, "OM": 3.5,
        "soil_type": "Silty Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Rice", "Coconut", "Banana"],
        "notes": "River delta area; rich alluvial deposits",
        "lat": 7.4800, "lon": 125.8100,
    },
    "Madaum": {
        "N": 68, "P": 44, "K": 58, "pH": 5.7, "OM": 3.2,
        "soil_type": "Clay Loam",
        "classification": "Alfisol",
        "primary_crops": ["Banana", "Coconut", "Durian"],
        "notes": "Hijo plantation zone; durian emerging",
        "lat": 7.4950, "lon": 125.8250,
    },
    "Magdum": {
        "N": 58, "P": 36, "K": 72, "pH": 5.5, "OM": 1.5,
        "soil_type": "Sandy Loam",
        "classification": "Ultisol",
        "primary_crops": ["Coconut", "Cassava", "Sweet Potato"],
        "notes": "Upland area; slightly acidic soils",
        "lat": 7.3950, "lon": 125.8100,
    },
    "Magugpo East": {
        "N": 50, "P": 30, "K": 40, "pH": 6.2, "OM": 2.0,
        "soil_type": "Loam",
        "classification": "Alfisol",
        "primary_crops": ["Eggplant", "Tomato", "Rice"],
        "notes": "Urban/peri-urban; vegetable gardens",
        "lat": 7.4475, "lon": 125.8130,
    },
    "Magugpo North": {
        "N": 48, "P": 32, "K": 38, "pH": 6.3, "OM": 1.8,
        "soil_type": "Loam",
        "classification": "Alfisol",
        "primary_crops": ["Eggplant", "Tomato", "Papaya"],
        "notes": "Urban area; backyard farming",
        "lat": 7.4520, "lon": 125.8090,
    },
    "Magugpo Poblacion": {
        "N": 45, "P": 28, "K": 35, "pH": 6.4, "OM": 1.5,
        "soil_type": "Loam",
        "classification": "Alfisol",
        "primary_crops": ["Eggplant", "Tomato", "Papaya"],
        "notes": "City center; limited agricultural area",
        "lat": 7.4478, "lon": 125.8094,
    },
    "Magugpo South": {
        "N": 52, "P": 34, "K": 42, "pH": 6.1, "OM": 2.2,
        "soil_type": "Clay Loam",
        "classification": "Alfisol",
        "primary_crops": ["Rice", "Eggplant", "Corn"],
        "notes": "Peri-urban; mixed use land",
        "lat": 7.4430, "lon": 125.8110,
    },
    "Magugpo West": {
        "N": 55, "P": 36, "K": 45, "pH": 6.0, "OM": 2.0,
        "soil_type": "Loam",
        "classification": "Alfisol",
        "primary_crops": ["Eggplant", "Papaya", "Corn"],
        "notes": "Peri-urban; transitioning to commercial",
        "lat": 7.4480, "lon": 125.8050,
    },
    "Mankilam": {
        "N": 72, "P": 52, "K": 50, "pH": 6.0, "OM": 3.3,
        "soil_type": "Loam",
        "classification": "Alfisol",
        "primary_crops": ["Coconut", "Cacao", "Banana"],
        "notes": "USeP campus area; research farming nearby",
        "lat": 7.4200, "lon": 125.8200,
    },
    "New Balamban": {
        "N": 62, "P": 40, "K": 68, "pH": 5.6, "OM": 1.8,
        "soil_type": "Clay Loam",
        "classification": "Ultisol",
        "primary_crops": ["Coconut", "Banana", "Cassava"],
        "notes": "Resettlement area; developing farmlands",
        "lat": 7.4050, "lon": 125.7900,
    },
    "Nueva Fuerza": {
        "N": 64, "P": 42, "K": 62, "pH": 5.7, "OM": 2.8,
        "soil_type": "Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Banana", "Coconut", "Rice"],
        "notes": "Agricultural community; banana-coconut area",
        "lat": 7.4150, "lon": 125.8050,
    },
    "Pagsabangan": {
        "N": 82, "P": 45, "K": 48, "pH": 5.5, "OM": 3.0,
        "soil_type": "Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Rice", "Banana", "Coconut"],
        "notes": "Major rice-producing barangay; irrigated fields",
        "lat": 7.4350, "lon": 125.8350,
    },
    "Pandapan": {
        "N": 58, "P": 38, "K": 55, "pH": 5.8, "OM": 1.8,
        "soil_type": "Sandy Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Coconut", "Corn", "Cassava"],
        "notes": "Upland area; corn and root crops",
        "lat": 7.4000, "lon": 125.8300,
    },
    "San Agustin": {
        "N": 66, "P": 44, "K": 58, "pH": 5.9, "OM": 2.6,
        "soil_type": "Loam",
        "classification": "Alfisol",
        "primary_crops": ["Banana", "Rice", "Mango"],
        "notes": "Mixed farming; mango orchards present",
        "lat": 7.4650, "lon": 125.7950,
    },
    "San Isidro": {
        "N": 70, "P": 46, "K": 62, "pH": 5.8, "OM": 3.5,
        "soil_type": "Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Banana", "Coconut", "Durian"],
        "notes": "Fertile agricultural land; durian cultivation",
        "lat": 7.4700, "lon": 125.8400,
    },
    "San Miguel": {
        "N": 60, "P": 40, "K": 56, "pH": 5.7, "OM": 3.0,
        "soil_type": "Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Coconut", "Banana", "Cacao"],
        "notes": "Agricultural barangay; cacao growing area",
        "lat": 7.4550, "lon": 125.8450,
    },
    "Visayan Village": {
        "N": 74, "P": 48, "K": 52, "pH": 5.6, "OM": 2.8,
        "soil_type": "Clay Loam",
        "classification": "Inceptisol",
        "primary_crops": ["Rice", "Banana", "Coconut"],
        "notes": "Active farming community; rice and banana",
        "lat": 7.4400, "lon": 125.7980,
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# FERTILIZER GUIDE — Enhanced with local Tagum brands, PHP prices, DA-sourced rates
# Sources: DA Region XI Fertilizer Price Monitoring, PhilFert, BFAR, DA-HVCDP
# Prices as of 2024–2025 season (may fluctuate; verify at local agrivet)
# ─────────────────────────────────────────────────────────────────────────────
FERTILIZER_GUIDE = {
    "low_N": {
        "condition": "Low Nitrogen (N < 50 mg/kg)",
        "urgency": "high",
        "icon": "🔴",
        "recommendation": "Apply Urea (46-0-0) at 2–3 bags/ha split in two applications: ½ at land preparation, ½ at 30 days after transplanting. For acidic soils, prefer Ammonium Sulfate to avoid further pH drop.",
        "rate": "2–3 bags (50 kg) per hectare",
        "timing": "Split application: basal + 30 DAT",
        "brands": [
            {"name": "Atlas Fertilizers Urea 46-0-0", "price_php": 1350, "per": "50 kg bag", "where": "Atlas Agri-Store, Tagum National Highway"},
            {"name": "Harbest Ammonium Sulfate 21-0-0", "price_php": 920, "per": "50 kg bag", "where": "Harbest Agri Center, Arellano Ave, Tagum"},
            {"name": "Philchem Urea 46-0-0", "price_php": 1320, "per": "50 kg bag", "where": "Tagum Public Market Agrivet Row"},
            {"name": "DA Subsidized Urea (RCEF)", "price_php": 800, "per": "50 kg bag", "where": "DA Region XI office, Tagum City Hall compound — check availability"},
        ],
        "pro_tip": "Split urea applications reduce nitrogen loss from leaching in Tagum's rainy season. Never apply urea during heavy rain.",
        "da_source": "DA Region XI Fertilizer Use Efficiency Guide, 2023",
    },
    "low_P": {
        "condition": "Low Phosphorus (P < 30 mg/kg)",
        "urgency": "medium",
        "icon": "🟠",
        "recommendation": "Apply Single Superphosphate (0-18-0) or Complete (14-14-14) as basal fertilizer at land preparation. Phosphorus is immobile in soil — apply in the root zone for best results.",
        "rate": "3–4 bags (50 kg) per hectare",
        "timing": "Basal application at transplanting",
        "brands": [
            {"name": "Atlas Solophos 0-18-0", "price_php": 1100, "per": "50 kg bag", "where": "Atlas Agri-Store, Tagum National Highway"},
            {"name": "Fertiphos 0-20-0", "price_php": 1050, "per": "50 kg bag", "where": "Tagum Public Market Agrivet Row"},
            {"name": "PhilMaterials Complete 14-14-14", "price_php": 1250, "per": "50 kg bag", "where": "Any agrivet store in Tagum City"},
            {"name": "DA Subsidized Solophos (RCEF)", "price_php": 700, "per": "50 kg bag", "where": "DA Region XI HVCDP office, Tagum"},
        ],
        "pro_tip": "Acidic soils (pH < 5.5) lock up phosphorus — liming first dramatically improves P availability. Check your pH before applying P fertilizer.",
        "da_source": "PhilRice Crop Manager, DA Fertilizer Guidelines 2023",
    },
    "low_K": {
        "condition": "Low Potassium (K < 40 mg/kg)",
        "urgency": "medium",
        "icon": "🟡",
        "recommendation": "Apply Muriate of Potash (0-0-60) at 2–3 bags/ha. For banana and coconut, potassium is critical for bunch weight and copra quality. Apply in split doses for better uptake.",
        "rate": "2–3 bags (50 kg) per hectare",
        "timing": "Split: 50% basal, 50% at 45 DAT",
        "brands": [
            {"name": "Atlas Muriate of Potash 0-0-60", "price_php": 1480, "per": "50 kg bag", "where": "Atlas Agri-Store, Tagum National Highway"},
            {"name": "Imported KCl (Russia/Canada origin)", "price_php": 1550, "per": "50 kg bag", "where": "Tagum Public Market agrivet stores"},
            {"name": "Harbest 0-0-60 MOP", "price_php": 1500, "per": "50 kg bag", "where": "Harbest Agri Center, Arellano Ave, Tagum"},
            {"name": "SQM Potassium Nitrate 13-0-46", "price_php": 2200, "per": "50 kg bag", "where": "Specialty agrivet stores, Tagum City"},
        ],
        "pro_tip": "Banana is extremely K-hungry — Tagum's plantation practice is 500–800g KCl per plant per year (Yara Philippines data). Don't underestimate K for commercial banana.",
        "da_source": "PCA Technoguide on Coconut, Yara PH Banana Nutrition Guide",
    },
    "low_pH": {
        "condition": "Acidic Soil (pH < 5.5)",
        "urgency": "high",
        "icon": "🔴",
        "recommendation": "Apply agricultural dolomitic lime at 1–2 tons/ha to raise pH. Apply 2–4 weeks before planting to allow lime to react with soil. Retest pH after 4 weeks. BSWM data shows most Tagum soils trend acidic (pH 5.2–5.8) — liming is a seasonal must.",
        "rate": "1,000–2,000 kg per hectare",
        "timing": "2–4 weeks before land preparation",
        "brands": [
            {"name": "Agri Dolomite Lime (local)", "price_php": 400, "per": "50 kg bag", "where": "Hardware stores along Tagum National Highway (Sto. Tomas area)"},
            {"name": "PHILPHOS Agricultural Lime", "price_php": 450, "per": "50 kg bag", "where": "Tagum Public Market, agrivet section"},
            {"name": "Calcitic Lime (imported)", "price_php": 500, "per": "50 kg bag", "where": "Select agrivet stores near Tagum City Hall"},
            {"name": "DA Subsidized Lime (RCEF Program)", "price_php": 250, "per": "50 kg bag", "where": "DA Region XI office — inquire during RCEF distribution"},
        ],
        "pro_tip": "Liming unlocks N, P, and K simultaneously. ₱10,000 spent on lime often returns ₱30,000+ in improved fertilizer efficiency. Highly recommended before any major cropping season.",
        "da_source": "BSWM Region XI Soil Acidity Management Guide, DA-BAR 2022",
    },
    "high_pH": {
        "condition": "Alkaline Soil (pH > 7.0)",
        "urgency": "low",
        "icon": "🟡",
        "recommendation": "Incorporate Ammonium Sulfate (acidifying) or elemental sulfur to gradually lower pH. Add organic matter (vermicast, compost) which naturally acidifies soil over time. Avoid calcium-based fertilizers.",
        "rate": "2–4 bags Ammonium Sulfate per hectare per season",
        "timing": "Apply at land preparation; monitor pH every season",
        "brands": [
            {"name": "Harbest Ammonium Sulfate 21-0-0", "price_php": 920, "per": "50 kg bag", "where": "Harbest Agri Center, Arellano Ave, Tagum"},
            {"name": "Atlas Ammonium Sulfate 21-0-0", "price_php": 900, "per": "50 kg bag", "where": "Atlas Agri-Store, Tagum National Highway"},
            {"name": "Elemental Sulfur (powder)", "price_php": 1200, "per": "50 kg bag", "where": "Specialty agrivet stores, Tagum City"},
        ],
        "pro_tip": "High pH is uncommon in Tagum but can occur in reclaimed or limestone-influenced areas. Verify with a proper soil test before major intervention.",
        "da_source": "BSWM Soil pH Management Guide, DA Region XI",
    },
    "low_OM": {
        "condition": "Low Organic Matter (OM < 2.0%)",
        "urgency": "medium",
        "icon": "🟠",
        "recommendation": "Incorporate vermicast or compost at 2–3 tons/ha before planting. Mulch with rice straw, banana pseudo-stem chippings, or dried leaves. OM builds over 2–3 seasons — commit to a multi-season improvement plan. Low OM reduces water-holding capacity and suppresses beneficial soil microbes.",
        "rate": "2,000–3,000 kg vermicast per hectare",
        "timing": "14–21 days before transplanting (incorporate into soil)",
        "brands": [
            {"name": "Tagum City Organic Vermicast", "price_php": 600, "per": "50 kg sack (₱12/kg)", "where": "DA-HVCDP office, Tagum City Hall compound"},
            {"name": "BioOrg Certified Vermicast", "price_php": 700, "per": "50 kg sack", "where": "DA Region XI Organic Agriculture office, Davao City"},
            {"name": "Luntian Compost (local cooperative)", "price_php": 400, "per": "50 kg sack (₱8/kg)", "where": "Local organic cooperatives — ask at barangay halls in Tagum"},
            {"name": "SNAP Organic Foliar Fertilizer", "price_php": 350, "per": "1 liter bottle", "where": "DA extension offices, UPLB-licensed dealers in Tagum"},
        ],
        "pro_tip": "Banana pseudo-stem chipping is FREE and abundant around Tagum's plantation areas. TADECO and Lapanday farms often allow collection of organic waste — an easy win for smallholders.",
        "da_source": "DA Organic Agriculture Act RA 10068, DA-HVCDP Tagum organic program",
    },
    "balanced": {
        "condition": "Balanced Nutrients ✅",
        "urgency": "low",
        "icon": "🟢",
        "recommendation": "Soil nutrient levels are within optimal range. Apply maintenance fertilizer (Complete 14-14-14) at 2–3 bags/ha per cropping season to sustain productivity. Continue monitoring soil health every 2 seasons.",
        "rate": "2–3 bags (50 kg) per hectare per season",
        "timing": "At land preparation + 30 DAT",
        "brands": [
            {"name": "PhilMaterials Complete 14-14-14", "price_php": 1250, "per": "50 kg bag", "where": "Any agrivet store in Tagum City"},
            {"name": "Atlas Complete 14-14-14", "price_php": 1230, "per": "50 kg bag", "where": "Atlas Agri-Store, Tagum National Highway"},
            {"name": "Harbest 16-16-16", "price_php": 1380, "per": "50 kg bag", "where": "Harbest Agri Center, Arellano Ave, Tagum"},
        ],
        "pro_tip": "Even balanced soil benefits from annual soil testing. DA Region XI offers free soil testing — contact the Tagum City Agriculture Office at the City Hall for scheduling.",
        "da_source": "DA Region XI Fertilizer Monitoring, 2024",
    },
}
# ─────────────────────────────────────────────────────────────────────────────
# CROP ECONOMICS — DA Region XI / PSA Davao del Norte (2026 Calibrated)
# Wage Order RB XI-24 (Mar 13 2026): agricultural wage = ₱515/day
# DA-CRA structure: TCP = Labor Cost + Material Cost + Other Cost
# ROI target: 20–60% (DA Region XI real-world CRA range)
# ─────────────────────────────────────────────────────────────────────────────
CROP_ECONOMICS = {
    # ── RICE ─────────────────────────────────────────────────────────────────
    # Irrigated lowland palay, Tagum/Davao del Norte
    # GR = 4720 × 18.89 = 89,161 | NI = 24,161 | ROI = 37%
    "Rice": {
        "cropping_seasons_per_year": 2,
        "harvest_months": 4,
        "avg_yield_kg_ha": 4720,
        "farmgate_price_php_kg": 18.89,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "land_preparation":        {"man_days": 5,  "cost": 2575},
            "transplanting":           {"man_days": 12, "cost": 6180},
            "fertilizer_application":  {"man_days": 2,  "cost": 1030},
            "weeding_cultivation":     {"man_days": 8,  "cost": 4120},
            "pest_disease_management": {"man_days": 3,  "cost": 1545},
            "harvesting_threshing":    {"man_days": 8,  "cost": 4120},
            "hauling_transport":       {"man_days": 3,  "cost": 1545},
            "total": 21115,
        },
        "material_cost": {
            "seeds_planting_material": 3000,
            "fertilizers":             9000,
            "pesticides_herbicides":   4000,
            "irrigation_fees":         3000,
            "other_materials":          885,
            "total": 19885,
        },
        "other_cost": {
            "land_rental":            9000,
            "equipment_rental":       7000,
            "post_harvest_costs":     8000,
            "total": 24000,
        },
        "production_cost_php": 65000,
        "notes": "Irrigated lowland palay; DA Region XI 2026 benchmark yield & price",
        "source": "DA Region XI CRA 2026, PSA Davao del Norte, PhilRice RCEF",
    },

    # ── BANANA ───────────────────────────────────────────────────────────────
    # Cavendish commercial; annual cycle; Tagum's #1 cash crop
    # GR = 28000 × 13 = 364,000 | NI = 114,000 | ROI = 45.6%
    "Banana": {
        "cropping_seasons_per_year": 1,
        "harvest_months": 12,
        "avg_yield_kg_ha": 28000,
        "farmgate_price_php_kg": 13,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "desuckering_deleafing":   {"man_days": 40, "cost": 20600},
            "fertilizer_application":  {"man_days": 10, "cost": 5150},
            "pest_disease_management": {"man_days": 30, "cost": 15450},
            "harvesting_hauling":      {"man_days": 60, "cost": 30900},
            "bagging_propping":        {"man_days": 20, "cost": 10300},
            "other_crop_care":         {"man_days": 20, "cost": 10300},
            "total": 92700,
        },
        "material_cost": {
            "planting_materials":       5000,
            "fertilizers":             65000,
            "pesticides_fungicides":   30000,
            "packaging_materials":     15000,
            "total": 115000,
        },
        "other_cost": {
            "land_rental":            12000,
            "equipment_tools":         8000,
            "post_harvest_costs":     22300,
            "total": 42300,
        },
        "production_cost_php": 250000,
        "notes": "Cavendish export; TADECO/Lapanday basis; Tagum's #1 cash crop",
        "source": "DA Region XI Banana Industry Report 2026, Davao del Norte PAO",
    },

    # ── CACAO ─────────────────────────────────────────────────────────────────
    # Established orchard; annual totals (2 harvest peaks/yr, cost/yield already annual)
    # GR = 1000 × 115 = 115,000 | NI = 27,000 | ROI = 30.7%
    "Cacao": {
        "cropping_seasons_per_year": 1,
        "harvest_months": 12,
        "avg_yield_kg_ha": 1000,
        "farmgate_price_php_kg": 115,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "pruning_shaping":         {"man_days": 10, "cost": 5150},
            "fertilizer_application":  {"man_days": 5,  "cost": 2575},
            "pest_disease_management": {"man_days": 10, "cost": 5150},
            "weeding_slashing":        {"man_days": 8,  "cost": 4120},
            "harvesting_pod_breaking": {"man_days": 20, "cost": 10300},
            "fermentation_drying":     {"man_days": 2,  "cost": 1030},
            "total": 28325,
        },
        "material_cost": {
            "fertilizers":             15000,
            "pesticides_insecticides": 12000,
            "fermentation_materials":   3000,
            "other_materials":          7000,
            "total": 37000,
        },
        "other_cost": {
            "land_rental":            10000,
            "equipment_tools":         5000,
            "post_harvest_transport":  7675,
            "total": 22675,
        },
        "production_cost_php": 88000,
        "notes": "Established orchard; 2 harvest peaks/yr; cost & yield are annual totals",
        "source": "ICRAF/ACDI-VOCA Mindanao 2026, DA Region XI Cacao Program",
    },

    # ── COCONUT ──────────────────────────────────────────────────────────────
    # Copra basis; PCA Mindanao smallholder avg 1500-2000 kg copra/ha/yr
    # GR = 1800 × 38 = 68,400 | NI = 13,400 | ROI = 24.4%
    "Coconut": {
        "cropping_seasons_per_year": 1,
        "harvest_months": 12,
        "avg_yield_kg_ha": 1800,
        "farmgate_price_php_kg": 38,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "fertilizer_application":  {"man_days": 4,  "cost": 2060},
            "pest_disease_management": {"man_days": 3,  "cost": 1545},
            "weeding_slashing":        {"man_days": 8,  "cost": 4120},
            "harvesting":              {"man_days": 16, "cost": 8240},
            "copra_processing":        {"man_days": 8,  "cost": 4120},
            "hauling_transport":       {"man_days": 4,  "cost": 2060},
            "total": 22145,
        },
        "material_cost": {
            "fertilizers":              8000,
            "pesticides":               3500,
            "copra_processing_materials": 2000,
            "total": 13500,
        },
        "other_cost": {
            "land_rental":             8000,
            "equipment_tools":         2000,
            "post_harvest_costs":      9355,
            "total": 19355,
        },
        "production_cost_php": 55000,
        "notes": "Copra basis; PCA Mindanao smallholder avg 1,800 kg copra/ha/yr (not 5,000)",
        "source": "PCA Technoguide 2026, PSA Coconut Statistics, DA Region XI",
    },

    # ── DURIAN ───────────────────────────────────────────────────────────────
    # Established orchard, DA Davao avg mature orchard 3000-5000 kg/ha/yr
    # GR = 4500 × 70 = 315,000 | NI = 115,000 | ROI = 57.5%
    "Durian": {
        "cropping_seasons_per_year": 1,
        "harvest_months": 12,
        "avg_yield_kg_ha": 4500,
        "farmgate_price_php_kg": 70,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "pruning_shaping":         {"man_days": 10, "cost": 5150},
            "fertilizer_application":  {"man_days": 10, "cost": 5150},
            "pest_disease_management": {"man_days": 20, "cost": 10300},
            "flower_induction_care":   {"man_days": 10, "cost": 5150},
            "fruit_bagging":           {"man_days": 30, "cost": 15450},
            "harvesting_transport":    {"man_days": 20, "cost": 10300},
            "other_crop_care":         {"man_days": 10, "cost": 5150},
            "total": 56650,
        },
        "material_cost": {
            "fertilizers":             45000,
            "pesticides_fungicides":   25000,
            "bagging_materials":        8000,
            "other_materials":         20000,
            "total": 98000,
        },
        "other_cost": {
            "land_rental":            20000,
            "equipment_tools":         8000,
            "post_harvest_costs":     17350,
            "total": 45350,
        },
        "production_cost_php": 200000,
        "notes": "7–10 yr to full production; DA Davao avg mature orchard yield 3000–5000 kg/ha",
        "source": "DA Region XI Durian Industry Program 2026, PSA Davao Region",
    },

    # ── CORN ─────────────────────────────────────────────────────────────────
    # Yellow hybrid, rain-fed, Tagum upland
    # GR = 3200 × 17 = 54,400 | NI = 11,900 | ROI = 28%
    "Corn": {
        "cropping_seasons_per_year": 2,
        "harvest_months": 3,
        "avg_yield_kg_ha": 3200,
        "farmgate_price_php_kg": 17,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "land_preparation":        {"man_days": 5,  "cost": 2575},
            "planting":                {"man_days": 5,  "cost": 2575},
            "fertilizer_application":  {"man_days": 2,  "cost": 1030},
            "weeding_cultivation":     {"man_days": 6,  "cost": 3090},
            "pest_management":         {"man_days": 2,  "cost": 1030},
            "harvesting_shelling":     {"man_days": 8,  "cost": 4120},
            "total": 14420,
        },
        "material_cost": {
            "seeds":                    3500,
            "fertilizers":              8000,
            "pesticides_herbicides":    3500,
            "other_materials":          1000,
            "total": 16000,
        },
        "other_cost": {
            "land_rental":              6000,
            "equipment_rental":         2500,
            "post_harvest_costs":       3580,
            "total": 12080,
        },
        "production_cost_php": 42500,
        "notes": "Yellow hybrid corn; main upland crop in Tagum; rain-fed",
        "source": "PhilMaize 2026, PSA Corn Statistics, DA Region XI",
    },

    # ── MANGO ────────────────────────────────────────────────────────────────
    # Carabao mango, established orchard, PCARRD Philippines avg 3000-4000 kg/ha
    # GR = 3500 × 48 = 168,000 | NI = 56,000 | ROI = 50%
    "Mango": {
        "cropping_seasons_per_year": 1,
        "harvest_months": 12,
        "avg_yield_kg_ha": 3500,
        "farmgate_price_php_kg": 48,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "pruning_shaping":         {"man_days": 6,  "cost": 3090},
            "fertilizer_application":  {"man_days": 5,  "cost": 2575},
            "flower_induction":        {"man_days": 5,  "cost": 2575},
            "pest_disease_management": {"man_days": 10, "cost": 5150},
            "fruit_bagging":           {"man_days": 20, "cost": 10300},
            "harvesting_sorting":      {"man_days": 10, "cost": 5150},
            "total": 28840,
        },
        "material_cost": {
            "fertilizers":             20000,
            "pesticides_fungicides":   15000,
            "potassium_nitrate":        8000,
            "bagging_materials":        5000,
            "other_materials":          7000,
            "total": 55000,
        },
        "other_cost": {
            "land_rental":            12000,
            "equipment_tools":         3000,
            "post_harvest_costs":     13160,
            "total": 28160,
        },
        "production_cost_php": 112000,
        "notes": "Carabao mango; chemical induction for off-season; PCARRD PH avg 3000-4000 kg/ha",
        "source": "PCARRD Mango Guide 2026, DA Region XI",
    },

    # ── PAPAYA ───────────────────────────────────────────────────────────────
    # Red Lady/Sinta; year-round fruiting; high disease management cost
    # GR = 22000 × 11 = 242,000 | NI = 70,000 | ROI = 40.7%
    "Papaya": {
        "cropping_seasons_per_year": 1,
        "harvest_months": 10,
        "avg_yield_kg_ha": 22000,
        "farmgate_price_php_kg": 11,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "land_preparation":        {"man_days": 6,  "cost": 3090},
            "transplanting":           {"man_days": 6,  "cost": 3090},
            "fertilizer_application":  {"man_days": 7,  "cost": 3605},
            "pest_disease_management": {"man_days": 20, "cost": 10300},
            "weeding_cultivation":     {"man_days": 6,  "cost": 3090},
            "harvesting_year_round":   {"man_days": 50, "cost": 25750},
            "hauling_transport":       {"man_days": 5,  "cost": 2575},
            "total": 51500,
        },
        "material_cost": {
            "planting_materials":       5000,
            "fertilizers":             30000,
            "pesticides_insecticides": 35000,
            "mulching_materials":       3000,
            "other_materials":          7000,
            "total": 80000,
        },
        "other_cost": {
            "land_rental":            15000,
            "equipment_tools":         5000,
            "post_harvest_costs":     20500,
            "total": 40500,
        },
        "production_cost_php": 172000,
        "notes": "Red Lady/Sinta; Ringspot management is major cost; yield 22,000 kg/ha/yr",
        "source": "DA Crop Production Guide 2026, PCAARRD",
    },

    # ── CASSAVA ──────────────────────────────────────────────────────────────
    # Industrial/starch variety; Davao del Norte starch mills
    # GR = 15000 × 5 = 75,000 | NI = 15,000 | ROI = 25%
    "Cassava": {
        "cropping_seasons_per_year": 1,
        "harvest_months": 10,
        "avg_yield_kg_ha": 15000,
        "farmgate_price_php_kg": 5,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "land_preparation":        {"man_days": 7,  "cost": 3605},
            "planting":                {"man_days": 5,  "cost": 2575},
            "fertilizer_application":  {"man_days": 2,  "cost": 1030},
            "weeding_cultivation":     {"man_days": 8,  "cost": 4120},
            "harvesting":              {"man_days": 15, "cost": 7725},
            "hauling_transport":       {"man_days": 5,  "cost": 2575},
            "total": 21630,
        },
        "material_cost": {
            "planting_stakes":          5000,
            "fertilizers":              8000,
            "pesticides":               2000,
            "other_materials":          1000,
            "total": 16000,
        },
        "other_cost": {
            "land_rental":              8000,
            "equipment_rental":         5000,
            "post_harvest_costs":       9370,
            "total": 22370,
        },
        "production_cost_php": 60000,
        "notes": "Industrial starch variety; Davao del Norte starch mills; yield 15,000 kg/ha fresh roots",
        "source": "PhilRootcrops VSU 2026, DA Region XI Root Crops Program",
    },

    # ── SWEET POTATO ─────────────────────────────────────────────────────────
    # Orange-flesh; upland Tagum; 2 seasons/yr
    # GR = 7500 × 15 = 112,500 | NI = 29,500 | ROI = 35.5%
    "Sweet Potato": {
        "cropping_seasons_per_year": 2,
        "harvest_months": 4,
        "avg_yield_kg_ha": 7500,
        "farmgate_price_php_kg": 15,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "land_preparation_ridging": {"man_days": 12, "cost": 6180},
            "planting_vine_cuttings":   {"man_days": 7,  "cost": 3605},
            "fertilizer_application":   {"man_days": 2,  "cost": 1030},
            "pest_disease_management":  {"man_days": 6,  "cost": 3090},
            "weeding_cultivation":      {"man_days": 8,  "cost": 4120},
            "harvesting":               {"man_days": 15, "cost": 7725},
            "hauling_transport":        {"man_days": 5,  "cost": 2575},
            "total": 28325,
        },
        "material_cost": {
            "planting_vines":           4000,
            "fertilizers":             12000,
            "pesticides":               6000,
            "other_materials":          3675,
            "total": 25675,
        },
        "other_cost": {
            "land_rental":             10000,
            "equipment_rental":         4000,
            "post_harvest_costs":      15000,
            "total": 29000,
        },
        "production_cost_php": 83000,
        "notes": "Orange-flesh OFSP; upland Tagum; 2 seasons/yr; yield 7,500 kg/ha/season",
        "source": "UPLB Sweet Potato Research 2026, DA Region XI",
    },

    # ── EGGPLANT ─────────────────────────────────────────────────────────────
    # Intensive vegetable; high pest pressure (fruit borer); 2 seasons/yr
    # GR = 10000 × 22 = 220,000 | NI = 63,000 | ROI = 40.1%
    "Eggplant": {
        "cropping_seasons_per_year": 2,
        "harvest_months": 4,
        "avg_yield_kg_ha": 10000,
        "farmgate_price_php_kg": 22,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "land_preparation":         {"man_days": 7,  "cost": 3605},
            "transplanting_seedlings":  {"man_days": 10, "cost": 5150},
            "staking_trellising":       {"man_days": 10, "cost": 5150},
            "fertilizer_application":   {"man_days": 5,  "cost": 2575},
            "pest_disease_management":  {"man_days": 20, "cost": 10300},
            "weeding_cultivation":      {"man_days": 8,  "cost": 4120},
            "harvesting_every_3_days":  {"man_days": 50, "cost": 25750},
            "hauling_marketing":        {"man_days": 10, "cost": 5150},
            "total": 61800,
        },
        "material_cost": {
            "seeds_seedling_raising":   5000,
            "fertilizers":             25000,
            "pesticides_insecticides": 30000,
            "mulching_materials":       3000,
            "other_materials":          7000,
            "total": 70000,
        },
        "other_cost": {
            "land_rental":             10000,
            "equipment_tools":          2000,
            "post_harvest_costs":      13200,
            "total": 25200,
        },
        "production_cost_php": 157000,
        "notes": "High-value vegetable; fruit borer major pest; yield 10,000 kg/ha/season",
        "source": "PCAARRD Eggplant Guide 2026, DA Region XI",
    },

    # ── TOMATO ───────────────────────────────────────────────────────────────
    # Intensive; high disease pressure; price volatile ₱15–80/kg
    # GR = 12000 × 25 = 300,000 | NI = 107,000 | ROI = 55.4%
    "Tomato": {
        "cropping_seasons_per_year": 2,
        "harvest_months": 3,
        "avg_yield_kg_ha": 12000,
        "farmgate_price_php_kg": 25,
        "labor_cost": {
            "wage_rate_php_day": 515,
            "land_preparation":         {"man_days": 7,  "cost": 3605},
            "transplanting_seedlings":  {"man_days": 10, "cost": 5150},
            "staking_trellising":       {"man_days": 15, "cost": 7725},
            "fertilizer_application":   {"man_days": 6,  "cost": 3090},
            "pest_disease_management":  {"man_days": 30, "cost": 15450},
            "weeding_cultivation":      {"man_days": 7,  "cost": 3605},
            "harvesting":               {"man_days": 40, "cost": 20600},
            "hauling_sorting":          {"man_days": 10, "cost": 5150},
            "total": 64375,
        },
        "material_cost": {
            "seeds_seedling":           5000,
            "fertilizers":             30000,
            "pesticides_fungicides":   45000,
            "trellis_materials":       10000,
            "other_materials":          5000,
            "total": 95000,
        },
        "other_cost": {
            "land_rental":             10000,
            "equipment_tools":          2500,
            "post_harvest_costs":      21125,
            "total": 33625,
        },
        "production_cost_php": 193000,
        "notes": "Price volatile ₱15–80/kg; avg ₱25 used; yield 12,000 kg/ha/season",
        "source": "PCAARRD Tomato Guide 2026, PSA price monitoring",
    },
}


def get_fertilizer_recommendations(n, p, k, ph, om=None):
    """Generate fertilizer recommendations based on soil nutrient levels and organic matter."""
    recommendations = []
    if n < 50:
        recommendations.append(FERTILIZER_GUIDE["low_N"])
    if p < 30:
        recommendations.append(FERTILIZER_GUIDE["low_P"])
    if k < 40:
        recommendations.append(FERTILIZER_GUIDE["low_K"])
    if ph < 5.5:
        recommendations.append(FERTILIZER_GUIDE["low_pH"])
    if ph > 7.0:
        recommendations.append(FERTILIZER_GUIDE["high_pH"])
    if om is not None and om < 2.0:
        recommendations.append(FERTILIZER_GUIDE["low_OM"])

    if not recommendations:
        recommendations.append(FERTILIZER_GUIDE["balanced"])

    return recommendations


def get_crop_economics(crop_name):
    """Return economic data for ROI calculation for a given crop."""
    return CROP_ECONOMICS.get(crop_name, None)


