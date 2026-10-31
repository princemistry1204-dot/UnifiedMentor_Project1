# Testing Report

## Automated checks executed in the build environment

Command: `python -m unittest discover -s tests -v`

Exit code: `0`

```text
Spreadsheet runtime warmup failed during python startup
Traceback (most recent call last):
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/patches/warm_spreadsheet_runtime_on_startup.py", line 26, in warm_spreadsheet_runtime_on_startup
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/spreadsheet_warmup.py", line 785, in warm_spreadsheet_runtime
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/spreadsheet_warmup.py", line 718, in _warm_feature_flows
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/spreadsheet_warmup.py", line 509, in _warm_drawing_and_image_flows
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/generated/interface/models.py", line 32861, in bring_to_front
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/rpc/remote.py", line 764, in __call__
  File "/tmp/tmp.QlpUkOUI9D/artifact_tool_v2-2.8.66/artifact_tool/rpc/client.py", line 175, in call
artifact_tool.rpc.client.RemoteError: Element ordering requires an owning element collection.
test_capacity_threshold (test_project.ProjectTests.test_capacity_threshold) ... ok
test_date_duplicate_detection (test_project.ProjectTests.test_date_duplicate_detection) ... ok
test_forecast_horizon_and_nonnegative (test_project.ProjectTests.test_forecast_horizon_and_nonnegative) ... ok
test_invalid_horizon (test_project.ProjectTests.test_invalid_horizon) ... ok
test_load_real_dataset (test_project.ProjectTests.test_load_real_dataset) ... ok
test_metrics_with_zero_actuals (test_project.ProjectTests.test_metrics_with_zero_actuals) ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.021s

OK
```

Syntax compilation: `python -m compileall -q app.py src tests`

Exit code: `0`

## Coverage
- Loading the supplied real dataset and checking row counts.
- Duplicate-date detection.
- Forecast horizon and nonnegative outputs.
- Error metrics with zero actual values.
- Capacity threshold classification.
- Invalid forecast horizon handling.

## Environment limitation
Streamlit is not installed in the build environment, so a live dashboard/browser startup check could not be performed here. Install dependencies using `pip install -r requirements.txt`, then launch with `streamlit run app.py`.

## Known limitations
- No full Streamlit browser interaction test is included.
- Walk-forward validation and calibrated prediction intervals are not implemented.
- Business-day forecast dates are approximate because reporting dates are irregular.
