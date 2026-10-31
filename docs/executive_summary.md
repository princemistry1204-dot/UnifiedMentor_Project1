# Executive Summary

This project provides a Streamlit dashboard for exploring historical aggregate counts in the Unaccompanied Alien Children program and generating short-term forecasts. It includes baseline, statistical, and machine-learning models, a chronological holdout comparison, and an optional user-defined care-load threshold scenario.

The source file contains 720 usable records from 12 January 2023 through 21 December 2025, plus 450 completely blank rows. Reporting dates are irregular, so missing dates are not treated as zero activity.

Forecasts and metrics are generated at runtime from the selected series. No fixed accuracy figure is presented. The capacity threshold is an assumption entered by the user and is not an official capacity limit.

The tool is intended for exploratory planning and education. It does not predict individual outcomes and should not be treated as an official government forecasting system.
