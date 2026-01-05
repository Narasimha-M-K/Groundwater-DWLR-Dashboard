# MVP Development Flow — Groundwater Recharge Insight Dashboard

This project follows an intentional, MVP-first development workflow. Features are implemented in small, verifiable steps with review-before-apply discipline. No structural changes are made unless required by a working feature.

## Phase 1 — Mock-Mode Offline Loop (Baseline Functionality)
Goal: App works fully offline with synthetic groundwater data.

- Create mock stations
- Generate 180–365 days of synthetic groundwater readings with natural variation
- Save data to SQLite (DataStore)
- Retrieve and display data in Streamlit UI

Outcome: End-to-end pipeline works (data → storage → UI) before analytics.

## Phase 2 — Trend Logic
- Implement moving-average-based short-term trend signal
- Classify as Recharging / Stable / Depleting
- Thresholds remain configurable

## Phase 3 — Seasonal Deviation
- Compute deviation from seasonal baseline
- Provide contextual interpretation rather than complex hydrological modeling

## Phase 4 — Composite Risk Index (0–100)
- Trend component weight: 0.6
- Seasonal deviation weight: 0.4
- Output risk bands: Low / Moderate / High

## Phase 5 — Insight Interpreter Refinement
- Convert metrics into short, neutral, policy-style messages
- Emphasis on clarity, transparency, and explainability

## Phase 6 — Simple Chart
- Add a basic time-series groundwater level plot
- Minimal visual complexity; utility over design

## Phase 7 — MVP Lockdown
- Sanity pass and cleanup
- Remove placeholders not used in MVP
- API ingestion remains a future enhancement phase

## Guiding Principles
- MVP first; avoid premature expansion
- Modify structure only when required by real functionality
- Maintain transparent, explainable analytics
- Treat Cursor as a junior developer — propose → review → approve → apply
