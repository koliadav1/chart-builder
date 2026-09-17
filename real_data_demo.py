"""
real_data_demo.py
-----------------------
Три примера, как строить график на РЕАЛЬНЫХ данных через load_series(),
вместо случайных данных из random_demo.py. load_series принимает данные откуда
угодно и сам приводит их к единому виду/

Запуск:
    python real_data_demo.py
"""
from chart_builder import build_multi_metric_chart
from data_loader import load_series

metrics = {
    "cost": {"name": "Cost", "kind": "area", "color": "#F2B705", "value_format": "$.2f"},
    "cpa": {"name": "CPA", "kind": "bar", "color": "#4C8DF6"},
    "roi_confirmed": {"name": "ROI confirmed", "kind": "spline", "color": "#34A853"},
    "conversions": {"name": "Conversions", "kind": "line", "color": "#B026FF", "value_format": ".0f"},
}


# --- Вариант 1: данные из CSV-файла --------------------------------------
dates, series = load_series(
    data="data/sample_data.csv",
    date_column="date",
    metrics=metrics,
)
fig = build_multi_metric_chart(dates, series, title="Из CSV-файла")
fig.write_html("output_from_csv.html")
print("Сохранено: output_from_csv.html (источник — data/sample_data.csv)")


# --- Вариант 2: данные "из API" (список словарей / JSON) ------------------
api_like_data = [
    {"date": "2026-06-01", "cost": 31.5, "cpa": 1.29, "roi_confirmed": 119.76, "conversions": 42},
    {"date": "2026-06-02", "cost": 33.9, "cpa": 1.51, "roi_confirmed": 134.29, "conversions": 39},
    {"date": "2026-06-03", "cost": 34.58, "cpa": 0.9, "roi_confirmed": 139.07, "conversions": 34},
]
dates, series = load_series(
    data=api_like_data,
    date_column="date",
    metrics=metrics,
)
fig = build_multi_metric_chart(dates, series, title="Из API (список словарей)")
fig.write_html("output_from_api.html")
print("Сохранено: output_from_api.html (источник — список словарей, как из API)")


# --- Вариант 3: данные "из БД" (pandas.DataFrame) --------------------------
import pandas as pd

df_like_from_db = pd.read_csv("data/sample_data.csv")
dates, series = load_series(
    data=df_like_from_db,
    date_column="date",
    metrics=metrics,
)
fig = build_multi_metric_chart(dates, series, title="Из готового DataFrame (например, из БД)")
fig.write_html("output_from_dataframe.html")
print("Сохранено: output_from_dataframe.html (источник — pandas.DataFrame)")
