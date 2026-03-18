# Grid Saver ⚡
### Adaptive Grid Intelligence Platform
**Red Bull Basement 2026 | Justine Adzormado**

> Preventing blackouts through predictive, distributed energy coordination.

---

## What is Grid Saver?

Power grids do not fail due to lack of electricity, they fail when demand spikes faster than system response. Grid Saver prevents these failures by predicting peak vulnerability windows and coordinating small, distributed reductions in residential energy use before the grid reaches critical stress.

Validated using ERCOT (Texas) grid data, the same system that failed during the 2021 Texas Power Crisis, leaving millions without power.

---

## The Sense-Predict-Act Framework

| Layer | Function | Dataset | Status |
|-------|----------|---------|--------|
| SENSE | Detect grid stress signals | Electricity Maps US-TEX-ERCO 2025 | ✅ Phase 1 Complete |
| PREDICT | Forecast vulnerability windows 24hr ahead | PJM 145,367 hourly records | ✅ Phase 2 Complete |
| ACT | Simulate coordinated 3-5% HVAC load reduction | Pecan Street Austin 15-min | ✅ Phase 1 Preview Complete |

---

## Live Demo

Interactive prototype demonstrating:
- Real-time demand visualization
- Peak vulnerability detection
- HVAC load reduction simulation
- Impact at Scale slider
- AI Decision Explanation

👉 **[https://gridsaver.streamlit.app](https://gridsaver.streamlit.app)**

---

## Phase 1 Results - Confirmed

**SENSE Layer (ERCOT US-TEX-ERCO 2025)**
- 8,760 hourly records analysed
- 1,316 vulnerability windows detected (15% of year)
- Peak event stress month: August | Peak stress hour: 01:00 UTC

**ACT Layer Preview (Pecan Street Austin 2018)**
- 25 real Austin TX households, full year 2018
- HVAC share of total load: 56.3% (Texas hot climate)
- Original peak event demand: 105.71 kW
- Grid Saver optimized: 103.41 kW
- Peak event reduction: 2.2% (Grid Stabilized)
- Worst day validated: 2018-08-28

---

```bash
git clone https://github.com/justineadzormado/grid-saver
cd grid-saver
pip install -r requirements.txt
streamlit run grid_saver_app.py
```

---

## Repository Structure

```
grid-saver/
├── grid_saver_app.py               # Streamlit dashboard
├── gridsaver_phase1.ipynb          # Colab analysis notebook
├── requirements.txt                # Dependencies
├── README.md                       # This file
└── data/
    └── snapshots_US-TEX-ERCO.csv  # ERCOT sense layer data
```

---

## Dataset Stack

| Dataset | Records | Role |
|---------|---------|------|
| Electricity Maps US-TEX-ERCO 2025 | 8,761 hourly | Sense Layer |
| PJM_Load_hourly.csv | 32,897 hourly | Predict Layer |
| PJME_hourly.csv | 145,367 hourly | Validation |
| Pecan Street Austin 15-min | 680K rows | Act Layer |
| Ghana Energy Commission 2025 | 2000-2024 | Context |

---

## The Science

Because power grids operate within narrow reserve margins, even small, coordinated reductions in residential HVAC demand can significantly reduce peak load and prevent system instability.

**Reserve Margin Formula:**
- Peak demand: 9,200 MW
- Grid Saver 4% reduction: 368 MW removed
- New demand: 8,832 MW (grid stabilizes)

**Scaling (proven on real Pecan Street data):**
- 0.0920 kW reduction per home (25 Austin TX homes validated)
- 1,000,000 homes = 92 MW removed
- Grid-scale stabilisation confirmed

---

## Tech Stack

- **Analysis:** Google Colab
- **Code:** GitHub
- **Deployment:** Streamlit Community Cloud
- **Production path:** Azure Functions + Azure ML (Phase 3)

---

*Built for Red Bull Basement 2026*
