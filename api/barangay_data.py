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
# CROP ECONOMICS — DA / PSA Region XI Data for ROI Calculation
# Source: PSA Crop Statistics 2023, DA Region XI Production Cost Survey,
#         Davao del Norte Provincial Agriculture Office price monitoring
# All costs/prices in Philippine Peso (PHP) per hectare
# ─────────────────────────────────────────────────────────────────────────────
CROP_ECONOMICS = {
    "Rice": {
        "production_cost_php": 55000,   # PHP/ha/season (PhilRice, 2023)
        "avg_yield_kg_ha": 4200,         # kg/ha (DA Region XI avg, irrigated)
        "farmgate_price_php_kg": 22,     # PHP/kg (PSA Davao del Norte, 2024)
        "cropping_seasons_per_year": 2,
        "harvest_months": 4,
        "notes": "Irrigated lowland rice; PhilRice recommends 14-14-14 + Urea split",
        "source": "PSA Rice Statistics 2023, DA Region XI",
    },
    "Banana": {
        "production_cost_php": 180000,  # PHP/ha/year (Cavendish commercial, TADECO basis)
        "avg_yield_kg_ha": 35000,        # kg/ha/year (Cavendish, 13 hands/bunch avg)
        "farmgate_price_php_kg": 14,     # PHP/kg (Tagum/Davao del Norte, 2024)
        "cropping_seasons_per_year": 1,
        "harvest_months": 12,
        "notes": "Cavendish for export; Tagum's #1 cash crop",
        "source": "DA Region XI Banana Industry Report 2023, Davao del Norte PAO",
    },
    "Cacao": {
        "production_cost_php": 80000,   # PHP/ha/year (established orchard)
        "avg_yield_kg_ha": 1200,         # kg/ha dry beans (ACDI/VOCA Mindanao)
        "farmgate_price_php_kg": 130,    # PHP/kg dry beans (Tagum, 2024 premium)
        "cropping_seasons_per_year": 2,
        "harvest_months": 12,
        "notes": "High-value crop; 2 harvest peaks per year",
        "source": "ICRAF/ACDI-VOCA Mindanao Cacao Data, DA Region XI 2023",
    },
    "Coconut": {
        "production_cost_php": 30000,   # PHP/ha/year (mature orchard)
        "avg_yield_kg_ha": 5000,         # kg copra/ha/year (PCA national avg)
        "farmgate_price_php_kg": 38,     # PHP/kg copra (Davao del Norte, 2024)
        "cropping_seasons_per_year": 1,
        "harvest_months": 12,
        "notes": "Copra basis; 6-8 year maturity period",
        "source": "PCA Technoguide, PSA Coconut Statistics 2023",
    },
    "Durian": {
        "production_cost_php": 120000,  # PHP/ha/year (established orchard)
        "avg_yield_kg_ha": 8000,         # kg/ha/year (DA Davao Region)
        "farmgate_price_php_kg": 80,     # PHP/kg farmgate (Davao region, 2024)
        "cropping_seasons_per_year": 1,
        "harvest_months": 12,
        "notes": "High-value; 7-10 yr to full production; Davao's premium export",
        "source": "DA Region XI Durian Industry Development Program, 2023",
    },
    "Corn": {
        "production_cost_php": 38000,   # PHP/ha/season (yellow corn, rain-fed)
        "avg_yield_kg_ha": 3500,         # kg/ha (DA Region XI upland avg)
        "farmgate_price_php_kg": 18,     # PHP/kg (PSA Davao del Norte, 2024)
        "cropping_seasons_per_year": 2,
        "harvest_months": 3,
        "notes": "Yellow corn (hybrid); main upland crop in Tagum",
        "source": "PhilMaize, PSA Corn Statistics 2023, DA Region XI",
    },
    "Mango": {
        "production_cost_php": 60000,   # PHP/ha/year (established orchard)
        "avg_yield_kg_ha": 6000,         # kg/ha/year (PCARRD data)
        "farmgate_price_php_kg": 55,     # PHP/kg (Davao del Norte, 2024)
        "cropping_seasons_per_year": 1,
        "harvest_months": 12,
        "notes": "Carabao mango; chemical induction used for off-season",
        "source": "PCARRD Mango Production Guide, DA Region XI 2023",
    },
    "Papaya": {
        "production_cost_php": 45000,   # PHP/ha/year
        "avg_yield_kg_ha": 30000,        # kg/ha/year (high-yielding variety)
        "farmgate_price_php_kg": 12,     # PHP/kg (Tagum market, 2024)
        "cropping_seasons_per_year": 1,
        "harvest_months": 10,
        "notes": "Red Lady or Sinta variety; year-round fruiting",
        "source": "DA Crop Production Guide, PCAARRD 2023",
    },
    "Cassava": {
        "production_cost_php": 28000,   # PHP/ha/season
        "avg_yield_kg_ha": 18000,        # kg/ha fresh roots (VSU/PhilRootcrops)
        "farmgate_price_php_kg": 5,      # PHP/kg fresh roots (Davao del Norte, 2024)
        "cropping_seasons_per_year": 1,
        "harvest_months": 10,
        "notes": "Industrial/starch variety; processed by local starch mills",
        "source": "PhilRootcrops VSU, DA Region XI Root Crops Program 2023",
    },
    "Sweet Potato": {
        "production_cost_php": 22000,   # PHP/ha/season
        "avg_yield_kg_ha": 12000,        # kg/ha (UPLB data)
        "farmgate_price_php_kg": 18,     # PHP/kg (Tagum market, 2024)
        "cropping_seasons_per_year": 2,
        "harvest_months": 4,
        "notes": "Orange-flesh variety for food security + commercial sale",
        "source": "UPLB Sweet Potato Research, DA Region XI 2023",
    },
    "Eggplant": {
        "production_cost_php": 80000,   # PHP/ha/season (intensive vegetable)
        "avg_yield_kg_ha": 25000,        # kg/ha (PCAARRD, irrigated)
        "farmgate_price_php_kg": 35,     # PHP/kg (Tagum/Davao del Norte, 2024)
        "cropping_seasons_per_year": 2,
        "harvest_months": 4,
        "notes": "High-value vegetable; Tagum markets have strong demand",
        "source": "PCAARRD Eggplant Production Guide, DA Region XI 2023",
    },
    "Tomato": {
        "production_cost_php": 90000,   # PHP/ha/season
        "avg_yield_kg_ha": 20000,        # kg/ha (DA irrigated farm avg)
        "farmgate_price_php_kg": 40,     # PHP/kg (Tagum market avg, 2024 — volatile)
        "cropping_seasons_per_year": 2,
        "harvest_months": 3,
        "notes": "Price highly volatile (₱15–80/kg); peak season = low price",
        "source": "PCAARRD Tomato Production Guide, PSA 2024 price monitoring",
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


