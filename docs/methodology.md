# Methodology

## Data inspection

The supplied CSV has 1,170 rows including 450 fully blank rows. After excluding fully blank rows for analysis, 720 records remain. Dates span 12 January 2023 to 21 December 2025. There are no duplicate dates among usable records, no invalid dates, and no negative values in the five count columns. The source is reverse chronological and is sorted ascending by the loader.

The date coverage spans 1,075 calendar days but has 720 reporting dates. Gaps are preserved because a missing date is not necessarily a zero count.

## Forecast targets

The data provides five aggregate count series. Children in HHS Care is a stock measure. Apprehensions, transfers out of CBP custody, and discharges are flow measures. The dataset does not explicitly contain a separate HHS-transfer-in column, so net HHS transfer pressure cannot be calculated reliably from the available columns.

## Models

Baseline methods are naive persistence and a seven-observation moving average. Exponential smoothing is included as a statistical method. A random forest model uses lag-1, lag-7, and trailing seven-observation mean features. Recursive forecasts feed prior predictions into later steps.

## Evaluation

The app uses a chronological final holdout. Metrics include MAE, RMSE, WAPE, and MAPE where defined. MAPE excludes zero-valued actual observations; WAPE is undefined when all actual values sum to zero. A full walk-forward evaluation is not yet implemented.

## Forecast dates

The original reporting schedule is irregular. Forecast values represent future observation steps. Business-day dates are used for visualization only and should not be interpreted as a verified reporting calendar.

## Capacity monitoring

A user-entered threshold supports a deterministic warning. It is explicitly a scenario assumption, not an official capacity limit. A breach probability is not calculated.
