"""
data_loader.py
---------------
Один универсальный метод — load_series() — который принимает данные ЛЮБОГО
происхождения (CSV-файл, готовый pandas.DataFrame, ответ из БД, JSON из API)
и приводит их к единому виду: (dates, series), готовому для передачи прямо
в build_multi_metric_chart() из chart_builder.py.
"""

from pathlib import Path
from typing import Mapping, Sequence, Union
import pandas as pd

from chart_builder import SeriesConfig

DataSource = Union[
    str,                    # путь к CSV-файлу, например "data/report.csv"
    Path,                   # то же самое, но объектом Path вместо строки
    pd.DataFrame,           # уже готовая pandas-таблица (например, из pd.read_sql для БД)
    Mapping[str, Sequence],  # словарь {"date": [...], "cost": [...], ...} — удобно собирать вручную
    Sequence[Mapping],      # список словарей [{"date": ..., "cost": ...}, ...] — типичный ответ API в JSON
]


def load_series(
    data: DataSource,
    date_column: str,
    metrics: dict[str, dict],
) -> tuple[list, list[SeriesConfig]]:
    """Приводит данные любого происхождения к (dates, series) для графика.

    Параметры:
      data:
        Что угодно из списка DataSource выше:
          - "path/to/file.csv"                       — путь к CSV-файлу
          - pandas.DataFrame                          — например, результат pd.read_sql(...) из БД
          - {"date": [...], "cost": [...], ...}       — словарь колонок (списки одной длины)
          - [{"date": ..., "cost": ...}, {...}, ...]  — список словарей (например response.json() из API)

      date_column:
        Имя колонки/ключа, в которой лежат даты, например "date".

      metrics:
        Словарь: ключ — имя колонки с числами, значение — словарь с
        параметрами этой серии для графика. Пример:

            {
                "cost":         {"name": "Cost",          "kind": "area",   "color": "#F2B705", "value_format": "$.2f"},
                "cpa":          {"name": "CPA",            "kind": "bar",    "color": "#4C8DF6"},
                "roi_confirmed":{"name": "ROI confirmed",  "kind": "spline", "color": "#34A853"},
                "conversions":  {"name": "Conversions",    "kind": "line",   "color": "#B026FF", "value_format": ".0f"},
            }

        Обязательные под-ключи: "kind" и "color". "name" и "value_format"
        необязательны — если не указать "name", возьмётся имя колонки;
        если не указать "value_format" — будет использовано ".2f" по
        умолчанию (как в SeriesConfig).

    Возвращает:
        (dates, series) — кортеж из списка дат и списка SeriesConfig,
        который можно сразу передать в build_multi_metric_chart(dates, series).
    """

    # --- Шаг 1: приводим "data" к единому виду — pandas.DataFrame ---

    if isinstance(data, pd.DataFrame):
        df = data.copy()

    elif isinstance(data, (str, Path)):
        df = pd.read_csv(data)

    else:
        df = pd.DataFrame(data)

    # --- Шаг 2: нормализуем колонку с датами ---

    df[date_column] = pd.to_datetime(df[date_column])
    df = df.sort_values(date_column).reset_index(drop=True)
    dates = df[date_column].tolist()

    # --- Шаг 3: строим SeriesConfig для каждой запрошенной метрики ---

    series: list[SeriesConfig] = []
    for column, cfg in metrics.items():
        if column not in df.columns:
            raise KeyError(
                f"Колонка '{column}' не найдена в данных. "
                f"Доступные колонки: {list(df.columns)}"
            )
        series.append(
            SeriesConfig(
                name=cfg.get("name", column),
                values=df[column].tolist(),
                kind=cfg["kind"],
                color=cfg["color"],
                value_format=cfg.get("value_format", ".2f"),
                line_width=cfg.get("line_width", 2.5),
            )
        )
    return dates, series
