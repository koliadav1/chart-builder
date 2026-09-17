# График

Комбинированный time-series график на Python (Plotly): 4 серии данных,
каждая своим типом отрисовки — **area / bar / spline / line** в одном
графике, с общим (unified) тултипом при наведении.

## Установка

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Быстрый старт (демо на 4 сгенерированных сериях)

```bash
python random_demo.py
```

Откроется интерактивный график в браузере и сохранится `output.html`
(его можно открыть отдельно, без Python — это самодостаточный файл).

## Как подставить свои 4 последовательности данных

Всё завязано на двух объектах из `chart_builder.py`: `SeriesConfig` и
`build_multi_metric_chart`.

```python
import pandas as pd
from chart_builder import SeriesConfig, build_multi_metric_chart

# 1. Ваши даты (любой sequence — list, pd.Series, DatetimeIndex)
dates = pd.date_range("2026-06-01", periods=30, freq="D")

# 2. Ваши 4 массива значений той же длины, что и dates
cost = [...]          # 30 чисел
cpa = [...]           # 30 чисел
roi = [...]           # 30 чисел
conversions = [...]   # 30 чисел

# 3. Описываете каждую серию: имя, значения, тип отрисовки, цвет, формат значения
series = [
    SeriesConfig(name="Cost",          values=cost,        kind="area",   color="#F2B705", value_format="$.2f"),
    SeriesConfig(name="CPA",           values=cpa,         kind="bar",    color="#4C8DF6", value_format=".2f"),
    SeriesConfig(name="ROI confirmed", values=roi,         kind="spline", color="#34A853", value_format=".2f"),
    SeriesConfig(name="Conversions",   values=conversions, kind="line",   color="#B026FF", value_format=".0f"),
]

# 4. Собираете фигуру и выводите её как угодно:
fig = build_multi_metric_chart(dates, series, title="Мой дашборд")

fig.show()                       # интерактивно (браузер / Jupyter)
fig.write_html("output.html")    # самодостаточный HTML-файл
# fig.write_image("chart.png")   # статичный PNG (нужен доп. пакет kaleido)
```

### Параметры `SeriesConfig`

| Поле | Назначение |
|---|---|
| `name` | Название серии — идёт в легенду и в тултип |
| `values` | Массив значений (той же длины, что `dates`) |
| `kind` | `"area"`, `"bar"`, `"spline"` или `"line"` |
| `color` | Hex-цвет серии, напр. `"#34A853"` |
| `value_format` | Формат числа в тултипе (D3-формат), напр. `"$.2f"`, `",.0f"`, `".1%"` |
| `line_width` | Толщина линии для area/spline/line (не влияет на bar) |

Порядок серий в списке — это и порядок отрисовки, и порядок строк в тултипе.
Можно передать любое количество серий, а не строго 4 — если появится пятая
метрика, просто добавьте ещё один `SeriesConfig`.

## Загрузка реальных данных: CSV / БД / API — одним методом

Помимо ручной сборки `SeriesConfig` (как в примере выше), есть готовый
универсальный загрузчик `load_series()` из `data_loader.py`. Он принимает
данные практически в любом виде и сам приводит их к единой таблице
(pandas.DataFrame) внутри, так что вызывающему коду не нужно знать,
откуда данные пришли:

| Что передать в `data=` | Когда используется |
|---|---|
| `"path/to/file.csv"` (строка) | данные лежат в CSV-файле |
| `pandas.DataFrame` | результат `pd.read_sql(query, connection)` — данные из БД |
| `[{"date": ..., "cost": ...}, ...]` (список словарей) | типичный `response.json()` из REST API |
| `{"date": [...], "cost": [...], ...}` (словарь списков) | данные собраны вручную/из своего кода |

Пример (CSV):

```python
from chart_builder import build_multi_metric_chart
from data_loader import load_series

metrics = {
    # ключ — имя колонки в данных, значение — как её рисовать
    "cost":          {"name": "Cost",          "kind": "area",   "color": "#F2B705", "value_format": "$.2f"},
    "cpa":           {"name": "CPA",           "kind": "bar",    "color": "#4C8DF6"},
    "roi_confirmed": {"name": "ROI confirmed", "kind": "spline", "color": "#34A853"},
    "conversions":   {"name": "Conversions",   "kind": "line",   "color": "#B026FF", "value_format": ".0f"},
}

dates, series = load_series(data="data/sample_data.csv", date_column="date", metrics=metrics)
fig = build_multi_metric_chart(dates, series, title="Мой дашборд")
fig.show()
```

Пример (БД через SQL):

```python
import sqlite3
import pandas as pd
from data_loader import load_series

conn = sqlite3.connect("my.db")
df = pd.read_sql("SELECT date, cost, cpa, roi_confirmed, conversions FROM metrics", conn)
dates, series = load_series(df, date_column="date", metrics=metrics)
```

Пример (API):

```python
import requests
from data_loader import load_series

api_data = requests.get("https://api.example.com/metrics").json()  # список словарей
dates, series = load_series(api_data, date_column="date", metrics=metrics)
```

Во всех трёх случаях дальше используется один и тот же
`build_multi_metric_chart(dates, series)` — разница только в том, чем
заполнить `data=`. Рабочие примеры всех трёх сценариев — в
`real_data_demo.py`, а тестовый CSV — в `data/sample_data.csv`.

Если у ваших колонок другие названия — просто поменяйте ключи в словаре `metrics` на реальные названия колонок; переименовывать сами данные не нужно.

## Структура репозитория

```
chart-builder/
├── chart_builder.py         # переиспользуемая логика построения графика (SeriesConfig, build_multi_metric_chart)
├── data_loader.py           # универсальный загрузчик: CSV / DataFrame / список словарей -> (dates, series)
├── random_demo.py                  # пример со случайными данными
├── real_data_demo.py   # пример с реальными данными (CSV / API-like / DataFrame)
├── data/
│   └── sample_data.csv      # тестовый CSV с 4 метриками для real_data_demo.py
├── requirements.txt
└── README.md
```