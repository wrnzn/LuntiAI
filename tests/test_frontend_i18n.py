import pytest
from pathlib import Path

def test_chart_js_is_translated():
    app_js_path = Path("frontend/app.js")
    content = app_js_path.read_text(encoding="utf-8")
    
    # renderEconChart shouldn't contain hardcoded English strings
    assert "label: 'Production Cost'" not in content, "Production Cost label in Chart.js is hardcoded"
    assert "label: 'Net Profit'" not in content, "Net Profit label in Chart.js is hardcoded"
    assert "labels: ['Per Hectare Estimates']" not in content, "Per Hectare Estimates label in Chart.js is hardcoded"
    
    # Ensure it uses localization function
    assert "label: t('econ_cost')" in content or 'label: t("econ_cost")' in content, "Should use t('econ_cost')"
    assert "label: t('econ_profit')" in content or 'label: t("econ_profit")' in content, "Should use t('econ_profit')"
    assert "labels: [t('econ_chart_title')]" in content or 'labels: [t("econ_chart_title")]' in content, "Should use t('econ_chart_title')"

