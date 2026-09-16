"""
demo.py
-------
Пример инициализации графика с четырьмя последовательностями данных
(Cost / CPA / ROI confirmed / Conversions), как на референсном скриншоте.

Запуск:
    python random_demo.py

Результат:
    - откроет интерактивный график в браузере (fig.show())
    - сохранит его как самодостаточный output.html рядом со скриптом
"""
import numpy as np
import pandas as pd

from chart_builder import SeriesConfig, build_multi_metric_chart

rng = np.random.default_rng(42)

# --- 1. Четыре последовательности данных ------------------------------
dates = pd.date_range("2026-06-01", periods=14, freq="D")

cost = np.clip(30 + np.cumsum(rng.normal(1.5, 3, len(dates))), 5, None)
cpa = np.clip(rng.normal(1.3, 0.3, len(dates)), 0.2, None)
roi = 120 + 60 * np.sin(np.linspace(0, 3, len(dates))) + rng.normal(0, 5, len(dates))
conversions = rng.integers(10, 45, len(dates)).astype(float)

# --- 2. Описание каждой серии: имя, тип отрисовки, цвет, формат значения ---
series = [
    SeriesConfig(name="Cost", values=cost, kind="area", color="#F2B705", value_format="$.2f"),
    SeriesConfig(name="CPA", values=cpa, kind="bar", color="#4C8DF6", value_format=".2f"),
    SeriesConfig(name="ROI confirmed", values=roi, kind="spline", color="#34A853", value_format=".2f"),
    SeriesConfig(name="Conversions", values=conversions, kind="line", color="#B026FF", value_format=".0f"),
]

# --- 3. Сборка и вывод графика ------------------------------------------
fig = build_multi_metric_chart(dates, series, title="Campaign performance")
fig.write_html("output.html", auto_open=False)
fig.show()

print("Готово: интерактивный график сохранён в output.html")
