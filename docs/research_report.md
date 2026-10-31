# Research Report: Predictive Forecasting of Care Load & Placement Demand

## 1. Introduction
This project explores short-term forecasting of aggregate UAC program counts using a Python and Streamlit application.

## 2. Problem statement
Historical operational counts may help users understand recent trends and explore possible near-term values. The purpose is analytical decision support, not individual-level prediction.

## 3. Objectives
- Inspect the source data and report data-quality limitations.
- Explore historical count series.
- Compare baseline, statistical, and machine-learning forecasts.
- Provide a dashboard for reviewing forecasts and a user-defined capacity scenario.

## 4. Dataset description
The supplied CSV has six columns: Date and five count variables. It contains 720 usable observations spanning 12 January 2023 through 21 December 2025, plus 450 completely blank rows.

## 5. Data quality
The loader detects invalid dates, duplicate dates, missing numeric values, and negative counts. The source data is sorted reverse chronologically and the loader sorts it ascending. Reporting dates are irregular, so missing calendar dates are not filled with zeroes.

## 6. Exploratory data analysis
The dashboard includes time-series plots, distribution plots, summary statistics, and a data-quality panel. Interpret apparent patterns with care because reporting dates are not continuous calendar days.

## 7. Feature engineering
The random forest uses lag-1, lag-7, and trailing seven-observation mean features. Features are built from earlier observations only; recursive forecasts use prior predictions rather than future actual values.

## 8. Forecasting methodology
Models include naive persistence, moving average, exponential smoothing, and random forest. Forecasts are constrained to nonnegative values because the targets are counts.

## 9. Training and validation
The application compares models on a chronological holdout. Random shuffling is not used. Rolling-origin validation is a recommended next step for a more rigorous research submission.

## 10. Model evaluation
MAE, RMSE, WAPE, and MAPE are calculated from predictions. MAPE is undefined if no nonzero actual values exist, and WAPE is undefined if the sum of absolute actual values is zero.

## 11. Model comparison
The dashboard calculates the comparison table from the loaded dataset at runtime. No model performance values are pre-filled in this report.

## 12. Forecasting results
Results depend on the chosen target, model, and horizon. Run the app to generate forecasts and metrics from the supplied data. This document does not claim uncomputed results.

## 13. Capacity monitoring
The app supports a user-defined threshold for the HHS care-load series. This is a scenario assumption, not an official capacity value. Warnings are deterministic and do not represent calibrated probabilities.

## 14. Operational recommendations
Use forecasts as one input to planning, review model performance across time periods, and confirm operational assumptions with qualified domain experts.

## 15. Limitations
Reporting dates are irregular; forecast dates are approximated using business days. The current evaluation is a chronological holdout rather than a full walk-forward procedure. The dataset does not identify individual placement readiness or provide an explicit HHS transfer-in measure.

## 16. Conclusion
The project provides a reproducible, beginner-readable starting point for exploring aggregate time-series forecasts. Further validation and domain review are required before operational use.
