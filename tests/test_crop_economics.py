"""
test_crop_economics.py — DA-CRA calibration tests (TDD)
==========================================================
Wage Order RB XI-24 (Mar 13 2026): agricultural minimum wage = ₱515/day
Source: DOLE Region XI, DA Region XI CRA standards

Run:  python -m pytest tests/test_crop_economics.py -v
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from barangay_data import CROP_ECONOMICS, get_crop_economics

WAGE_RATE = 515          # Wage Order RB XI-24 (Mar 2026)
ROI_MIN   = 20.0         # DA Region XI CRA floor
ROI_MAX   = 100.0        # Guard: > 100% → bad calibration

ALL_CROPS = list(CROP_ECONOMICS.keys())


# ── Behavior 1: TCP arithmetic ───────────────────────────────────────────────
# production_cost_php MUST equal LC.total + MC.total + OC.total

def test_tcp_equals_sum_of_cost_components_for_all_crops():
    """production_cost_php = labor_cost.total + material_cost.total + other_cost.total"""
    for crop, data in CROP_ECONOMICS.items():
        lc = data["labor_cost"]["total"]
        mc = data["material_cost"]["total"]
        oc = data["other_cost"]["total"]
        tcp = data["production_cost_php"]
        assert lc + mc + oc == tcp, (
            f"{crop}: LC({lc}) + MC({mc}) + OC({oc}) = {lc+mc+oc} ≠ TCP({tcp})"
        )


# ── Behavior 2: Wage Order RB XI-24 rate ────────────────────────────────────
# Every crop must use ₱515/day — old ₱450 is pre-March 2026

def test_all_crops_use_wage_order_rb_xi_24_rate():
    """labor_cost.wage_rate_php_day = 515 (Wage Order RB XI-24)"""
    for crop, data in CROP_ECONOMICS.items():
        rate = data["labor_cost"]["wage_rate_php_day"]
        assert rate == WAGE_RATE, (
            f"{crop}: wage_rate={rate}, expected {WAGE_RATE} (Wage Order RB XI-24)"
        )


# ── Behavior 3: Rice — DA Region XI 2026 benchmark values ───────────────────

def test_rice_uses_da_region_xi_2026_benchmark_values():
    """Rice: yield=4720 kg/ha, farmgate=₱18.89/kg (DA Region XI 2026)"""
    rice = get_crop_economics("Rice")
    assert rice is not None
    assert rice["avg_yield_kg_ha"] == 4720, (
        f"Rice yield={rice['avg_yield_kg_ha']}, expected 4720 kg/ha (DA Region XI 2026)"
    )
    assert abs(rice["farmgate_price_php_kg"] - 18.89) < 0.01, (
        f"Rice price={rice['farmgate_price_php_kg']}, expected ₱18.89/kg"
    )


# ── Behavior 4: Annual ROI 20–100% for all crops ────────────────────────────
# > 100% → inflated yield or deflated cost. DA-CRA Region XI real range: 20–60%.

def _annual_roi(data: dict) -> float:
    seasons = data["cropping_seasons_per_year"]
    tcp_annual = data["production_cost_php"] * seasons
    gr_annual  = data["avg_yield_kg_ha"] * data["farmgate_price_php_kg"] * seasons
    net = gr_annual - tcp_annual
    return (net / tcp_annual) * 100


def test_all_crops_annual_roi_within_realistic_range():
    """No crop annual ROI < 20% or > 100% (DA-CRA Region XI calibration guard)"""
    for crop, data in CROP_ECONOMICS.items():
        roi = _annual_roi(data)
        assert ROI_MIN <= roi <= ROI_MAX, (
            f"{crop}: annual ROI={roi:.1f}% — outside [{ROI_MIN}, {ROI_MAX}]% "
            f"(TCP=₱{data['production_cost_php']:,}, "
            f"yield={data['avg_yield_kg_ha']}kg, "
            f"price=₱{data['farmgate_price_php_kg']}/kg)"
        )
