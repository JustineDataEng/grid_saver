# Grid Saver ⚡
### Adaptive Grid Intelligence Platform
**Justine Adzormado**

> Preventing blackouts through predictive, distributed energy coordination and early vulnerability detection.

---

## What is Grid Saver?

Power grids do not fail due to lack of electricity, they fail when demand spikes faster than system response. Grid Saver prevents these failures by forecasting peak vulnerability windows and coordinating small, distributed reductions in residential energy use before the grid reaches critical stress.

Validated using ERCOT (Texas) grid data, the same system that failed during the 2021 Texas Power Crisis, leaving millions without power.

---

## The Sense-Predict-Act Framework

| Layer | Function | Dataset | Status |
|-------|----------|---------|--------|
| SENSE | Detect grid vulnerability signals | Electricity Maps US-TEX-ERCO 2025 | ✅ Phase 1 Complete |
| PREDICT | Forecast vulnerability windows 24hr ahead | PJM 32,896 hourly records | ✅ Phase 2 Complete |
| ACT | Simulate coordinated 3-5% HVAC load reduction | Pecan Street Austin 15-min | ✅ Phase 3 Complete |

**Full SPA Integration complete. All three layers connected into one unified pipeline.**

---

## Live Demo

Interactive prototype demonstrating:
- Real-time grid vulnerability detection
- Peak vulnerability window forecasting
- HVAC load reduction simulation
- Impact at Scale slider
- AI Decision Explanation
- Full SPA dual-confirmation logic
> ⚠️ Note: HVAC load is scaled for visualization clarity.
> Real-world impact validated using Pecan Street dataset.

👉 **[https://gridsaver.streamlit.app](https://gridsaver.streamlit.app)**

---

## Results - All Three Phases Confirmed

**SENSE Layer - Phase 1 (ERCOT US-TEX-ERCO 2025)**
- 8,760 hourly records analysed
- 1,316 vulnerability windows detected (15% of year)
- Peak vulnerability month: August | Peak vulnerability hour: 01:00 UTC

**PREDICT Layer - Phase 2 (PJM Interconnection)**
- XGBoost model trained on 32,896 hourly PJM records
- Validated on 145,366 PJME records (Eastern region)
- Recall: 91.6% (catches 9 out of 10 real grid vulnerability events)
- ROC-AUC: 0.977 (true 24-hour ahead forecasting)
- Decision threshold: 0.4 (tuned for safety-first recall)

**ACT Layer - Phase 3 (Pecan Street Austin 2018)**
- 25 real Austin TX households, full year 2018
- HVAC share of total load: 56.3% (Texas hot climate)
- Original peak demand: 105.71 kW
- Grid Saver optimized: 103.41 kW
- Peak reduction: 2.2% (Grid Stabilized)
- Worst day validated: 2018-08-28

**Full SPA Integration - Phase 3**
- Sense triggers: 1,316 hours (15% of year)
- Predict triggers: 1,659 hours (18.9%)
- SPA Actions triggered: 154 hours (dual-confirmation precision)
- Grid Saver only acts when BOTH layers independently confirm risk

---

## Running Locally

```bash
git clone https://github.com/JustineDataEng/grid_saver
cd grid_saver
pip install -r requirements.txt
streamlit run app.py
```

---

## Repository Structure

```
grid_saver/
├── README.md                 # This file
├── app.py                    # Streamlit dashboard - Full SPA Integration
├── gridsaver_phase1.ipynb    # Sense Layer - ERCOT vulnerability detection
├── gridsaver_phase2.ipynb    # Predict Layer - PJM XGBoost forecasting
├── gridsaver_phase3.ipynb    # Full SPA Integration pipeline
└── requirements.txt          # Dependencies
```

---

## Dataset Stack

| Dataset | Records | Role |
|---------|---------|------|
| Electricity Maps US-TEX-ERCO 2025 | 8,760 hourly | Sense Layer |
| PJM_Load_hourly.csv | 32,896 hourly | Predict Layer |
| PJME_hourly.csv | 145,366 hourly | Validation |
| Pecan Street Austin 15-min | 868,096 rows | Act Layer |
| IEA Electricity 2025 | 2020–2027 | Global demand statistics |
| World Bank Enterprise Surveys | 2024 | Infrastructure disruption costs |

---

## The Science

Because power grids operate within narrow reserve margins, even small, coordinated reductions in residential HVAC demand can significantly reduce peak load and prevent system instability.

**Reserve Margin Formula:**
- Peak demand: 9,200 MW
- Grid Saver 4% reduction: 368 MW removed
- New demand: 8,832 MW (grid stabilizes)

**Scaling (proven on real Pecan Street data):**
- 0.0920 kW reduction per home
- 1,000,000 homes = 92 MW removed (baseline scenario)
- Higher reductions achievable under coordinated peak conditions

**SPA Dual-Confirmation Logic:**
- Grid Saver does not trigger on every vulnerability signal
- Both Sense AND Predict must independently confirm risk
- 154 confirmed actions out of 8,760 hours (surgical precision, not blunt response)

---

## Tech Stack

- **Analysis:** Google Colab
- **Code:** GitHub https://github.com/JustineDataEng/grid_saver
- **Deployment:** Streamlit Community Cloud
- **Production path:** Azure Functions + Azure ML

---


