# Grid Saver ⚡
### Adaptive Grid Intelligence Platform
**Red Bull Basement 2026 | Justine Adzormado**

> Preventing blackouts through predictive, distributed energy coordination.

---

## What is Grid Saver?

Power grids do not fail due to lack of electricity — they fail when demand spikes faster than system response. Grid Saver prevents these failures by predicting peak vulnerability windows and coordinating small, distributed reductions in residential energy use before the grid reaches critical stress.

Validated using ERCOT (Texas) grid data — the same system that failed during the 2021 Texas Power Crisis, leaving millions without power.

---

## The Sense-Predict-Act Framework

| Layer | Function | Dataset | Status |
|-------|----------|---------|--------|
| SENSE | Detect grid stress signals | Electricity Maps US-TEX-ERCO 2025 | ✅ Phase 1 Complete |
| PREDICT | Forecast vulnerability windows 24hr ahead | PJM 145,367 hourly records | ✅ Phase 2 Complete |
| ACT | Simulate coordinated 3-5% HVAC load reduction | Pecan Street Austin 15-min | ✅ Phase 3 Complete |

**Full SPA Integration complete. All three layers connected into one unified pipeline.**

---

## Live Demo

Interactive prototype demonstrating:
- Real-time grid stress detection
- Peak vulnerability window forecasting
- HVAC load reduction simulation
- Impact at Scale slider
- AI Decision Explanation
- Full SPA dual-confirmation logic

👉 **[https://gridsaver.streamlit.app](https://gridsaver.streamlit.app)**

---

## Results — All Three Phases Confirmed

**SENSE Layer — Phase 1 (ERCOT US-TEX-ERCO 2025)**
- 8,760 hourly records analysed
- 1,316 vulnerability windows detected (15% of year)
- Peak stress month: August | Peak stress hour: 01:00 UTC

**PREDICT Layer — Phase 2 (PJM Interconnection)**
- XGBoost model trained on 32,897 hourly PJM records
- Validated on 145,367 PJME records (Eastern region)
- Recall: 91.6% — catches 9 out of 10 real grid stress events
- ROC-AUC: 0.977 — true 24-hour ahead forecasting
- Decision threshold: 0.4 (tuned for safety-first recall)

**ACT Layer — Phase 3 (Pecan Street Austin 2018)**
- 25 real Austin TX households, full year 2018
- HVAC share of total load: 56.3% (Texas hot climate)
- Original peak demand: 105.71 kW
- Grid Saver optimized: 103.41 kW
- Peak reduction: 2.2% — Grid Stabilized
- Worst day validated: 2018-08-28

**Full SPA Integration — Phase 3**
- Sense triggers: 1,316 hours (15% of year)
- Predict triggers: 1,659 hours (18.9%)
- SPA Actions triggered: 154 hours — dual-confirmation precision
- Grid Saver only acts when BOTH layers independently confirm risk

---

## Running Locally

```bash
git clone https://github.com/JustineAdzormado/grid-saver
cd grid-saver
pip install -r requirements.txt
streamlit run app.py
```

---

## Repository Structure

```
grid-saver/
├── app.py                    # Streamlit dashboard - Full SPA Integration
├── gridsaver_phase1.ipynb    # Sense Layer - ERCOT stress detection
├── gridsaver_phase2.ipynb    # Predict Layer - PJM XGBoost forecasting
├── gridsaver_phase3.ipynb    # Full SPA Integration pipeline
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

---

## Dataset Stack

| Dataset | Records | Role |
|---------|---------|------|
| Electricity Maps US-TEX-ERCO 2025 | 8,761 hourly | Sense Layer |
| PJM_Load_hourly.csv | 32,897 hourly | Predict Layer |
| PJME_hourly.csv | 145,367 hourly | Validation |
| Pecan Street Austin 15-min | ~680K rows | Act Layer |
| Ghana Energy Commission 2025 | 2000-2024 | Context |

---

## The Science

Because power grids operate within narrow reserve margins, even small, coordinated reductions in residential HVAC demand can significantly reduce peak load and prevent system instability.

**Reserve Margin Formula:**
- Peak demand: 9,200 MW
- Grid Saver 4% reduction: 368 MW removed
- New demand: 8,832 MW — grid stabilizes

**Scaling (proven on real Pecan Street data):**
- 0.0920 kW reduction per home (25 Austin TX homes validated)
- 1,000,000 homes = 92 MW removed
- Grid-scale stabilisation confirmed

**SPA Dual-Confirmation Logic:**
- Grid Saver does not trigger on every stress signal
- Both Sense AND Predict must independently confirm risk
- 154 confirmed actions out of 8,760 hours — surgical precision, not blunt response

---

## Tech Stack

- **Analysis:** Google Colab
- **Code:** GitHub — github.com/JustineAdzormado/grid-saver
- **Deployment:** Streamlit Community Cloud
- **Production path:** Azure Functions + Azure ML (after national selection)

---

*Built for Red Bull Basement 2026 World Final - Silicon Valley*
