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
    ? 'http://localhost:8080'
    : '';  // Relative path for deployed version
const AUTH_TOKEN_KEY = 'luntiai-token';
const AUTH_USER_KEY = 'luntiai-user';
const AUTH_QUOTA_KEY = 'luntiai-quota';

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

const CROP_ICON_CLASSES = {
    'Rice': 'fa-wheat-awn',
    'Banana': 'fa-seedling',
    'Cacao': 'fa-seedling',
    'Coconut': 'fa-tree',
    'Durian': 'fa-seedling',
    'Corn': 'fa-wheat-awn',
    'Mango': 'fa-leaf',
    'Papaya': 'fa-leaf',
    'Cassava': 'fa-carrot',
    'Sweet Potato': 'fa-carrot',
    'Eggplant': 'fa-seedling',
    'Tomato': 'fa-apple-whole',
};

// =============================================================================
// LOCALIZATION (EN / Tagalog / Cebuano)
// =============================================================================
const I18N = {
    en: {
        header_subtitle:    'Barangay-level crop recommendations for Tagum City.',
        header_badge:       'AI Model Active • 12 Philippine Crops • 23 Barangays',
        select_location:    'Select Your Location',
        select_location_desc: 'Select a Tagum barangay to auto-fill local soil and weather data.',
        soil_params_title:  'Soil & Climate Parameters',
        soil_params_desc:   'Auto-filled from your barangay — adjust if you have lab results',
        label_rainfall:     'Rainfall',
        hint_rainfall:      'Monthly average (mm)',
        label_om:           'Organic Matter (OM)',
        hint_om:            '% of soil weight (0–15%)',
        btn_predict:        'Get Crop Recommendation',
        pred_confidence:    'Prediction Confidence',
        shap_title:         'AI Explanation — Why this crop?',
        shap_positive:      'Factors that support this recommendation:',
        shap_negative:      'Limiting factors to manage:',
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
        scroll_explore:     'Explore below',
        live_cond:          'Live Conditions',
        soil_prof:          'Soil Profile',
        disclaimer_html:    '<strong>How does auto-fill work?</strong> Soil values are barangay-level averages from BSWM regional soil classification data, not exact measurements for a specific plot. Soil can vary within one barangay due to elevation, drainage, and land-use history. If you have lab test results, override the values for higher accuracy.',
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
        scroll_explore:     'I-explore sa ibaba',
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
        scroll_explore:     'Tan-awa sa ubos',
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
const accountControls  = document.getElementById('accountControls');
const quotaPanel       = document.getElementById('quotaPanel');
const authModal        = document.getElementById('authModal');
const accountModal     = document.getElementById('accountModal');
const loginForm        = document.getElementById('loginForm');
const registerForm     = document.getElementById('registerForm');
const redeemForm       = document.getElementById('redeemForm');
const accountSummary   = document.getElementById('accountSummary');
const historyList      = document.getElementById('historyList');
const resultsLockNotice = document.getElementById('resultsLockNotice');
const economicsSection = document.getElementById('economicsSection');
const econChartContainer = document.getElementById('econChartContainer');
const probabilityChartSection = document.getElementById('probabilityChartSection');

let probChartInstance = null;
let currentSession = {
    user: readJSON(AUTH_USER_KEY),
    quota: readJSON(AUTH_QUOTA_KEY),
};
let lastFocusedElement = null;

function readJSON(key) {
    try {
        const raw = localStorage.getItem(key);
        return raw ? JSON.parse(raw) : null;
    } catch (_) {
        return null;
    }
}

function getToken() {
    return localStorage.getItem(AUTH_TOKEN_KEY);
}

function setSession(data) {
    if (data.access_token) {
        localStorage.setItem(AUTH_TOKEN_KEY, data.access_token);
    }
    currentSession = {
        user: data.user || currentSession.user,
        quota: data.quota || currentSession.quota,
    };
    if (currentSession.user) localStorage.setItem(AUTH_USER_KEY, JSON.stringify(currentSession.user));
    if (currentSession.quota) localStorage.setItem(AUTH_QUOTA_KEY, JSON.stringify(currentSession.quota));
    renderAuthState();
}

function clearSession() {
    localStorage.removeItem(AUTH_TOKEN_KEY);
    localStorage.removeItem(AUTH_USER_KEY);
    localStorage.removeItem(AUTH_QUOTA_KEY);
    currentSession = { user: null, quota: null };
    renderAuthState();
}

function authHeaders(extra = {}) {
    const token = getToken();
    return {
        ...extra,
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
}

async function authFetch(path, options = {}) {
    const headers = authHeaders(options.headers || {});
    const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
    if (res.status === 401) {
        clearSession();
    }
    return res;
}

function formatResetTime(value) {
    if (!value) return 'tomorrow';
    try {
        return new Intl.DateTimeFormat('en-PH', {
            hour: 'numeric',
            minute: '2-digit',
            month: 'short',
            day: 'numeric',
        }).format(new Date(value));
    } catch (_) {
        return 'tomorrow';
    }
}

function quotaLabel(quota = currentSession.quota, user = currentSession.user) {
    if (!user) return '3 free analyses/day';
    if (user.tier === 'premium' || quota?.remaining === -1) return 'Unlimited analyses';
    const remaining = Math.max(Number(quota?.remaining ?? 0), 0);
    return `${remaining} free ${remaining === 1 ? 'analysis' : 'analyses'} left`;
}

function isPremiumUser(user = currentSession.user, quota = currentSession.quota) {
    return Boolean(user && (user.tier === 'premium' || quota?.remaining === -1));
}

function isQuotaExhausted(user = currentSession.user, quota = currentSession.quota) {
    if (!user || isPremiumUser(user, quota)) return false;
    return Math.max(Number(quota?.remaining ?? 0), 0) <= 0;
}

function getResultAccessMode() {
    if (!currentSession.user) return 'signed-out';
    if (isPremiumUser()) return 'premium';
    if (isQuotaExhausted()) return 'locked';
    return 'free';
}

function getPremiumSections() {
    return Array.from(document.querySelectorAll('[data-premium-section]'));
}

function updateSubmitState() {
    if (!submitBtn) return;
    const accessMode = getResultAccessMode();
    submitBtn.classList.toggle('quota-locked', accessMode === 'locked');
    submitBtn.disabled = false;
    submitBtn.innerHTML = accessMode === 'locked'
        ? '<i class="fas fa-lock"></i> Unlock premium to analyze'
        : `<i class="fas fa-magnifying-glass-chart"></i> ${t('btn_predict')}`;
}

function applyResultAccessState(accessMode = getResultAccessMode()) {
    if (!resultsSection) return;

    resultsSection.classList.remove('access-free', 'access-locked', 'access-premium');
    if (accessMode === 'free') resultsSection.classList.add('access-free');
    if (accessMode === 'locked') resultsSection.classList.add('access-locked');
    if (accessMode === 'premium') resultsSection.classList.add('access-premium');

    getPremiumSections().forEach(section => {
        const hasContent = section.innerHTML.trim() !== '' && !section.classList.contains('hidden');
        section.classList.toggle('premium-locked', accessMode === 'free' && hasContent);
    });

    if (!resultsLockNotice) return;
    if (accessMode === 'locked') {
        resultsLockNotice.classList.remove('hidden');
        resultsLockNotice.innerHTML = `
            <strong>Daily free quota used</strong>
            <span>You have reached today's free analyses. Upgrade to premium or wait until ${escapeHTML(formatResetTime(currentSession.quota?.resets_at))} to predict again.</span>
            <button class="btn btn-primary btn-sm" type="button" data-account-open>Unlock premium</button>
        `;
    } else {
        resultsLockNotice.classList.add('hidden');
        resultsLockNotice.innerHTML = '';
    }
}

function renderAuthState() {
    const user = currentSession.user;
    const quota = currentSession.quota;

    if (accountControls) {
        if (user) {
            accountControls.innerHTML = `
                <button class="account-pill" type="button" id="accountOpenBtn">
                    <span class="account-avatar" aria-hidden="true">${escapeHTML(user.display_name?.[0] || 'U')}</span>
                    <span>
                        <strong>${escapeHTML(user.display_name || 'LuntiAI user')}</strong>
                        <small>${escapeHTML(quotaLabel(quota, user))}</small>
                    </span>
                    <span class="tier-badge ${user.tier === 'premium' ? 'premium' : 'free'}">${escapeHTML(user.tier)}</span>
                </button>
            `;
        } else {
            accountControls.innerHTML = `
                <span class="account-free-cue">3 free analyses/day</span>
                <button class="btn btn-secondary btn-sm" type="button" data-auth-open="login">Log in</button>
                <button class="btn btn-primary btn-sm" type="button" data-auth-open="register">Create account</button>
            `;
        }
    }

    if (quotaPanel) {
        if (!user) {
            quotaPanel.className = 'quota-panel signed-out';
            quotaPanel.innerHTML = `
                <div>
                    <strong>Sign in to analyze</strong>
                    <span>Create an account to use 3 free crop analyses per day.</span>
                </div>
                <button class="btn btn-secondary btn-sm" type="button" data-auth-open="login">Log in</button>
            `;
        } else if (user.tier === 'premium' || quota?.remaining === -1) {
            quotaPanel.className = 'quota-panel premium';
            quotaPanel.innerHTML = `
                <div>
                    <strong>Premium active</strong>
                    <span>Unlimited crop analyses and prediction history are unlocked.</span>
                </div>
                <button class="btn btn-secondary btn-sm" type="button" id="historyQuickBtn">View history</button>
            `;
        } else {
            const remaining = Math.max(Number(quota?.remaining ?? 0), 0);
            quotaPanel.className = remaining === 0 ? 'quota-panel limited' : 'quota-panel free';
            quotaPanel.innerHTML = `
                <div>
                    <strong>${remaining === 0 ? 'Daily quota used' : quotaLabel(quota, user)}</strong>
                    <span>${remaining === 0 ? `Unlock premium or wait until ${formatResetTime(quota?.resets_at)}.` : 'Premium unlocks unlimited analyses and history.'}</span>
                </div>
                <button class="btn btn-secondary btn-sm" type="button" data-account-open>${remaining === 0 ? 'Unlock premium' : 'Account'}</button>
            `;
        }
    }

    renderAccountSummary();
    updateSubmitState();
    if (window.lastResult && !resultsSection.classList.contains('hidden')) {
        applyResultAccessState();
    }
}

function renderAccountSummary() {
    if (!accountSummary) return;
    const user = currentSession.user;
    if (!user) {
        accountSummary.innerHTML = `
            <div class="empty-state">
                <strong>No account loaded</strong>
                <span>Log in to manage quota and history.</span>
            </div>
        `;
        return;
    }
    accountSummary.innerHTML = `
        <div class="summary-grid">
            <div class="summary-item">
                <span>Display alias</span>
                <strong>${escapeHTML(user.display_name || 'LuntiAI user')}</strong>
            </div>
            <div class="summary-item">
                <span>Username</span>
                <strong>${escapeHTML(user.username || '—')}</strong>
            </div>
            <div class="summary-item">
                <span>Plan</span>
                <strong><span class="tier-badge ${user.tier === 'premium' ? 'premium' : 'free'}">${escapeHTML(user.tier)}</span></strong>
            </div>
            <div class="summary-item">
                <span>Quota</span>
                <strong>${escapeHTML(quotaLabel())}</strong>
            </div>
            <div class="summary-item">
                <span>Reset</span>
                <strong>${currentSession.quota?.remaining === -1 ? 'Unlimited' : escapeHTML(formatResetTime(currentSession.quota?.resets_at))}</strong>
            </div>
        </div>
    `;
}

function escapeHTML(value) {
    return String(value ?? '').replace(/[&<>"']/g, char => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#39;',
    }[char]));
}

function setApiStatus(mode, label) {
    const status = document.getElementById('apiStatus');
    if (!status) return;
    const dot = status.querySelector('.status-dot');
    if (dot) {
        dot.className = `status-dot ${mode}`;
    }
    const text = status.querySelector('span:last-child');
    if (text) {
        text.textContent = label;
    }
}

// =============================================================================
// INITIALIZATION
// =============================================================================
document.addEventListener('DOMContentLoaded', async () => {
    initTheme();
    initLocalization();
    initAuthUI();
    renderAuthState();
    await loadBarangays();
    checkBackendHealth();
    await refreshMe();
    initInteractivity();

    // Language toggle buttons
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', () => applyLang(btn.dataset.lang));
    });
});

function initAuthUI() {
    document.addEventListener('click', (event) => {
        const authOpen = event.target.closest('[data-auth-open]');
        if (authOpen) {
            openAuthModal(authOpen.dataset.authOpen || 'login');
            return;
        }

        const tab = event.target.closest('[data-auth-tab]');
        if (tab) {
            setAuthPanel(tab.dataset.authTab || 'login');
            return;
        }

        if (event.target.closest('[data-modal-close]')) {
            closeModals();
            return;
        }

        if (event.target === authModal || event.target === accountModal) {
            closeModals();
            return;
        }

        if (event.target.closest('#accountOpenBtn') || event.target.closest('[data-account-open]')) {
            openAccountModal();
            return;
        }

        if (event.target.closest('#historyQuickBtn')) {
            openAccountModal();
            loadHistory();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') closeModals();
    });

    loginForm?.addEventListener('submit', handleLogin);
    registerForm?.addEventListener('submit', handleRegister);
    redeemForm?.addEventListener('submit', handleRedeem);
    document.getElementById('logoutBtn')?.addEventListener('click', () => {
        clearSession();
        closeModals();
        showToast('Logged out.', 'info');
    });
    document.getElementById('deleteAccountBtn')?.addEventListener('click', handleDeleteAccount);
    document.getElementById('loadHistoryBtn')?.addEventListener('click', loadHistory);
}

function openAuthModal(mode = 'login', message = '') {
    lastFocusedElement = document.activeElement;
    setAuthPanel(mode);
    if (message) {
        const desc = document.getElementById('authModalDesc');
        if (desc) desc.textContent = message;
    }
    authModal?.classList.remove('hidden');
    setTimeout(() => {
        const field = mode === 'register'
            ? document.getElementById('registerDisplayName')
            : document.getElementById('loginUsername');
        field?.focus();
    }, 30);
}

function setAuthPanel(mode = 'login') {
    const normalized = mode === 'register' ? 'register' : 'login';
    document.querySelectorAll('[data-auth-tab]').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.authTab === normalized);
    });
    document.querySelectorAll('[data-auth-panel]').forEach(panel => {
        panel.classList.toggle('hidden', panel.dataset.authPanel !== normalized);
    });
    const title = document.getElementById('authModalTitle');
    const desc = document.getElementById('authModalDesc');
    if (title) title.textContent = normalized === 'register' ? 'Create your LuntiAI account' : 'Log in to LuntiAI';
    if (desc) {
        desc.textContent = normalized === 'register'
            ? 'Portfolio demo: use an alias and a unique throwaway password. Do not enter real personal information.'
            : 'Sign in to run crop analyses and keep your history.';
    }
}

function openAccountModal() {
    if (!currentSession.user) {
        openAuthModal('login');
        return;
    }
    lastFocusedElement = document.activeElement;
    renderAccountSummary();
    accountModal?.classList.remove('hidden');
    setTimeout(() => document.getElementById('redeemCode')?.focus(), 30);
}

function closeModals() {
    authModal?.classList.add('hidden');
    accountModal?.classList.add('hidden');
    lastFocusedElement?.focus?.();
}

async function handleLogin(event) {
    event.preventDefault();
    await submitAuth('/login', loginForm, 'Welcome back.');
}

async function handleRegister(event) {
    event.preventDefault();
    await submitAuth('/register', registerForm, 'Account created.');
}

async function submitAuth(path, form, successMessage) {
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    try {
        const res = await fetch(`${API_BASE}${path}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Authentication failed');
        setSession(data);
        form.reset();
        closeModals();
        showToast(successMessage, 'success');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function refreshMe() {
    if (!getToken()) {
        renderAuthState();
        return;
    }
    try {
        const res = await authFetch('/me');
        if (!res.ok) throw new Error('Session expired');
        setSession(await res.json());
    } catch (err) {
        clearSession();
    }
}

async function handleRedeem(event) {
    event.preventDefault();
    const code = new FormData(redeemForm).get('code');
    if (!code) {
        showToast('Enter a redeem code.', 'error');
        return;
    }
    try {
        const res = await authFetch('/redeem', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code }),
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Could not redeem code');
        setSession(data);
        redeemForm.reset();
        showToast('Premium unlocked.', 'success');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function handleDeleteAccount() {
    if (!currentSession.user) return;
    const confirmed = window.confirm('Delete this LuntiAI account and prediction history? This cannot be undone.');
    if (!confirmed) return;

    try {
        const res = await authFetch('/me', { method: 'DELETE' });
        const data = await res.json().catch(() => ({}));
        if (!res.ok) throw new Error(data.detail || 'Could not delete account');
        clearSession();
        closeModals();
        showToast('Account deleted.', 'info');
    } catch (err) {
        showToast(err.message, 'error');
    }
}

async function loadHistory() {
    if (!currentSession.user) {
        openAuthModal('login');
        return;
    }
    if (currentSession.user.tier !== 'premium') {
        historyList.innerHTML = `
            <div class="paywall-card">
                <strong>History is a premium feature.</strong>
                <span>Redeem <code>LUNTIAI2026</code> to unlock saved prediction history.</span>
            </div>
        `;
        return;
    }
    historyList.innerHTML = `<div class="empty-state">Loading history...</div>`;
    try {
        const res = await authFetch('/history?limit=20');
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Could not load history');
        if (!data.history?.length) {
            historyList.innerHTML = `
                <div class="empty-state">
                    <strong>No predictions yet</strong>
                    <span>Run an analysis and it will appear here.</span>
                </div>
            `;
            return;
        }
        historyList.innerHTML = data.history.map(item => `
            <article class="history-item">
                <div>
                    <strong>${escapeHTML(item.best_crop)}</strong>
                    <span>${escapeHTML(item.barangay || 'Manual input')} · ${Number(item.confidence).toFixed(2)}% confidence</span>
                </div>
                <time>${escapeHTML(formatResetTime(item.created_at))}</time>
            </article>
        `).join('');
    } catch (err) {
        historyList.innerHTML = `<div class="empty-state error">${escapeHTML(err.message)}</div>`;
    }
}

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
        setApiStatus('offline', 'Offline demo mode');
        showToast('Backend not connected. Using offline demo mode.', 'info');
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
            setApiStatus('online', 'API connected');
        }
    } catch (err) {
        console.warn('⚠ Backend not reachable:', err.message);
        setApiStatus('offline', 'Offline demo mode');
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
            <span class="data-card-icon"><i class="fas fa-temperature-half"></i></span>
            <div class="data-card-label">Temperature</div>
            <div class="data-card-value">${weather.temp}<span class="data-card-unit">°C</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-water"></i></span>
            <div class="data-card-label">Humidity</div>
            <div class="data-card-value">${weather.humidity}<span class="data-card-unit">%</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-cloud-rain"></i></span>
            <div class="data-card-label">Rainfall</div>
            <div class="data-card-value">${weather.rainfall_estimate}<span class="data-card-unit">mm/mo</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-cloud-sun"></i></span>
            <div class="data-card-label">Conditions</div>
            <div class="data-card-value compact">${weather.description}</div>
        </div>
    `;
}

function renderWeatherFallback() {
    weatherSource.textContent = 'PAGASA Climate Normals';
    weatherDataGrid.innerHTML = `
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-temperature-half"></i></span>
            <div class="data-card-label">Temperature</div>
            <div class="data-card-value">27.5<span class="data-card-unit">°C</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-water"></i></span>
            <div class="data-card-label">Humidity</div>
            <div class="data-card-value">82<span class="data-card-unit">%</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-cloud-rain"></i></span>
            <div class="data-card-label">Rainfall</div>
            <div class="data-card-value">175<span class="data-card-unit">mm/mo</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-cloud-sun"></i></span>
            <div class="data-card-label">Conditions</div>
            <div class="data-card-value compact">Tropical Wet</div>
        </div>
    `;
}

function renderSoilData(soil, barangayName) {
    soilTypeLabel.textContent = `${soil.soil_type || 'Loam'} — ${barangayName}`;
    soilDataGrid.innerHTML = `
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-flask"></i></span>
            <div class="data-card-label">Nitrogen (N)</div>
            <div class="data-card-value">${soil.N}<span class="data-card-unit">mg/kg</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-vial"></i></span>
            <div class="data-card-label">Phosphorus (P)</div>
            <div class="data-card-value">${soil.P}<span class="data-card-unit">mg/kg</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-atom"></i></span>
            <div class="data-card-label">Potassium (K)</div>
            <div class="data-card-value">${soil.K}<span class="data-card-unit">mg/kg</span></div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-droplet"></i></span>
            <div class="data-card-label">pH Level</div>
            <div class="data-card-value">${soil.pH || soil.ph}</div>
        </div>
        <div class="data-card">
            <span class="data-card-icon"><i class="fas fa-layer-group"></i></span>
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

    if (!getToken()) {
        openAuthModal('login', 'Log in or create an account before running a crop analysis.');
        showToast('Please log in to analyze your field data.', 'info');
        return;
    }

    if (isQuotaExhausted()) {
        applyResultAccessState('locked');
        if (window.lastResult) resultsSection.classList.remove('hidden');
        openAccountModal();
        showToast('Your free quota is used for today. Unlock premium to continue.', 'info');
        return;
    }

    cropForm.querySelectorAll('[aria-invalid="true"]').forEach(el => el.removeAttribute('aria-invalid'));

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
            const field = cropForm.querySelector(`[name="${key}"]`);
            if (field) {
                field.setAttribute('aria-invalid', 'true');
                field.focus();
            }
            showToast(`Please fill in ${key}.`, 'error');
            return;
        }
    }

    // Show loading
    showLoading();
    resultsSection.classList.add('hidden');

    try {
        const res = await authFetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        });

        const result = await res.json();
        hideLoading();

        if (res.ok) {
            currentSession.quota = {
                allowed: !result.is_quota_limited,
                remaining: result.quota_remaining,
                resets_at: result.quota_resets_at,
            };
            if (currentSession.quota) localStorage.setItem(AUTH_QUOTA_KEY, JSON.stringify(currentSession.quota));
            renderResults(result);
            renderAuthState();
        } else {
            if (res.status === 401) {
                openAuthModal('login', 'Your session expired. Log in again to analyze.');
            }
            showToast(result.detail || 'Prediction failed', 'error');
        }
    } catch (err) {
        hideLoading();
        showToast(`Network error: ${err.message}. Is the backend running?`, 'error');
    }
});

cropForm.querySelectorAll('input').forEach(input => {
    input.addEventListener('input', () => input.removeAttribute('aria-invalid'));
});

// =============================================================================
// RESULTS RENDERING
// =============================================================================
function renderResults(result) {
    window.lastResult = result; // Save for language toggles
    const accessMode = getResultAccessMode();

    const iconClass = CROP_ICON_CLASSES[result.best_crop] || 'fa-seedling';
    const confTone = result.confidence >= 80 ? 'high' :
                     result.confidence >= 60 ? 'medium' : 'low';
    
    // Construct localized message
    const locMsg = `${t('msg_prefix')} <strong>${result.best_crop}</strong> ${t('msg_suffix')}`;
    const paywallHTML = accessMode === 'locked' ? `
        <div class="paywall-card result-paywall">
            <strong>Free quota reached</strong>
            <span>This report is now locked for the day. Unlock premium to keep analyzing and reveal the full decision report.</span>
            <button class="btn btn-primary btn-sm" type="button" data-account-open>Unlock premium</button>
        </div>
    ` : accessMode === 'free' ? `
        <div class="paywall-card result-paywall">
            <strong>Free plan view</strong>
            <span>Your top crop recommendation is visible. ROI, fertilizer advice, confidence charts, and alternatives are premium-only.</span>
            <button class="btn btn-primary btn-sm" type="button" data-account-open>Unlock premium</button>
        </div>
    ` : '';

    resultHero.innerHTML = `
        <div class="result-hero confidence-${confTone}">
            <div class="result-crop-icon" aria-hidden="true"><i class="fas ${iconClass}"></i></div>
            <div class="result-crop-name">${result.best_crop}</div>
            <p class="result-message">${locMsg}</p>
            <div class="result-confidence">
                <i class="fas fa-bullseye"></i> ${(result.confidence).toFixed(2)}% <span data-i18n="pred_confidence">${t('pred_confidence')}</span>
            </div>
            ${paywallHTML}
        </div>
    `;

    // Alternative crops
    const alts = (result.top_predictions || []).filter(p => p.crop !== result.best_crop).slice(0, 4);
    if (alts.length > 0) {
        altCropsSection.innerHTML = `
            <div class="generated-heading">
                <i class="fas fa-list-ul"></i>
                <span>${t('alt_crops_label')}</span>
            </div>
            <div class="alt-crops-grid">
                ${alts.map((a, i) => `
                    <div class="alt-crop-card">
                        <div class="alt-crop-rank">${i + 2}</div>
                        <div>
                            <div class="alt-crop-name"><i class="fas ${CROP_ICON_CLASSES[a.crop] || 'fa-seedling'}" aria-hidden="true"></i> ${a.crop}</div>
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
            <div class="generated-heading">
                <i class="fas fa-flask"></i>
                <span>${t('fertilizer_label')}</span>
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
                    <div class="fertilizer-title">${t(f.condition)}</div>
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
    if (result.crop_economics) {
        const econ = result.crop_economics;
        
        // Compute Gross Income and ROI
        const grossIncome = econ.avg_yield_kg_ha * econ.farmgate_price_php_kg;
        const netProfit = grossIncome - econ.production_cost_php;
        const roi = (netProfit / econ.production_cost_php) * 100;
        
        // Format Currency
        const fmtPHP = (val) => new Intl.NumberFormat('en-PH', { style: 'currency', currency: 'PHP', minimumFractionDigits: 0 }).format(val);
        const fmtNum = (val) => new Intl.NumberFormat('en-US').format(val);
        
        economicsSection.innerHTML = `
            <div class="generated-heading">
                <i class="fas fa-calculator"></i>
                <span>${t('econ_title')}</span>
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
        if (economicsSection) economicsSection.innerHTML = '';
        if (econChartContainer) econChartContainer.classList.add('hidden');
    }

    // Probability Chart
    renderChart(result.top_predictions || []);

    // Show results
    resultsSection.classList.remove('hidden');
    applyResultAccessState(accessMode);
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
        <div class="shap-card">
            <div class="generated-heading">
                <i class="fas fa-brain"></i>
                <span>${t('shap_title')}</span>
            </div>
            <p class="shap-label">${t('shap_positive')}</p>
            ${posHTML}
            <p class="shap-label">${t('shap_negative')}</p>
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
    const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDarkMode ? '#b9c2b5' : '#5f6b61';
    const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.08)' : 'rgba(24, 34, 26, 0.08)';
    const primaryColor = isDarkMode ? 'rgba(119, 197, 140, 0.72)' : 'rgba(31, 107, 59, 0.76)';
    const primaryBorder = isDarkMode ? 'rgba(119, 197, 140, 1)' : 'rgba(31, 107, 59, 1)';

    probChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Match Probability (%)',
                data: data,
                backgroundColor: primaryColor,
                borderColor: primaryBorder,
                borderWidth: 1.5,
                borderRadius: 8,
                hoverBackgroundColor: 'rgba(34, 197, 94, 0.9)',
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
                    backgroundColor: isDarkMode ? 'rgba(16, 23, 15, 0.95)' : 'rgba(255, 255, 255, 0.96)',
                    titleColor: isDarkMode ? '#f3f0e7' : '#18221a',
                    bodyColor: isDarkMode ? '#f3f0e7' : '#18221a',
                    borderColor: primaryBorder,
                    borderWidth: 1,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    grid: { color: gridColor },
                    ticks: { color: textColor, font: { family: 'Plus Jakarta Sans' } }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: textColor, font: { family: 'Plus Jakarta Sans', size: 11 } }
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
    
    const isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
    const textColor = isDarkMode ? '#b9c2b5' : '#5f6b61';
    const gridColor = isDarkMode ? 'rgba(255, 255, 255, 0.08)' : 'rgba(24, 34, 26, 0.08)';

    econChartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [t('econ_chart_title')],
            datasets: [
                {
                    label: t('econ_cost'),
                    data: [cost],
                    backgroundColor: isDarkMode ? 'rgba(231, 191, 88, 0.65)' : 'rgba(180, 83, 9, 0.58)',
                    borderColor: isDarkMode ? 'rgba(231, 191, 88, 1)' : 'rgba(180, 83, 9, 1)',
                    borderWidth: 1.5,
                    borderRadius: 8
                },
                {
                    label: t('econ_profit'),
                    data: [profit],
                    backgroundColor: isDarkMode ? 'rgba(119, 197, 140, 0.65)' : 'rgba(31, 107, 59, 0.62)',
                    borderColor: isDarkMode ? 'rgba(119, 197, 140, 1)' : 'rgba(31, 107, 59, 1)',
                    borderWidth: 1.5,
                    borderRadius: 8
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { 
                    position: 'top',
                    labels: { color: textColor, font: { family: 'Plus Jakarta Sans' } }
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
                        font: { family: 'Plus Jakarta Sans' },
                        callback: function(value) {
                            return '₱' + new Intl.NumberFormat('en-US', { notation: "compact", compactDisplay: "short" }).format(value);
                        }
                    }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: textColor, font: { family: 'Plus Jakarta Sans' } }
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
    loadingOverlay.setAttribute('aria-hidden', 'false');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
}

function hideLoading() {
    loadingOverlay.classList.remove('active');
    loadingOverlay.setAttribute('aria-hidden', 'true');
    submitBtn.disabled = false;
    updateSubmitState();
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
    toast.setAttribute('role', type === 'error' ? 'alert' : 'status');
    toast.setAttribute('aria-live', type === 'error' ? 'assertive' : 'polite');
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
    if (saved === 'dark') {
        document.documentElement.setAttribute('data-theme', 'dark');
        updateThemeIcon('dark');
    } else {
        document.documentElement.removeAttribute('data-theme');
        updateThemeIcon('light');
    }
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('themeIcon');
    if (!icon) return;
    if (theme === 'dark') {
        icon.className = 'fas fa-sun';
    } else {
        icon.className = 'fas fa-moon';
    }
}

document.getElementById('themeToggle')?.addEventListener('click', () => {
    const current = document.documentElement.getAttribute('data-theme');
    if (current === 'dark') {
        document.documentElement.removeAttribute('data-theme');
        localStorage.setItem('luntiai-theme', 'light');
        updateThemeIcon('light');
    } else {
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('luntiai-theme', 'dark');
        updateThemeIcon('dark');
    }

    // Re-render chart if visible so colors adapt
    if (window.lastResult && !resultsSection.classList.contains('hidden')) {
        renderResults(window.lastResult);
    }
});

// =============================================================================
// UI INTERACTIVITY (Glow, Scroll, etc.)
// =============================================================================
function initInteractivity() {
    const cursorGlow = document.getElementById('cursorGlow');
    const scrollProgress = document.getElementById('scrollProgress');

    // Cursor Glow Follow
    document.addEventListener('mousemove', (e) => {
        if (!cursorGlow) return;
        cursorGlow.style.left = `${e.clientX}px`;
        cursorGlow.style.top = `${e.clientY}px`;
    });

    // Scroll Progress
    window.addEventListener('scroll', () => {
        if (!scrollProgress) return;
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        scrollProgress.style.width = `${scrolled}%`;
    });
}
