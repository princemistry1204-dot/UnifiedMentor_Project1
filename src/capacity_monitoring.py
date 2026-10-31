def capacity_status(forecast_value, threshold, caution_percent=85):
    """Return a transparent status using a user-entered threshold."""
    if threshold <= 0:
        return "Threshold not configured"
    if forecast_value >= threshold:
        return "High risk"
    if forecast_value >= threshold * caution_percent / 100:
        return "Caution"
    return "Normal"
