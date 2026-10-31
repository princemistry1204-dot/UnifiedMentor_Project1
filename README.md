# Predictive Forecasting of Care Load & Placement Demand

A Python and Streamlit project for exploring aggregate historical UAC program counts and generating short-term time-series forecasts.

## Important note

This is an educational planning prototype, not an official government forecasting system. It does not predict outcomes for individual children. Forecasts are estimates and should be interpreted alongside operational context.

## Dataset included

`data/HHS_Unaccompanied_Alien_Children_Program.csv` is the original CSV supplied for this project. The loader removes completely blank trailing rows for analysis but does not modify the source file.

The file contains 720 usable observations from 12 January 2023 through 21 December 2025, plus 450 completely blank rows. Dates are unique and the data is reverse chronological in the original file. Reporting dates are irregular: not every calendar date has a record. Missing dates are not filled with zeroes.

## Setup

Python 3.10 or later is recommended.

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
streamlit run app.py
```

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

Open the local address shown in the terminal by Streamlit.

## Project structure

```text
care_load_forecasting/
├── app.py
├── requirements.txt
├── README.md
├── data/
│   └── HHS_Unaccompanied_Alien_Children_Program.csv
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── forecasting_models.py
│   ├── evaluation.py
│   └── capacity_monitoring.py
├── tests/
│   └── test_project.py
├── outputs/
└── docs/
    ├── methodology.md
    ├── research_report.md
    ├── executive_summary.md
    └── testing_report.md
```

## Forecast targets

The dashboard can explore all five available numeric series:
- Children apprehended and placed in CBP custody
- Children in CBP custody
- Children transferred out of CBP custody
- Children in HHS Care
- Children discharged from HHS Care

These are not interchangeable. Care load is a stock measured at a point in time; transfers and discharges are flows over a period.

## Models

The app includes:
- Naive forecast
- Moving-average forecast
- Exponential smoothing
- Random forest with lag features and recursive multi-step prediction

The model comparison uses a chronological holdout. It does not randomly shuffle dates. More extensive walk-forward validation and residual-calibrated prediction intervals are future improvements. The dashboard does not claim a fabricated accuracy percentage.

## Data handling

- Dates are parsed and sorted chronologically.
- Completely blank rows are removed from the analysis copy.
- Duplicate dates, invalid dates, negative counts, and invalid numeric values produce clear errors rather than silent corrections.
- Comma-formatted counts are parsed as numbers.
- Missing calendar dates are reported, not converted to zero.
- Forecast display dates use business days as an approximation because the source reporting schedule is irregular.

## Capacity scenario

The care-load threshold in the dashboard is user-defined. It is not an official capacity figure. The warning is a deterministic comparison against the selected threshold; no breach probability is calculated.

## Run tests

```bash
python -m unittest discover -s tests -v
```

## Limitations

- Reporting dates are irregular and omit many calendar days. The app forecasts the next observation steps and uses business-day dates only for display.
- The compact holdout comparison is not a full rolling-origin evaluation.
- Exponential smoothing and random forest performance may vary with the installed dependency versions.
- No capacity threshold is supplied as an official value.
- The data does not support individual placement-readiness predictions.
