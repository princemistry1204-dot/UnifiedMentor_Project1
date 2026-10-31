import time
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from src.evaluation import calculate_metrics
from statsmodels.tsa.holtwinters import ExponentialSmoothing

def _future_dates(index, horizon):
    last_date = pd.Timestamp(index[-1])
    # Source reporting dates are irregular and often omit weekends/holidays.
    # Business days are a display approximation, not a claim about the source schedule.
    return pd.bdate_range(last_date + pd.offsets.BDay(1), periods=horizon)

def forecast_series(series, horizon=7, model_name="Naive"):
    """Fit a simple model and return a nonnegative multi-step forecast."""
    values = pd.Series(series).dropna().astype(float).sort_index()
    if len(values) < 2:
        raise ValueError("At least two observations are needed to forecast.")
    if horizon < 1:
        raise ValueError("Forecast horizon must be at least 1.")

    started = time.perf_counter()
    if model_name == "Naive":
        predictions = np.repeat(values.iloc[-1], horizon)
    elif model_name == "Moving average":
        window = min(7, len(values))
        predictions = np.repeat(values.iloc[-window:].mean(), horizon)
    elif model_name == "Exponential smoothing":
        try:
            if len(values) >= 10:
                fitted = ExponentialSmoothing(values, trend="add", seasonal=None).fit(optimized=True)
            else:
                fitted = ExponentialSmoothing(values, trend=None, seasonal=None).fit(optimized=True)
            predictions = np.asarray(fitted.forecast(horizon), dtype=float)
        except Exception:
            # A stable fallback keeps the app usable if statsmodels fitting fails.
            predictions = np.repeat(values.iloc[-7:].mean(), horizon)
    elif model_name == "Random forest":
        predictions = _random_forest_recursive(values, horizon)
    else:
        raise ValueError(f"Unknown model: {model_name}")

    predictions = np.maximum(np.asarray(predictions, dtype=float), 0)
    forecast_dates = _future_dates(values.index, horizon)
    result = pd.DataFrame({"forecast": predictions}, index=forecast_dates)
    result.index.name = "Date"
    result.attrs["runtime_seconds"] = time.perf_counter() - started
    return result


def _random_forest_recursive(values, horizon):
    values = np.asarray(values, dtype=float)
    if len(values) < 15:
        return np.repeat(values[-min(7, len(values)):].mean(), horizon)

    rows, targets = [], []
    for position in range(7, len(values)):
        rows.append([
            values[position - 1],
            values[position - 7],
            values[max(0, position - 7):position].mean(),
        ])
        targets.append(values[position])

    model = RandomForestRegressor(n_estimators=150, max_depth=6, random_state=42, n_jobs=-1)
    model.fit(np.asarray(rows), np.asarray(targets))
    history = list(values)
    predictions = []
    for _ in range(horizon):
        features = [[history[-1], history[-7], float(np.mean(history[-7:]))]]
        prediction = max(0.0, float(model.predict(features)[0]))
        predictions.append(prediction)
        history.append(prediction)
    return predictions


def compare_models(series, horizon=7):
    """Compare models on a chronological final holdout."""
    

    values = pd.Series(series).dropna().astype(float).sort_index()
    holdout_size = max(horizon, int(round(len(values) * 0.2)))
    holdout_size = min(holdout_size, len(values) // 3)
    if holdout_size < 2:
        return pd.DataFrame([{"Model": "Not enough data", "MAE": np.nan, "RMSE": np.nan, "WAPE (%)": np.nan}])

    train = values.iloc[:-holdout_size]
    test = values.iloc[-holdout_size:]
    rows = []
    for name in ["Naive", "Moving average", "Exponential smoothing", "Random forest"]:
        try:
            prediction = forecast_series(train, len(test), name)["forecast"].to_numpy()
            metrics = calculate_metrics(test.to_numpy(), prediction)
            rows.append({"Model": name, **metrics, "Holdout observations": len(test)})
        except Exception as exc:
            rows.append({"Model": name, "MAE": np.nan, "RMSE": np.nan, "WAPE (%)": np.nan,
                         "Holdout observations": len(test), "Note": str(exc)})
    return pd.DataFrame(rows).sort_values("MAE", na_position="last").reset_index(drop=True)
