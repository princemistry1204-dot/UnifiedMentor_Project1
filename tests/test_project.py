import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from src.data_loader import load_dataset, TARGETS
from src.evaluation import calculate_metrics
from src.forecasting_models import forecast_series
from src.capacity_monitoring import capacity_status


class ProjectTests(unittest.TestCase):
    def test_load_real_dataset(self):
        path = Path(__file__).parents[1] / "data" / "HHS_Unaccompanied_Alien_Children_Program.csv"
        data, report = load_dataset(path)
        self.assertEqual(len(data), 720)
        self.assertEqual(report["blank_rows"], 450)
        self.assertTrue(data["Date"].is_monotonic_increasing)

    def test_date_duplicate_detection(self):
        frame = pd.DataFrame({
            "Date": ["2024-01-01", "2024-01-01"],
            **{column: [1, 2] for column in TARGETS.values()}
        })
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "duplicate.csv"
            frame.to_csv(path, index=False)
            with self.assertRaisesRegex(ValueError, "Duplicate dates"):
                load_dataset(path)

    def test_forecast_horizon_and_nonnegative(self):
        dates = pd.bdate_range("2024-01-01", periods=40)
        series = pd.Series(np.linspace(10, 30, 40), index=dates)
        result = forecast_series(series, horizon=7, model_name="Naive")
        self.assertEqual(len(result), 7)
        self.assertTrue((result["forecast"] >= 0).all())

    def test_metrics_with_zero_actuals(self):
        metrics = calculate_metrics([0, 10, 20], [2, 8, 22])
        self.assertAlmostEqual(metrics["MAE"], 2.0)
        self.assertTrue(np.isnan(calculate_metrics([0, 0], [1, 2])["WAPE (%)"]))

    def test_capacity_threshold(self):
        self.assertEqual(capacity_status(100, 100), "High risk")
        self.assertEqual(capacity_status(90, 100, 85), "Caution")
        self.assertEqual(capacity_status(70, 100, 85), "Normal")

    def test_invalid_horizon(self):
        series = pd.Series([1, 2, 3], index=pd.date_range("2024-01-01", periods=3))
        with self.assertRaises(ValueError):
            forecast_series(series, horizon=0)


if __name__ == "__main__":
    unittest.main()
