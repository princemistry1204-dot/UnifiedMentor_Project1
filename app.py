import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.data_loader import load_dataset, inspect_dataset, TARGETS
from src.forecasting_models import forecast_series, compare_models
from src.evaluation import calculate_metrics
from src.capacity_monitoring import capacity_status

st.set_page_config(page_title="Care Load Forecasting", page_icon="📈", layout="wide")

st.title("Predictive Forecasting of Care Load & Placement Demand")
st.caption("A practical forecasting prototype built with Python and Streamlit.")
st.info(
    "This is an analytical planning prototype, not an official government forecasting system. "
    "Forecasts are estimates and should not be used to make decisions about individual children."
)

with st.sidebar:
    st.header("Forecast settings")
    uploaded = st.file_uploader("Use another CSV or Excel file", type=["csv", "xlsx", "xls"])
    horizon = st.selectbox("Forecast horizon (observations)", [7, 14, 30], index=0)
    target_label = st.selectbox("Series to forecast", list(TARGETS.keys()), index=3)
    model_name = st.selectbox(
        "Forecasting model",
        ["Moving average", "Naive", "Exponential smoothing", "Random forest"],
        index=2,
    )
    st.divider()
    st.subheader("Optional capacity scenario")
    capacity = st.number_input(
        "User-defined care-load threshold",
        min_value=0,
        value=3000,
        step=100,
        help="Scenario assumption only; this is not an official capacity figure.",
    )
    caution_pct = st.slider("Caution level (% of threshold)", 50, 95, 85)

try:
    source = uploaded if uploaded is not None else (
        "data/HHS_Unaccompanied_Alien_Children_Program.csv"
    )
    data, report = load_dataset(source)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

target = TARGETS[target_label]
series = data.set_index("Date")[target].dropna().sort_index()
if len(series) < 20:
    st.error("There are too few usable observations for a meaningful model comparison.")
    st.stop()

forecast = forecast_series(series, horizon=horizon, model_name=model_name)
comparison = compare_models(series, horizon=min(horizon, max(1, len(series) // 5)))

overview, exploration, forecasting, models, data_tab = st.tabs(
    ["Executive overview", "Explore the data", "Forecast", "Model comparison", "Data & quality"]
)

with overview:
    latest = series.iloc[-1]
    last_date = series.index[-1]
    future_value = float(forecast["forecast"].iloc[-1])
    first, second, third, fourth = st.columns(4)
    first.metric("Latest observed value", f"{latest:,.0f}", help=f"Reported on {last_date:%d %b %Y}")
    second.metric("Forecast at horizon", f"{future_value:,.0f}", f"{future_value-latest:+,.0f}")
    third.metric("Observations available", f"{len(series):,}")
    fourth.metric("Forecast horizon", f"{horizon} observations")

    if target_label == "Children in HHS Care":
        status = capacity_status(future_value, capacity, caution_pct)
        st.subheader("Capacity scenario check")
        a, b = st.columns(2)
        a.metric("User-defined threshold", f"{capacity:,.0f}")
        b.metric("Headroom at horizon", f"{capacity-future_value:,.0f}")
        if status == "High risk":
            st.error(f"{status}: the point forecast reaches or exceeds the user-defined threshold.")
        elif status == "Caution":
            st.warning(f"{status}: the point forecast is approaching the user-defined threshold.")
        else:
            st.success(f"{status}: the point forecast remains below the caution level.")
        st.caption("This is a deterministic threshold check, not a breach probability.")
    else:
        st.caption("Capacity monitoring is available for the HHS care-load series.")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=series.index[-120:], y=series.iloc[-120:], mode="lines", name="Observed"))
    fig.add_trace(go.Scatter(x=forecast.index, y=forecast["forecast"], mode="lines+markers", name="Forecast"))
    fig.update_layout(title=f"Recent history and {horizon}-observation forecast", xaxis_title="Date", yaxis_title=target_label)
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("What this forecast means")
    st.write(
        f"The selected **{model_name}** model extends the historical pattern in **{target_label}**. "
        "The forecast is based on the reported observations, which are not present for every calendar day. "
        "Future dates are estimated on a business-day calendar for display, so reporting dates may differ."
    )

with exploration:
    st.subheader("Historical observations")
    st.write(f"Date range: **{data['Date'].min():%d %b %Y}** to **{data['Date'].max():%d %b %Y}**")
    chosen = st.multiselect("Series to show", list(TARGETS.keys()), default=[target_label])
    fig = px.line(data, x="Date", y=[TARGETS[name] for name in chosen], title="Historical time series")
    st.plotly_chart(fig, use_container_width=True)

    left, right = st.columns(2)
    with left:
        st.subheader("Distribution")
        st.plotly_chart(px.histogram(data, x=target, nbins=30, title=f"Distribution: {target_label}"), use_container_width=True)
    with right:
        st.subheader("Summary statistics")
        st.dataframe(series.describe().to_frame("Value"), use_container_width=True)

with forecasting:
    st.subheader(f"{target_label}: forecast")
    st.write(f"Model: **{model_name}** · Horizon: **{horizon} observations**")
    st.dataframe(forecast.reset_index(names="Date").rename(columns={"forecast": "Forecast"}), use_container_width=True)
    csv = forecast.reset_index(names="Date").to_csv(index=False).encode("utf-8")
    st.download_button("Download forecast CSV", csv, file_name="forecast.csv", mime="text/csv")
    st.caption("The displayed forecast dates use business days as a convenient approximation. Actual reporting schedules may vary.")

with models:
    st.subheader("Chronological holdout comparison")
    st.write(
        "Models are evaluated on the final chronological holdout. This compact comparison is a baseline, "
        "not a substitute for a full walk-forward study. The final holdout is not randomly shuffled."
    )
    st.dataframe(comparison, use_container_width=True)
    st.caption("MAE and RMSE are error measures; lower values are better. No universal accuracy percentage is reported.")

with data_tab:
    st.subheader("Dataset summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Rows after removing blank lines", f"{report['usable_rows']:,}")
    c2.metric("Completely blank rows removed", f"{report['blank_rows']:,}")
    c3.metric("Duplicate dates", f"{report['duplicate_dates']:,}")
    st.write(f"**Source date range:** {pd.Timestamp(report['start_date']):%d %b %Y} – {pd.Timestamp(report['end_date']):%d %b %Y}")
    st.write(f"**Unique reporting dates:** {report['unique_dates']:,}")
    st.write(f"**Calendar days covered:** {report['calendar_days']:,}")
    st.write(f"**Missing calendar dates:** {report['missing_calendar_days']:,}")
    st.warning(
        "The source has gaps between reporting dates. They are not filled with zeroes because a missing "
        "report is not evidence of zero activity."
    )
    st.subheader("Data quality checks")
    st.json(report)
    st.subheader("Processed data preview")
    st.dataframe(data.head(20), use_container_width=True)
