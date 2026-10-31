import numpy as np

def calculate_metrics(actual, predicted):
    actual = np.asarray(actual, dtype=float)
    predicted = np.asarray(predicted, dtype=float)
    if actual.shape != predicted.shape:
        raise ValueError("Actual and predicted arrays must have the same shape.")
    valid = np.isfinite(actual) & np.isfinite(predicted)
    actual, predicted = actual[valid], predicted[valid]
    if len(actual) == 0:
        raise ValueError("No valid pairs are available for evaluation.")
    errors = actual - predicted
    mae = float(np.mean(np.abs(errors)))
    rmse = float(np.sqrt(np.mean(errors ** 2)))
    denominator = float(np.sum(np.abs(actual)))
    wape = float(np.sum(np.abs(errors)) / denominator * 100) if denominator > 0 else float("nan")
    nonzero = actual != 0
    mape = float(np.mean(np.abs(errors[nonzero] / actual[nonzero])) * 100) if nonzero.any() else float("nan")
    return {"MAE": mae, "RMSE": rmse, "WAPE (%)": wape, "MAPE (%)": mape}
