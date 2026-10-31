from pathlib import Path
import pandas as pd

DATE_COLUMN = "Date"
TARGETS = {
    "Children apprehended and placed in CBP custody": "Children apprehended and placed in CBP custody*",
    "Children in CBP custody": "Children in CBP custody",
    "Children transferred out of CBP custody": "Children transferred out of CBP custody",
    "Children in HHS Care": "Children in HHS Care",
    "Children discharged from HHS Care": "Children discharged from HHS Care",
}

def load_dataset(source):
    """Load a CSV/Excel file and standardize dates and count columns."""
    if hasattr(source, "name"):
        name = source.name.lower()
        if name.endswith(".csv"):
            raw = pd.read_csv(source)
        elif name.endswith((".xlsx", ".xls")):
            raw = pd.read_excel(source)
        else:
            raise ValueError("Please upload a CSV or Excel file.")
    else:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"Dataset not found: {path}")
        if path.suffix.lower() == ".csv":
            raw = pd.read_csv(path)
        elif path.suffix.lower() in (".xlsx", ".xls"):
            raw = pd.read_excel(path)
        else:
            raise ValueError("Supported formats are CSV and Excel.")

    original_rows = len(raw)
    blank_rows = int(raw.isna().all(axis=1).sum())
    raw = raw.dropna(how="all").copy()

    required = [DATE_COLUMN, *TARGETS.values()]
    missing_columns = [column for column in required if column not in raw.columns]
    if missing_columns:
        raise ValueError("Missing required columns: " + ", ".join(missing_columns))

    raw[DATE_COLUMN] = pd.to_datetime(raw[DATE_COLUMN], errors="coerce")
    bad_dates = int(raw[DATE_COLUMN].isna().sum())
    if bad_dates:
        raise ValueError(f"{bad_dates} nonblank rows have invalid dates; review the source file.")

    for column in TARGETS.values():
        # The HHS care-load column contains comma-formatted values in the source CSV.
        cleaned = raw[column].astype(str).str.replace(",", "", regex=False).str.strip()
        raw[column] = pd.to_numeric(cleaned, errors="coerce")

    bad_numeric = {c: int(raw[c].isna().sum()) for c in TARGETS.values() if raw[c].isna().any()}
    if bad_numeric:
        raise ValueError(f"Missing or invalid numeric values found: {bad_numeric}")

    negative_counts = {c: int((raw[c] < 0).sum()) for c in TARGETS.values() if (raw[c] < 0).any()}
    if negative_counts:
        raise ValueError(f"Negative counts found and not automatically corrected: {negative_counts}")

    duplicate_dates = int(raw[DATE_COLUMN].duplicated().sum())
    if duplicate_dates:
        raise ValueError(f"Duplicate dates found ({duplicate_dates}); resolve them before forecasting.")

    data = raw.sort_values(DATE_COLUMN).rename(columns={DATE_COLUMN: "Date"}).reset_index(drop=True)
    data["Date"] = data["Date"].dt.normalize()

    start_date, end_date = data["Date"].min(), data["Date"].max()
    calendar_days = (end_date - start_date).days + 1
    unique_dates = int(data["Date"].nunique())
    report = {
        "original_rows": int(original_rows),
        "blank_rows": blank_rows,
        "usable_rows": int(len(data)),
        "bad_dates": bad_dates,
        "duplicate_dates": duplicate_dates,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "unique_dates": unique_dates,
        "calendar_days": int(calendar_days),
        "missing_calendar_days": int(calendar_days - unique_dates),
        "negative_counts": negative_counts,
        "numeric_missing_values": bad_numeric,
        "columns": list(raw.columns),
    }
    # ISO strings keep the report JSON-serializable for Streamlit.
    return data, report


def inspect_dataset(path):
    """Convenience helper for scripts and tests."""
    data, report = load_dataset(path)
    report["dtypes"] = {column: str(dtype) for column, dtype in data.dtypes.items()}
    report["missing_values"] = {column: int(value) for column, value in data.isna().sum().items()}
    return data, report
