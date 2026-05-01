import urllib.request, json

payload = json.dumps({
    'N':78,'P':42,'K':45,'temperature':27.5,
    'humidity':82,'ph':5.5,'rainfall':175,'OM':3.2,'barangay':'Bincungan'
}).encode()
req = urllib.request.Request('http://localhost:8000/predict', data=payload,
    headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())

crop = data['best_crop']
econ = data.get('crop_economics', {})

lc  = econ['labor_cost']['total']
mc  = econ['material_cost']['total']
oc  = econ['other_cost']['total']
tcp = econ['production_cost_php']
gr  = econ['avg_yield_kg_ha'] * econ['farmgate_price_php_kg']
ni  = gr - tcp
roi = ni / tcp * 100
wage = econ['labor_cost']['wage_rate_php_day']

print(f"Crop:      {crop} ({data['confidence']}% confidence)")
print(f"Wage:      P{wage}/day (Wage Order RB XI-24)")
print(f"LC:        P{lc:,}")
print(f"MC:        P{mc:,}")
print(f"OC:        P{oc:,}")
print(f"TCP:       P{tcp:,}  (LC+MC+OC={lc+mc+oc:,}  match={lc+mc+oc==tcp})")
print(f"Yield:     {econ['avg_yield_kg_ha']:,} kg/ha")
print(f"Price:     P{econ['farmgate_price_php_kg']}/kg")
print(f"GR:        P{gr:,.0f}")
print(f"NI:        P{ni:,.0f}")
print(f"ROI:       {roi:.1f}%  ({'OK' if 20 <= roi <= 100 else 'OUT OF RANGE'})")
print(f"B/C:       {gr/tcp:.2f}")
print(f"BEY:       {tcp/econ['farmgate_price_php_kg']:,.0f} kg/ha (break-even yield)")
