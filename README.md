# График

Комбинированный time-series график на Python (Plotly): 4 серии данных,
каждая своим типом отрисовки — **area / bar / spline / line** в одном
графике, с общим тултипом при наведении.

## Установка

```bash
python -m venv venv
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
Можно передать любое количество серий, а не строго 4 — если появится пятая метрика, просто добавьте ещё один `SeriesConfig`.

## Структура репозитория

```
multi-metric-chart/
├── chart_builder.py   # переиспользуемая логика построения графика
├── random_demo.py            # пример с 4 сгенерированными сериями
├── requirements.txt
└── README.md
```