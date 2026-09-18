"""Scenario arithmetic, not measured robot performance. Python standard library only."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent
U = 0.85
# Nominal pack energy; all powers referred to battery output. No named robot implied.
PLATFORMS = [
    ('小型四足示例', 250, 150, 10, 20),
    ('中型移动机器人示例', 600, 350, 20, 80),
    ('大型人形或工业四足示例', 2300, 450, 30, 120),
    ('轮式移动操作平台示例', 1500, 150, 20, 80),
]
SCENARIOS = [('2026基线', 1, 1, 1), ('2029保守', 1.1, 1.3, 1),
             ('2029中值规划', 1.2, 2, 1), ('2029积极', 1.4, 3, 1),
             ('2029计算量翻倍', 1.2, 2, 2)]
rows = []
for name, energy, other, fixed, dynamic in PLATFORMS:
    baseline = U * energy / (other + fixed + dynamic)
    for scenario, battery_gain, efficiency, workload in SCENARIOS:
        compute = fixed + dynamic * workload / efficiency
        runtime = U * energy * battery_gain / (other + compute)
        rows.append(dict(platform=name, scenario=scenario, nominal_Wh=energy* battery_gain,
                         usable_fraction=U, other_W=other, compute_fixed_W=fixed,
                         compute_dynamic_W=dynamic*workload/efficiency, compute_total_W=compute,
                         runtime_h=runtime, gain_pct=(runtime/baseline-1)*100))
with (ROOT / 'scenarios.csv').open('w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)
for row in rows:
    print(f"{row['platform']} {row['scenario']}: {row['compute_total_W']:.2f} W, "
          f"{row['runtime_h']:.3f} h, {row['gain_pct']:.1f}%")
print('Additional battery for 100 W, 4 h, 150 Wh/kg, k=10 W/kg:',
      4*100/(U*150-4*10), 'kg')
print('4-hour compute budget for 2300 Wh / other 450 W:', U*2300/4-450, 'W')
print('2029 with 20% more energy:', U*2300*1.2/4-450, 'W')
for size in [8, 32, 70]:
    weights_GB = size / 2
    print('Q4 conventional dense decode bandwidth envelope:', size,
          'B, 273 GB/s:', 273/weights_GB,
          't/s; 500 GB/s:', 500/weights_GB, 't/s')
