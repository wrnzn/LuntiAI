/* ============================================================================
   LuntiAI — Frontend Application Logic
   ============================================================================
   Handles barangay selection, weather API integration, form management,
   prediction requests, and results rendering.
   ============================================================================ */

// =============================================================================
// CONFIG
// =============================================================================
const API_BASE = window.location.hostname === '127.0.0.1' || window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : '';  // Relative path for deployed version

// Crop emoji mapping
const CROP_ICONS = {
    'Rice':         '🌾',
    'Banana':       '🍌',
    'Cacao':        '🍫',
    'Coconut':      '🥥',
    'Durian':       '🍈',
    'Corn':         '🌽',
    'Mango':        '🥭',
    'Papaya':       '🍈',
    'Cassava':      '🫚',
    'Sweet Potato': '🍠',
    'Eggplant':     '🍆',
    'Tomato':       '🍅',
};

// =============================================================================
// LOCALIZATION (EN / Tagalog / Cebuano)
// =============================================================================
const I18N = {
    en: {
        header_subtitle:    'Precision agriculture powered by AI — Smart crop recommendations for farmers in Tagum City, Davao del Norte',
        header_badge:       'AI Model Active • 12 Philippine Crops • 23 Barangays',
        select_location:    'Select Your Location',
        select_location_desc: 'Choose your barangay to auto-fill soil and weather data',
        soil_params_title:  'Soil & Climate Parameters',
        soil_params_desc:   'Auto-filled from your barangay — adjust if you have lab results',
        label_rainfall:     'Rainfall',
        hint_rainfall:      'Monthly average (mm)',
        label_om:           'Organic Matter (OM)',
        hint_om:            '% of soil weight (0–15%)',
        btn_predict:        'Get Crop Recommendation',
        pred_confidence:    'Prediction Confidence',
        shap_title:         '🧠 AI Explanation — Why this crop?',
        shap_positive:      '✅ Factors that support this recommendation:',
        shap_negative:      '⚠️ Limiting factors (consider managing these):',
        shap_no_data:       'Explanation not available for this prediction.',
        alt_crops_label:    'Other Suitable Crops',
        fertilizer_label:   'Fertilizer Advice',
        new_analysis:       'New Analysis',
        econ_title:         'Business ROI Calculator (Per Hectare)',
        econ_chart_title:   'Business Projection (per Hectare)',
        econ_cost:          'Production Cost',
        econ_cost_sub:      'per hectare / season',
        econ_gross:         'Est. Gross Income',
        econ_gross_sub:     'Yield:',
        econ_profit:        'Net Profit',
        econ_profit_sub:    'Farmgate:',
        econ_roi:           'ROI',
        econ_roi_sub:       'Return on Investment',
        econ_harvest:       'Harvest',
        econ_months:        'months',
        econ_seasons:       'seasons/year',
        econ_price:         'Avg Farmgate Price',
        econ_notes:         'Notes',
        econ_source:        'Source',
        fert_rate:          'Rate',
        fert_timing:        'Timing',
        fert_brands:        'Locally Available Brands (Tagum City)',
        fert_tip:           'Pro Tip',
        label_n:            'Nitrogen (N)',
        label_p:            'Phosphorus (P)',
        label_k:            'Potassium (K)',
        label_temp:         'Temperature',
        label_hum:          'Humidity',
        label_ph:           'pH Level',
        hint_mgkg:          '0–200 mg/kg',
        hint_mgkg_k:        '0–250 mg/kg',
        hint_celsius:       'Celsius',
        hint_percent:       'Percentage',
        hint_ph:            'Soil acidity',
        loading_text:       'Analyzing soil conditions with AI model...',
        hero_title:         'AI Recommendation',
        hero_desc:          'Based on your soil and climate conditions',
        footer_built:       'Built for the Technopreneurship Academic Festival 2026',
        live_cond:          'Live Conditions',
        soil_prof:          'Soil Profile',
        disclaimer_html:    '<strong>How does auto-fill work?</strong> Soil values are <em>barangay-level averages</em> from BSWM regional soil classification data — not exact measurements for your specific plot. Soil can vary within the same barangay due to elevation, drainage, and land-use history. These averages give you a <strong>reliable starting point</strong> (±15-20% of actual). If you have lab test results, override the values below for higher accuracy. <span class="disclaimer-future"><i class="fas fa-microchip"></i> Future: IoT soil sensors will provide plot-level precision.</span>',
        msg_prefix:         'Based on your soil and climate conditions,',
        msg_suffix:         'is the recommended crop.',
    },
    tl: {
        header_subtitle:    'Makabagong pagsasaka na pinapagana ng AI — Matalinong rekomendasyon ng pananim para sa mga magsasaka sa Lungsod ng Tagum, Davao del Norte',
        header_badge:       'AI Model Aktibo • 12 Piling Pananim • 23 Barangay',
        select_location:    'Piliin ang Inyong Lokasyon',
        select_location_desc: 'Pumili ng barangay para ma-auto-fill ang lupa at datos ng panahon',
        soil_params_title:  'Mga Parameter ng Lupa at Klima',
        soil_params_desc:   'Napalaman mula sa inyong barangay — baguhin kung mayroon kang resulta ng laboratoryo',
        label_rainfall:     'Pag-ulan',
        hint_rainfall:      'Buwanang average (mm)',
        label_om:           'Organikong Bagay (OM)',
        hint_om:            '% ng timbang ng lupa (0–15%)',
        btn_predict:        'Kumuha ng Rekomendasyon ng Pananim',
        pred_confidence:    'Antas ng Kumpiyansa ng Hula',
        shap_title:         '🧠 Paliwanag ng AI — Bakit ito ang pananim?',
        shap_positive:      '✅ Mga salik na sumusuporta sa rekomendasyong ito:',
        shap_negative:      '⚠️ Mga limitadong salik (pag-isipang pamahalaan ito):',
        shap_no_data:       'Ang paliwanag ay hindi available para sa hulang ito.',
        alt_crops_label:    'Iba Pang Angkop na Pananim',
        fertilizer_label:   'Payo sa Pataba',
        new_analysis:       'Bagong Pagsusuri',
        econ_title:         'Calculator ng ROI sa Negosyo (Kada Ektarya)',
        econ_chart_title:   'Proyekto sa Negosyo (Kada Ektarya)',
        econ_cost:          'Gastos sa Produksyon',
        econ_cost_sub:      'kada ektarya / panahon',
        econ_gross:         'Tinantyang Kabuuang Kita',
        econ_gross_sub:     'Ani:',
        econ_profit:        'Netong Kita',
        econ_profit_sub:    'Farmgate:',
        econ_roi:           'ROI',
        econ_roi_sub:       'Balik sa Pamumuhunan',
        econ_harvest:       'Anihan',
        econ_months:        'buwan',
        econ_seasons:       'panahon/taon',
        econ_price:         'Average na Presyo sa Farmgate',
        econ_notes:         'Mga Tala',
        econ_source:        'Pinagmulan',
        fert_rate:          'Dami',
        fert_timing:        'Oras ng Paglalagay',
        fert_brands:        'Lokal na Available na Tatak (Lungsod ng Tagum)',
        fert_tip:           'Pro Tip',
        label_n:            'Nitrogen (N)',
        label_p:            'Phosphorus (P)',
        label_k:            'Potassium (K)',
        label_temp:         'Temperatura',
        label_hum:          'Halumigmig',
        label_ph:           'Antas ng pH',
        hint_mgkg:          '0–200 mg/kg',
        hint_mgkg_k:        '0–250 mg/kg',
        hint_celsius:       'Celsius',
        hint_percent:       'Porsyento',
        hint_ph:            'Acidity ng lupa',
        loading_text:       'Sinisiyasat ang kondisyon ng lupa gamit ang AI...',
        hero_title:         'Rekomendasyon ng AI',
        hero_desc:          'Batay sa kondisyon ng lupa at klima mo',
        footer_built:       'Ginawa para sa Technopreneurship Academic Festival 2026',
        live_cond:          'Kasulukuyang Panahon',
        soil_prof:          'Profile ng Lupa',
        disclaimer_html:    '<strong>Paano gumagana ang auto-fill?</strong> Ang mga halaga ng lupa ay <em>average sa antas ng barangay</em> mula sa data ng BSWM — hindi eksaktong sukat para sa partikular na lote mo. Maaaring mag-iba ang lupa sa loob ng iisang barangay dahil sa elebasyon at daloy ng tubig. Ang mga average na ito ay nagbibigay ng <strong>maaasahang panimulang punto</strong> (±15-20% ng aktwal). Kung may resulta ka sa lab, palitan ang mga halaga para sa mas tumpak na resulta. <span class="disclaimer-future"><i class="fas fa-microchip"></i> Hinaharap: Ang mga IoT sensor ay magbibigay ng eksaktong katumpakan sa lote.</span>',
        msg_prefix:         'Batay sa kondisyon ng lupa at klima mo, ang',
        msg_suffix:         'ay ang inirerekomendang pananim.',
        'Balanced Nutrients ✅': 'Timbang na Sustansya ✅',
        'Soil nutrient levels are within optimal range. Apply maintenance fertilizer (Complete 14-14-14) at 2–3 bags/ha per cropping season to sustain productivity. Continue monitoring soil health every 2 seasons.': 'Ang antas ng sustansya ay nasa pinakamainam na saklaw. Maglagay ng maintenance na pataba (Complete 14-14-14) ng 2-3 sako kada ektarya upang mapanatili ang ani. Patuloy na suriin ang lupa bawat 2 panahon.',
        '2–3 bags (50 kg) per hectare per season': '2-3 sako (50 kg) kada ektarya bawat panahon',
        'At land preparation + 30 DAT': 'Sa paghahanda ng lupa + 30 araw pagkatanim (DAT)',
        'Any agrivet store in Tagum City': 'Kahit anong agrivet store sa Lungsod ng Tagum',
        'Atlas Agri-Store, Tagum National Highway': 'Atlas Agri-Store, Tagum National Highway',
        'Harbest Agri Center, Arellano Ave, Tagum': 'Harbest Agri Center, Arellano Ave, Tagum',
        'Even balanced soil benefits from annual soil testing. DA Region XI offers free soil testing — contact the Tagum City Agriculture Office at the City Hall for scheduling.': 'Kahit ang timbang na lupa ay nakikinabang sa taunang pagsusuri. Nag-aalok ang DA Region XI ng libreng pagsusuri ng lupa — makipag-ugnayan sa Tagum City Agriculture Office sa City Hall para magpa-iskedyul.',
        'DA Region XI Fertilizer Monitoring, 2024': 'Pagsubaybay sa Pataba ng DA Region XI, 2024',
        'Low Organic Matter (OM < 2.0%)': 'Mababang Organic Matter (OM < 2.0%)',
        'Incorporate vermicast or compost at 2–3 tons/ha before planting. Mulch with rice straw, banana pseudo-stem chippings, or dried leaves. OM builds over 2–3 seasons — commit to a multi-season improvement plan. Low OM reduces water-holding capacity and suppresses beneficial soil microbes.': 'Ihalo ang vermicast o compost na 2-3 tonelada kada ektarya bago magtanim. Maglagay ng mulch gamit ang dayami ng palay, tinadtad na puno ng saging, o tuyong dahon. Ang OM ay naiipon sa loob ng 2-3 panahon. Ang mababang OM ay nakakabawas sa kakayahang mag-imbak ng tubig ng lupa.',
        '2,000–3,000 kg vermicast per hectare': '2,000-3,000 kg vermicast kada ektarya',
        '14–21 days before transplanting (incorporate into soil)': '14-21 araw bago maglipat-tanim (ihalo sa lupa)',
        'DA-HVCDP office, Tagum City Hall compound': 'Opisina ng DA-HVCDP, Tagum City Hall compound',
        'DA Region XI Organic Agriculture office, Davao City': 'Opisina ng DA Region XI Organic Agriculture, Lungsod ng Davao',
        'Local organic cooperatives — ask at barangay halls in Tagum': 'Lokal na kooperatiba ng organiko — magtanong sa mga barangay hall sa Tagum',
        'DA extension offices, UPLB-licensed dealers in Tagum': 'Opisina ng DA extension, mga dealer na lisensyado ng UPLB sa Tagum',
        "Banana pseudo-stem chipping is FREE and abundant around Tagum's plantation areas. TADECO and Lapanday farms often allow collection of organic waste — an easy win for smallholders.": 'Libre at sagana ang mga tadtad na puno ng saging sa paligid ng mga plantasyon sa Tagum. Madalas pumapayag ang TADECO at Lapanday na kolektahin ang mga organikong basura — isang madaling paraan para sa mga maliliit na magsasaka.',
        'DA Organic Agriculture Act RA 10068, DA-HVCDP Tagum organic program': 'DA Organic Agriculture Act RA 10068, programa ng DA-HVCDP Tagum',
    },
    ceb: {
        header_subtitle:    'Precision nga agrikultura nga gipalihok sa AI — Maalamon nga rekomendasyon sa pananom para sa mga mag-uuma sa Dakbayan sa Tagum, Davao del Norte',
        header_badge:       'Aktibo ang AI Model • 12 ka Pananom • 23 ka Barangay',
        select_location:    'Pilia ang Imong Lokasyon',
        select_location_desc: 'Pagpili og barangay aron ma-auto-fill ang yuta ug datos sa panahon',
        soil_params_title:  'Mga Parameter sa Yuta ug Klima',
        soil_params_desc:   'Gi-auto-fill gikan sa imong barangay — usba kung adunay ka resulta sa laboratoryo',
        label_rainfall:     'Ulan',
        hint_rainfall:      'Binuwanang average (mm)',
        label_om:           'Organikong Butang (OM)',
        hint_om:            '% sa timbang sa yuta (0–15%)',
        btn_predict:        'Kuhaon ang Rekomendasyon sa Pananom',
        pred_confidence:    'Antas sa Pagsalig sa Hulaan',
        shap_title:         '🧠 Katin-awan sa AI — Nganong kini nga pananom?',
        shap_positive:      '✅ Mga hinungdan nga nagsuporta sa rekomendasyon:',
        shap_negative:      '⚠️ Mga limitasyon (hunahunaa ang pagdumala niini):',
        shap_no_data:       'Ang katin-awan dili anaa alang sa hulaan.',
        alt_crops_label:    'Uban nga Angay nga Pananom',
        fertilizer_label:   'Tambag sa Abono',
        new_analysis:       'Bag-ong Pagtuki',
        econ_title:         'Calculator sa ROI sa Negosyo (Kada Ektarya)',
        econ_chart_title:   'Proyekto sa Negosyo (Kada Ektarya)',
        econ_cost:          'Gasto sa Produksyon',
        econ_cost_sub:      'kada ektarya / panahon',
        econ_gross:         'Gibanabana nga Tibuok Kita',
        econ_gross_sub:     'Abot:',
        econ_profit:        'Klarong Kita',
        econ_profit_sub:    'Farmgate:',
        econ_roi:           'ROI',
        econ_roi_sub:       'Balik sa Puhunan',
        econ_harvest:       'Pag-ani',
        econ_months:        'ka bulan',
        econ_seasons:       'panahon/tuig',
        econ_price:         'Average nga Presyo sa Farmgate',
        econ_notes:         'Mga Mubo nga Tala',
        econ_source:        'Tinubdan',
        fert_rate:          'Kadaghanon',
        fert_timing:        'Oras sa Pagbutang',
        fert_brands:        'Lokal nga Available nga Brand (Dakbayan sa Tagum)',
        fert_tip:           'Pro Tip',
        label_n:            'Nitrogen (N)',
        label_p:            'Phosphorus (P)',
        label_k:            'Potassium (K)',
        label_temp:         'Temperatura',
        label_hum:          'Kaginhawaan (Humidity)',
        label_ph:           'Ang-ang sa pH',
        hint_mgkg:          '0–200 mg/kg',
        hint_mgkg_k:        '0–250 mg/kg',
        hint_celsius:       'Celsius',
        hint_percent:       'Porsyento',
        hint_ph:            'Kaaslom sa yuta',
        loading_text:       'Gisusi ang kondisyon sa yuta gamit ang AI...',
        hero_title:         'Rekomendasyon sa AI',
        hero_desc:          'Base sa kondisyon sa imong yuta ug klima',
        footer_built:       'Gihimo para sa Technopreneurship Academic Festival 2026',
        live_cond:          'Kasamtangang Panahon',
        soil_prof:          'Profile sa Yuta',
        disclaimer_html:    '<strong>Giunsa pag-obra ang auto-fill?</strong> Ang mga value sa yuta kay <em>average sa matag barangay</em> gikan sa datos sa BSWM — dili eksakto sa imong kaugalingong yuta. Ang yuta pwede magkalahi sa usa ka barangay tungod sa porma sa yuta ug agianan sa tubig. Kining mga average muhatag nimog <strong>kasaligan nga basehan</strong> (±15-20% sa tinuod). Kung duna kay resulta sa lab, usba ang mga value ubos para mas ensakto. <span class="disclaimer-future"><i class="fas fa-microchip"></i> Sa Unahan: Ang mga IoT sensor muhatag og mas eksaktong datos sa matag luna.</span>',
        msg_prefix:         'Base sa kondisyon sa imong yuta ug klima, ang',
        msg_suffix:         'maoy girekomenda nga pananom.',
        'Balanced Nutrients ✅': 'Balanse nga Nutrisyon ✅',
        'Soil nutrient levels are within optimal range. Apply maintenance fertilizer (Complete 14-14-14) at 2–3 bags/ha per cropping season to sustain productivity. Continue monitoring soil health every 2 seasons.': 'Ang lebel sa nutrisyon anaa sa sakto nga range. Pagbutang og maintenance nga abono (Complete 14-14-14) og 2-3 ka sako kada ektarya kada panahon sa pagtanom aron mapadayon ang ani. Padayon sa pagsusi sa yuta kada 2 ka panahon.',
        '2–3 bags (50 kg) per hectare per season': '2-3 ka sako (50 kg) kada ektarya kada panahon',
        'At land preparation + 30 DAT': 'Atol sa pagpangandam sa yuta + 30 adlaw human tanom (DAT)',
        'Any agrivet store in Tagum City': 'Bisan asang agrivet store sa Dakbayan sa Tagum',
        'Atlas Agri-Store, Tagum National Highway': 'Atlas Agri-Store, Tagum National Highway',
        'Harbest Agri Center, Arellano Ave, Tagum': 'Harbest Agri Center, Arellano Ave, Tagum',
        'Even balanced soil benefits from annual soil testing. DA Region XI offers free soil testing — contact the Tagum City Agriculture Office at the City Hall for scheduling.': 'Bisan ang balanse nga yuta makabenepisyo sa tinuig nga pagsusi. Ang DA Region XI nagatanyag og libre nga pagsusi sa yuta — kontaka ang Tagum City Agriculture Office sa City Hall para magpa-iskedyul.',
        'DA Region XI Fertilizer Monitoring, 2024': 'Pag-monitor sa Abono sa DA Region XI, 2024',
        'Low Organic Matter (OM < 2.0%)': 'Gamay nga Organic Matter (OM < 2.0%)',
        'Incorporate vermicast or compost at 2–3 tons/ha before planting. Mulch with rice straw, banana pseudo-stem chippings, or dried leaves. OM builds over 2–3 seasons — commit to a multi-season improvement plan. Low OM reduces water-holding capacity and suppresses beneficial soil microbes.': 'Isagol ang vermicast o compost sa 2-3 ka tonelada kada ektarya sa dili pa magtanom. Pagbutang og mulch gamit ang dagami, tinagod nga punoan sa saging, o uga nga dahon. Ang OM magtukod sa sulod sa 2-3 ka panahon. Ang gamay nga OM magpakunhod sa abilidad sa yuta nga magpabilin og tubig.',
        '2,000–3,000 kg vermicast per hectare': '2,000-3,000 kg vermicast kada ektarya',
        '14–21 days before transplanting (incorporate into soil)': '14-21 ka adlaw sa dili pa magbalhin-tanom (isagol sa yuta)',
        'DA-HVCDP office, Tagum City Hall compound': 'Opisina sa DA-HVCDP, Tagum City Hall compound',
        'DA Region XI Organic Agriculture office, Davao City': 'Opisina sa DA Region XI Organic Agriculture, Dakbayan sa Davao',
        'Local organic cooperatives — ask at barangay halls in Tagum': 'Lokal nga kooperatiba nga organiko — pangutana sa mga barangay hall sa Tagum',
        'DA extension offices, UPLB-licensed dealers in Tagum': 'Opisina sa DA extension, mga dealer nga lisensyado sa UPLB sa Tagum',
        "Banana pseudo-stem chipping is FREE and abundant around Tagum's plantation areas. TADECO and Lapanday farms often allow collection of organic waste — an easy win for smallholders.": 'Libre ug daghan ang mga tinagod nga punoan sa saging sa palibot sa mga plantasyon sa Tagum. Sagad motugot ang TADECO ug Lapanday nga kolektahon ang mga organikong basura — usa ka sayon nga paagi para sa mga gagmayng mag-uuma.',
        'DA Organic Agriculture Act RA 10068, DA-HVCDP Tagum organic program': 'DA Organic Agriculture Act RA 10068, programa sa DA-HVCDP Tagum',
    },
};

let currentLang = localStorage.getItem('luntiai-lang') || 'en';

function t(key) {
    return I18N[currentLang]?.[key] || I18N['en'][key] || key;
}

function initLocalization() {
    // Apply saved language
    applyLang(currentLang);
}

function applyLang(lang) {
    currentLang = lang;
    localStorage.setItem('luntiai-lang', lang);

    // Update all data-i18n elements (text)
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (I18N[lang]?.[key]) el.textContent = I18N[lang][key];
    });

    // Update all data-i18n-html elements (inner HTML)
    document.querySelectorAll('[data-i18n-html]').forEach(el => {
        const key = el.getAttribute('data-i18n-html');
        if (I18N[lang]?.[key]) el.innerHTML = I18N[lang][key];
    });

    // Update active button state
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.lang === lang);
    });

    // If results are currently showing, re-render them completely
    if (window.lastResult && !document.getElementById('resultsSection').classList.contains('hidden')) {
        // Destroy existing chart to prevent canvas overlap issues
        if (window.econChartInstance) {
            window.econChartInstance.destroy();
        }
        renderResults(window.lastResult);
    }
}

// =============================================================================
// DOM REFERENCES
// =============================================================================
const barangaySelect   = document.getElementById('barangaySelect');
const autoDataSection  = document.getElementById('autoDataSection');
const weatherDataGrid  = document.getElementById('weatherDataGrid');
const soilDataGrid     = document.getElementById('soilDataGrid');
const weatherSource    = document.getElementById('weatherSource');
const soilTypeLabel    = document.getElementById('soilType');
const cropForm         = document.getElementById('cropForm');
const submitBtn        = document.getElementById('submitBtn');
const loadingOverlay   = document.getElementById('loadingOverlay');
const resultsSection   = document.getElementById('resultsSection');
const resultHero       = document.getElementById('resultHero');
const altCropsSection  = document.getElementById('altCropsSection');
const shapSection      = document.getElementById('shapSection');
const fertilizerSection= document.getElementById('fertilizerSection');

let probChartInstance = null;

// =============================================================================
// INITIALIZATION
// =============================================================================
document.addEventListener('DOMContentLoaded', async () => {
    initTheme();
    initLocalization();
    await loadBarangays();
    checkBackendHealth();

    // Language toggle buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => applyLang(btn.dataset.lang));
    });
});

async function loadBarangays() {
    try {
        const res = await fetch(`${API_BASE}/barangays`);
        if (!res.ok) throw new Error('Failed to load barangays');
        const data = await res.json();

        const names = Object.keys(data.barangays).sort();
        names.forEach(name => {
            const opt = document.createElement('option');
            opt.value = name;
            opt.textContent = name;
            barangaySelect.appendChild(opt);
        });

        // Store barangay data globally
        window._barangayData = data.barangays;
    } catch (err) {
        console.warn('Could not load barangays from API:', err.message);
        showToast('Backend not connected. Using offline mode.', 'info');
        loadBarangaysFallback();
    }
}

function loadBarangaysFallback() {
    // Hardcoded fallback list
    const names = [
        "Apokon", "Bincungan", "Busaon", "Canocotan", "Cuambogan",
        "La Filipina", "Liboganon", "Madaum", "Magdum",
        "Magugpo East", "Magugpo North", "Magugpo Poblacion",
        "Magugpo South", "Magugpo West", "Mankilam", "New Balamban",
        "Nueva Fuerza", "Pagsabangan", "Pandapan", "San Agustin",
        "San Isidro", "San Miguel", "Visayan Village"
    ];
    names.forEach(name => {
        const opt = document.createElement('option');
        opt.value = name;
        opt.textContent = name;
        barangaySelect.appendChild(opt);
    });
}

async function checkBackendHealth() {
    try {
        const res = await fetch(`${API_BASE}/health`);
        if (res.ok) {
            const health = await res.json();
            console.log('✅ Backend connected:', health);
        }
    } catch (err) {
        console.warn('⚠ Backend not reachable:', err.message);
    }
}

// =============================================================================
// BARANGAY SELECTION — AUTO-FILL DATA
// =============================================================================
barangaySelect.addEventListener('change', async () => {
    const name = barangaySelect.value;
    if (!name) {
        autoDataSection.classList.add('hidden');
        return;
    }

    try {
        // Fetch weather + soil from API
        const res = await fetch(`${API_BASE}/weather/${encodeURIComponent(name)}`);
        if (!res.ok) throw new Error('API error');
        const data = await res.json();

        renderWeatherData(data.weather);
        renderSoilData(data.soil, name);
        autoFillForm(data);

        autoDataSection.classList.remove('hidden');
    } catch (err) {
        console.warn('Weather API fallback:', err.message);

        // Use local data if API unavailable
        if (window._barangayData && window._barangayData[name]) {
            const brgy = window._barangayData[name];
            renderSoilData({
                N: brgy.N, P: brgy.P, K: brgy.K,
                pH: brgy.pH, OM: brgy.OM, soil_type: brgy.soil_type
            }, name);
            renderWeatherFallback();
            autoFillFormFromLocal(brgy);
            autoDataSection.classList.remove('hidden');
        }
    }
});

function renderWeatherData(weather) {
    weatherSource.textContent = weather.source || '';
    weatherDataGrid.innerHTML = `
        <div class="data-card">
            <span class="data-card-icon">🌡️</span>
            <div class="data-card-label">Temperature</div>
            <div class="data-card-value">${weather.temp}<span class="data-card-unit">°C</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon">💧</span>
            <div class="data-card-label">Humidity</div>
            <div class="data-card-value">${weather.humidity}<span class="data-card-unit">%</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon">🌧️</span>
            <div class="data-card-label">Rainfall</div>
            <div class="data-card-value">${weather.rainfall_estimate}<span class="data-card-unit">mm/mo</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon">☁️</span>
            <div class="data-card-label">Conditions</div>
            <div class="data-card-value" style="font-size: 1rem;">${weather.description}</div>
        </div>
    `;
}

function renderWeatherFallback() {
    weatherSource.textContent = 'PAGASA Climate Normals';
    weatherDataGrid.innerHTML = `
        <div class="data-card">
            <span class="data-card-icon">🌡️</span>
            <div class="data-card-label">Temperature</div>
            <div class="data-card-value">27.5<span class="data-card-unit">°C</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon">💧</span>
            <div class="data-card-label">Humidity</div>
            <div class="data-card-value">82<span class="data-card-unit">%</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon">🌧️</span>
            <div class="data-card-label">Rainfall</div>
            <div class="data-card-value">175<span class="data-card-unit">mm/mo</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon">☁️</span>
            <div class="data-card-label">Conditions</div>
            <div class="data-card-value" style="font-size: 1rem;">Tropical Wet</div>
        </div>
    `;
}

function renderSoilData(soil, barangayName) {
    soilTypeLabel.textContent = `${soil.soil_type || 'Loam'} — ${barangayName}`;
    soilDataGrid.innerHTML = `
        <div class="data-card">
            <span class="data-card-icon" style="color: #ef4444;">⚛</span>
            <div class="data-card-label">Nitrogen (N)</div>
            <div class="data-card-value">${soil.N}<span class="data-card-unit">mg/kg</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon" style="color: #f97316;">◉</span>
            <div class="data-card-label">Phosphorus (P)</div>
            <div class="data-card-value">${soil.P}<span class="data-card-unit">mg/kg</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon" style="color: #a855f7;">◉</span>
            <div class="data-card-label">Potassium (K)</div>
            <div class="data-card-value">${soil.K}<span class="data-card-unit">mg/kg</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon" style="color: #8b5cf6;">⚗</span>
            <div class="data-card-label">pH Level</div>
            <div class="data-card-value">${soil.pH || soil.ph}</div>
        </div>
        <div class="data-card">
            <span class="data-card-icon" style="color: #a16207;">🌿</span>
            <div class="data-card-label">Organic Matter</div>
            <div class="data-card-value">${soil.OM ?? soil.om ?? '—'}<span class="data-card-unit">%</span></div>
        </div>
    `;
}

function autoFillForm(data) {
    document.getElementById('inputN').value        = data.soil.N;
    document.getElementById('inputP').value        = data.soil.P;
    document.getElementById('inputK').value        = data.soil.K;
    document.getElementById('inputPH').value       = data.soil.pH || data.soil.ph;
    document.getElementById('inputOM').value       = data.soil.OM ?? data.soil.om ?? '';
    document.getElementById('inputTemp').value     = data.weather.temp;
    document.getElementById('inputHumidity').value = data.weather.humidity;
    document.getElementById('inputRainfall').value = data.weather.rainfall_estimate;
}

function autoFillFormFromLocal(brgy) {
    document.getElementById('inputN').value        = brgy.N;
    document.getElementById('inputP').value        = brgy.P;
    document.getElementById('inputK').value        = brgy.K;
    document.getElementById('inputPH').value       = brgy.pH;
    document.getElementById('inputOM').value       = brgy.OM ?? '';
    document.getElementById('inputTemp').value     = 27.5;
    document.getElementById('inputHumidity').value = 82;
    document.getElementById('inputRainfall').value = 175;
}

// =============================================================================
// FORM SUBMISSION — PREDICTION
// =============================================================================
cropForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    e.stopPropagation();

    const formData = new FormData(cropForm);
    const payload = {
        N:           parseFloat(formData.get('N')),
        P:           parseFloat(formData.get('P')),
        K:           parseFloat(formData.get('K')),
        temperature: parseFloat(formData.get('temperature')),
        humidity:    parseFloat(formData.get('humidity')),
        ph:          parseFloat(formData.get('ph')),
        rainfall:    parseFloat(formData.get('rainfall')),
        OM:          parseFloat(formData.get('OM')),
        barangay:    barangaySelect.value || null,
    };

    // Validate
    for (const [key, val] of Object.entries(payload)) {
        if (key === 'barangay') continue;
        if (isNaN(val) || val === null) {
            showToast(`Please fill in all fields. "${key}" is missing.`, 'error');
            return;
        }
    }

    // Show loading
    showLoading();
    resultsSection.classList.add('hidden');

    try {
        const res = await fetch(`${API_BASE}/predict`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const result = await res.json();
        hideLoading();

        if (res.ok) {
            renderResults(result);
        } else {
            showToast(result.detail || 'Prediction failed', 'error');
        }
    } catch (err) {
        hideLoading();
        showToast(`Network error: ${err.message}. Is the backend running?`, 'error');
    }
});

// =============================================================================
// RESULTS RENDERING
// =============================================================================
function renderResults(result) {
    window.lastResult = result; // Save for language toggles

    const icon = CROP_ICONS[result.best_crop] || '🌱';
    const confColor = result.confidence >= 80 ? 'var(--green-600)' :
                      result.confidence >= 60 ? 'var(--earth-600)' : '#f59e0b';
    
    // Construct localized message
    const locMsg = `${t('msg_prefix')} <strong>${result.best_crop}</strong> ${t('msg_suffix')}`;

    resultHero.innerHTML = `
        <div class="result-hero">
            <div style="font-size: 3.5rem; margin-bottom: 8px;">${icon}</div>
            <div class="result-crop-name">${result.best_crop}</div>
            <p style="color: var(--text-secondary); margin: 8px 0; font-size: 1.05rem; line-height: 1.5;">${locMsg}</p>
            <div class="result-confidence" style="color: ${confColor}; border-color: ${confColor}40;">
                <i class="fas fa-bullseye"></i> ${(result.confidence).toFixed(2)}% <span data-i18n="pred_confidence">${t('pred_confidence')}</span>
            </div>
        </div>
    `;

    // Alternative crops
    const alts = (result.top_predictions || []).filter(p => p.crop !== result.best_crop).slice(0, 4);
    if (alts.length > 0) {
        altCropsSection.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 20px; margin-bottom: 12px;">
                <i class="fas fa-list-ul" style="color: var(--green-400);"></i>
                <span style="font-weight: 600; color: var(--text-primary); font-size: 0.9rem;">${t('alt_crops_label')}</span>
            </div>
            <div class="alt-crops-grid">
                ${alts.map((a, i) => `
                    <div class="alt-crop-card">
                        <div class="alt-crop-rank">${i + 2}</div>
                        <div>
                            <div class="alt-crop-name">${CROP_ICONS[a.crop] || '🌱'} ${a.crop}</div>
                            <div class="alt-crop-prob">${a.probability}% match</div>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
    } else {
        altCropsSection.innerHTML = '';
    }

    // SHAP Explanation
    renderShapExplanation(result.shap_explanation);

    // Fertilizer recommendations
    const ferts = result.fertilizer_recommendations || [];
    if (ferts.length > 0) {
        fertilizerSection.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 20px; margin-bottom: 12px;">
                <i class="fas fa-flask" style="color: var(--earth-400);"></i>
                <span style="font-weight: 600; color: var(--text-primary); font-size: 0.9rem;">${t('fertilizer_label')}</span>
            </div>
            ${ferts.map(f => {
                let brandsHtml = '';
                if (f.brands && Array.isArray(f.brands)) {
                    brandsHtml = `<ul class="fertilizer-brands-list">` + 
                        f.brands.map(b => `<li><strong>${b.name}</strong> — ₱${b.price_php} / ${b.per}<br><span class="fert-where"><i class="fas fa-map-marker-alt"></i> ${t(b.where)}</span></li>`).join('') +
                        `</ul>`;
                } else if (f.local_brand) {
                    brandsHtml = `<div class="fertilizer-brand"><i class="fas fa-store"></i> ${t(f.local_brand)}</div>`;
                }
                
                return `
                <div class="fertilizer-card urgency-${f.urgency || 'low'}">
                    <div class="fertilizer-title">${f.icon || ''} ${t(f.condition)}</div>
                    <div class="fertilizer-text">${t(f.recommendation)}</div>
                    
                    ${f.rate ? `<div class="fert-detail"><strong><i class="fas fa-balance-scale"></i> ${t('fert_rate')}:</strong> ${t(f.rate)}</div>` : ''}
                    ${f.timing ? `<div class="fert-detail"><strong><i class="fas fa-clock"></i> ${t('fert_timing')}:</strong> ${t(f.timing)}</div>` : ''}
                    
                    <div class="fert-brands-title">${t('fert_brands')}:</div>
                    ${brandsHtml}
                    
                    ${f.pro_tip ? `<div class="fert-pro-tip"><strong>💡 ${t('fert_tip')}:</strong> ${t(f.pro_tip)}</div>` : ''}
                    ${f.da_source ? `<div class="fert-source"><i class="fas fa-info-circle"></i> ${t('econ_source')}: ${t(f.da_source)}</div>` : ''}
                </div>
                `;
            }).join('')}
        `;
    } else {
        fertilizerSection.innerHTML = '';
    }

    // Business & ROI Economics
    const econSection = document.getElementById('economicsSection');
    const econChartContainer = document.getElementById('econChartContainer');
    
    if (result.crop_economics) {
        const econ = result.crop_economics;
        
        // Compute Gross Income and ROI
        const grossIncome = econ.avg_yield_kg_ha * econ.farmgate_price_php_kg;
        const netProfit = grossIncome - econ.production_cost_php;
        const roi = (netProfit / econ.production_cost_php) * 100;
        
        // Format Currency
        const fmtPHP = (val) => new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP', minimumFractionDigits: 0 }).format(val);
        const fmtNum = (val) => new Intl.NumberFormat('en-US').format(val);
        
        econSection.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px; margin-top: 24px; margin-bottom: 12px;">
                <i class="fas fa-calculator" style="color: var(--green-400);"></i>
                <span style="font-weight: 600; color: var(--text-primary); font-size: 0.9rem;">${t('econ_title')}</span>
            </div>
            
            <div class="econ-card">
                <div class="econ-grid">
                    <div class="econ-stat">
                        <div class="econ-label">${t('econ_cost')}</div>
                        <div class="econ-value cost">${fmtPHP(econ.production_cost_php)}</div>
                        <div class="econ-sub">${t('econ_cost_sub')}</div>
                    </div>
                    <div class="econ-stat">
                        <div class="econ-label">${t('econ_gross')}</div>
                        <div class="econ-value gross">${fmtPHP(grossIncome)}</div>
                        <div class="econ-sub">${t('econ_gross_sub')} ${fmtNum(econ.avg_yield_kg_ha)} kg/ha</div>
                    </div>
                    <div class="econ-stat">
                        <div class="econ-label">${t('econ_profit')}</div>
                        <div class="econ-value profit">${fmtPHP(netProfit)}</div>
                        <div class="econ-sub">${t('econ_profit_sub')} ₱${econ.farmgate_price_php_kg}/kg</div>
                    </div>
                    <div class="econ-stat roi-stat">
                        <div class="econ-label">${t('econ_roi')}</div>
                        <div class="econ-value roi">${roi.toFixed(1)}%</div>
                        <div class="econ-sub">${t('econ_roi_sub')}</div>
                    </div>
                </div>
                
                <div class="econ-details">
                    <div><i class="fas fa-calendar-alt"></i> <strong>${t('econ_harvest')}:</strong> ${econ.harvest_months} ${t('econ_months')} (${econ.cropping_seasons_per_year} ${t('econ_seasons')})</div>
                    <div><i class="fas fa-tag"></i> <strong>${t('econ_price')}:</strong> ₱${econ.farmgate_price_php_kg}/kg</div>
                    ${econ.notes ? `<div><i class="fas fa-info-circle"></i> <strong>${t('econ_notes')}:</strong> ${econ.notes}</div>` : ''}
                    <div class="fert-source" style="margin-top: 8px;">${t('econ_source')}: ${econ.source}</div>
                </div>
            </div>
        `;
        
        // Show and render chart
        econChartContainer.classList.remove('hidden');
        renderEconChart(econ.production_cost_php, netProfit, grossIncome);
        
    } else {
        if (econSection) econSection.innerHTML = '';
        if (econChartContainer) econChartContainer.classList.add('hidden');
    }

    // Probability Chart
    renderChart(result.top_predictions || []);

    // Show results
    resultsSection.classList.remove('hidden');
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function renderShapExplanation(shap) {
    if (!shapSection) return;
    if (!shap) {
        shapSection.innerHTML = '';
        return;
    }

    const positives = shap.top_positive || [];
    const negatives = shap.top_negative || [];

    const featureLabels = {
        'N': 'Nitrogen (N)', 'P': 'Phosphorus (P)', 'K': 'Potassium (K)',
        'Temp': 'Temperature', 'Humidity': 'Humidity', 'pH': 'pH Level',
        'Rainfall': 'Rainfall', 'OM': 'Organic Matter',
    };

    const fmt = (v) => (v >= 0 ? '+' : '') + v.toFixed(4);

    const posHTML = positives.length > 0
        ? positives.map(f => `
            <div class="shap-bar-row">
                <span class="shap-feature">${featureLabels[f.feature] || f.feature}</span>
                <div class="shap-bar-wrap">
                    <div class="shap-bar shap-pos" style="width:${Math.min(Math.abs(f.value) * 1200, 100)}%"></div>
                </div>
                <span class="shap-val pos">${fmt(f.value)}</span>
            </div>`).join('')
        : `<div class="shap-none">—</div>`;

    const negHTML = negatives.length > 0
        ? negatives.map(f => `
            <div class="shap-bar-row">
                <span class="shap-feature">${featureLabels[f.feature] || f.feature}</span>
                <div class="shap-bar-wrap">
                    <div class="shap-bar shap-neg" style="width:${Math.min(Math.abs(f.value) * 1200, 100)}%"></div>
                </div>
                <span class="shap-val neg">${fmt(f.value)}</span>
            </div>`).join('')
        : `<div class="shap-none">—</div>`;

    shapSection.innerHTML = `
        <div class="shap-card" style="margin-top: 20px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:14px;">
                <i class="fas fa-brain" style="color: var(--green-400);"></i>
                <span style="font-weight:700; color:var(--text-primary); font-size:0.95rem;">${t('shap_title')}</span>
            </div>
            <p class="shap-label">${t('shap_positive')}</p>
            ${posHTML}
            <p class="shap-label" style="margin-top:12px;">${t('shap_negative')}</p>
            ${negHTML}
        </div>
    `;
}

function renderChart(predictions) {
    const ctx = document.getElementById('probChart');
    if (!ctx) return;

    if (probChartInstance) {
        probChartInstance.destroy();
    }

    const labels = predictions.map(p => p.crop);
    const data = predictions.map(p => p.probability);
    
    // Check if light mode is active for chart colors
    const isLightMode = document.documentElement.getAttribute('data-theme') === 'light';
    const textColor = isLightMode ? '#44403c' : '#a5d6a7';
    const gridColor = isLightMode ? 'rgba(0,0,0,0.05)' : 'rgba(255, 255, 255, 0.1)';

    probChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Match Probability (%)',
                data: data,
                backgroundColor: 'rgba(34, 197, 94, 0.6)',
                borderColor: 'rgba(34, 197, 94, 1)',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: ctx => `${ctx.parsed.y}%`
                    },
                    backgroundColor: 'rgba(20, 40, 25, 0.9)',
                    borderColor: 'rgba(34, 197, 94, 0.3)',
                    borderWidth: 1,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: gridColor },
                    ticks: { color: textColor, font: { family: 'Inter' } }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: textColor, font: { family: 'Inter', size: 11 } }
                }
            }
        }
    });
}

let econChartInstance = null;

function renderEconChart(cost, profit, gross) {
    const ctx = document.getElementById('econChart');
    if (!ctx) return;

    if (econChartInstance) {
        econChartInstance.destroy();
    }
    
    const isLightMode = document.documentElement.getAttribute('data-theme') === 'light';
    const textColor = isLightMode ? '#44403c' : '#a5d6a7';
    const gridColor = isLightMode ? 'rgba(0,0,0,0.05)' : 'rgba(255, 255, 255, 0.1)';

    econChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Per Hectare Estimates'],
            datasets: [
                {
                    label: 'Production Cost',
                    data: [cost],
                    backgroundColor: 'rgba(245, 158, 11, 0.7)',
                    borderColor: 'rgba(245, 158, 11, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                },
                {
                    label: 'Net Profit',
                    data: [profit],
                    backgroundColor: 'rgba(34, 197, 94, 0.7)',
                    borderColor: 'rgba(34, 197, 94, 1)',
                    borderWidth: 1,
                    borderRadius: 4
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    position: 'top',
                    labels: { color: textColor, font: { family: 'Inter' } }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) label += ': ';
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP', minimumFractionDigits: 0 }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: gridColor },
                    ticks: { 
                        color: textColor,
                        font: { family: 'Inter' },
                        callback: function(value) {
                            return '₱' + new Intl.NumberFormat('en-US', { notation: "compact", compactDisplay: "short" }).format(value);
                        }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: textColor, font: { family: 'Inter' } }
                }
            }
        }
    });
}


// =============================================================================
// UI UTILITIES
// =============================================================================
function showLoading() {
    loadingOverlay.classList.add('active');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
    submitBtn.disabled = false;
    submitBtn.innerHTML = '<i class="fas fa-seedling"></i> Get Crop Recommendation';
}

function resetAll() {
    cropForm.reset();
    barangaySelect.value = '';
    autoDataSection.classList.add('hidden');
    resultsSection.classList.add('hidden');
    if (probChartInstance) {
        probChartInstance.destroy();
        probChartInstance = null;
    }
    document.getElementById('header').scrollIntoView({ behavior: 'smooth' });
}

function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `<i class="fas fa-${type === 'error' ? 'exclamation-circle' : type === 'success' ? 'check-circle' : 'info-circle'}"></i> ${message}`;
    document.body.appendChild(toast);
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s ease-out reverse';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

// Global error handler
window.addEventListener('error', (event) => {
    try { hideLoading(); } catch(_) {}
    const msg = event?.error?.message || event?.message || 'Unexpected error';
    showToast(`Error: ${msg}`, 'error');
});

// =============================================================================
// THEME TOGGLE (Dark / Light)
// =============================================================================
function initTheme() {
    const saved = localStorage.getItem('luntiai-theme');
    if (saved === 'light') {
        document.documentElement.setAttribute('data-theme', 'light');
        updateThemeIcon('light');
    } else {
        document.documentElement.removeAttribute('data-theme');
        updateThemeIcon('dark');
    }
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    if (theme === 'light') {
        icon.className = 'fas fa-moon';
    } else {
        icon.className = 'fas fa-sun';
    }
}

document.getElementById('themeToggle')?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    if (current === 'light') {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('luntiai-theme', 'dark');
        updateThemeIcon('dark');
    } else {
        document.documentElement.setAttribute('data-theme', 'light');
        localStorage.setItem('luntiai-theme', 'light');
        updateThemeIcon('light');
    }

    // Re-render chart if visible so colors adapt
    if (probChartInstance) {
        const data = probChartInstance.data;
        probChartInstance.destroy();
        probChartInstance = null;
        // Rebuild from stored predictions
        const predictions = data.labels.map((label, i) => ({
            crop: label,
            probability: data.datasets[0].data[i],
        }));
        renderChart(predictions);
    }
});
