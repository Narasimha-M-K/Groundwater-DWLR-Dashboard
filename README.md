# Groundwater Recharge Insight Dashboard (DWLR – NWDP Data)

A lightweight, Python-based decision-support dashboard that analyzes groundwater level readings from DWLR (Digital Water Level Recorder) stations to estimate short-term trends, seasonal deviation, and a simple, explainable groundwater-stress risk index. Built for planners, researchers, and sustainability teams who need interpretable insights instead of raw telemetry values.

## Project Overview

The Groundwater Recharge Insight Dashboard converts groundwater level readings into transparent, human-readable sustainability insights. Instead of relying on complex or black-box analytics, the system focuses on simple, explainable indicators that help decision-makers understand whether groundwater levels are improving, stable, or depleting; how current conditions compare to seasonal baselines; and clear narrative interpretations explaining what the data means. The dashboard supports data ingestion from NWDP groundwater datasets, and also includes a deterministic mock-data mode that generates approximately 5 years of synthetic data for development, testing, and demonstration when API access is unavailable.

## Problem Context and Motivation

Groundwater is one of the most critical natural resources in India, yet field data is often difficult to interpret without analytical tools, locked in raw telemetry logs or spreadsheets, or presented without context or sustainability meaning. Decision-makers do not just need graphs; they need interpretation, trends, and signals that support practical choices. This project bridges the gap between data, understanding, and action by converting water-level readings into structured sustainability indicators that are transparent, auditable, and aligned with policy-style decision workflows.

## Core Features (MVP)

### 1. NWDP Data Ingestion (API and Mock Mode)

Supports ingestion of groundwater level readings from NWDP datasets; configurable mock-data mode generates deterministic multi-year datasets (approximately 5 years) for offline or demo usage; same pipeline works for real or mock inputs.

### 2. Trend and Seasonal Analysis (Explainable Metrics)

Short-term trend indicator using linear regression analysis; Recharge, Stable, or Depleting classification using configurable thresholds; seasonal deviation metric for contextual comparison with historical baselines. Seasonal deviation is conditionally available—it requires sufficient aligned historical windows and may legitimately be unavailable for some stations or time periods. When seasonal deviation cannot be computed, the system continues to operate normally with trend analysis only.

### 3. Composite Risk Index (0–100)

**Status: Not implemented in current MVP**

A future enhancement that will provide a simple, transparent risk score derived from short-term trend signal (60 percent weight) and seasonal deviation indicator (40 percent weight). Outputs will include Low Risk, Moderate Risk, and High Risk bands. No heavy ML or opaque scoring logic.

### 4. Insight Interpreter (Human-Readable Output)

Automatically generates short, policy-style explanations that describe what the metrics indicate, making the dashboard usable beyond technical users.

### 5. Streamlit Dashboard (MVP UI)

Station summary view with trend indicators; station detail view with metrics summary and interpreter explanation text; clean, minimal, decision-focused interface.

## Time Context and Deterministic Behavior

The system uses data-derived time semantics for all analytics. The reference date (effective "now") is derived from the maximum reading date in the database, not from system clock time. This ensures deterministic behavior across machines, dates, and reruns. All UI queries and analytics calculations align to this data-derived reference date, making the system suitable for reproducible analysis and historical data review.

## Technology Stack

Python; Streamlit (dashboard UI); SQLite (lightweight local storage); Pandas and NumPy (data handling and metrics); modular OOP-style architecture.

## System Architecture (Conceptual)

api_client: data ingestion (API or mock mode with deterministic multi-year data generation); data_store: SQLite storage and retrieval with data-derived reference date queries; models: stations, readings, metrics; processing: trend calculation (always available) and seasonal deviation (conditionally available); insights: interpretation message engine; app: Streamlit UI layer. Designed to be clean, modular, and extensible.

## Data Philosophy

This project prioritizes explainable indicators over black-box analytics, clarity over complexity, and decision-support over prediction. Every metric in the system is deterministic, auditable, and transparent, with no hidden transformations or unverifiable claims. The system explicitly acknowledges when metrics cannot be computed due to insufficient data alignment, treating such cases as valid system states rather than errors.

## MVP Development Status

- **Phase 1: Mock-mode offline loop** — Complete. Deterministic multi-year mock data generation (≈5 years).
- **Phase 2: Trend logic** — Complete. Short-term trend calculation using linear regression.
- **Phase 3: Seasonal deviation** — Complete. Conditionally available based on historical data alignment.
- **Phase 4: Composite risk index** — Not implemented. Future enhancement.
- **Phase 5: Insight interpreter** — Complete. Human-readable narrative generation.
- **Phase 6: Simple chart** — Not implemented. Future enhancement.

## Roadmap (Future Enhancements – Not in MVP)

Composite risk index calculation; CSV or PDF export; multi-station comparison views; geospatial mapping or district aggregation; automated alerts or notifications; PostgreSQL migration for scale deployments; integration with rainfall and recharge datasets; calibration by basin or region; chart visualization.

## Green-Skilling and Sustainability Alignment

The project supports data-driven groundwater stewardship and capacity building in environmental analytics, and develops practical skills in Python data engineering, sustainability-focused decision systems, and transparent analytical modeling. It demonstrates how technology can enable responsible resource management rather than just data visualization.

## Disclaimer

This is an MVP prototype intended for learning, demonstration, and capacity-building. It is not an official government platform; metrics are indicative and should not replace expert analysis; real-world deployment would require validation, calibration, and domain review.
