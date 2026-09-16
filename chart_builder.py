"""
chart_builder.py
-----------------
Переиспользуемый билдер комбинированного time-series графика с четырьмя
метриками, отрисованными как area / spline / line / bar — по образцу
референсного скриншота (светлая карточка, единый тултип с датой в шапке,
цветными маркерами и жирными значениями, вертикальный crosshair при наведении).
"""

from dataclasses import dataclass
from typing import Literal, Sequence

import plotly.graph_objects as go

SeriesType = Literal["area", "spline", "line", "bar"]


@dataclass
class SeriesConfig:
    """Описание одной серии данных."""

    name: str
    values: Sequence[float]
    kind: SeriesType
    color: str
    value_format: str = ".2f"   # питон/D3-формат для значения в тултипе, напр. "$.2f", ",.0f"
    line_width: float = 2.5


def build_multi_metric_chart(
    dates: Sequence,
    series: Sequence[SeriesConfig],
    title: str | None = None,
    date_format: str = "%d.%m.%Y",
) -> go.Figure:
    """Строит комбинированный график из списка SeriesConfig.

    Каждая серия рисуется тем типом трейса, который указан в ``kind``:
      - "area"   -> заливка снизу (Cost на референсе)
      - "bar"    -> тонкие бары (CPA на референсе)
      - "spline" -> сглаженная кривая (ROI confirmed на референсе)
      - "line"   -> ломаная с квадратными маркерами (Conversions на референсе)

    Порядок в списке ``series`` — это и порядок отрисовки (z-order), и порядок
    строк в тултипе.
    """
    fig = go.Figure()
    x = list(dates)

    for cfg in series:
        hovertemplate = f"{cfg.name}: <b>%{{y:{cfg.value_format}}}</b><extra></extra>"
        common = dict(name=cfg.name, x=x, y=list(cfg.values), hovertemplate=hovertemplate)

        if cfg.kind == "bar":
            fig.add_trace(
                go.Bar(
                    **common,
                    marker=dict(color=cfg.color, cornerradius=6),
                    opacity=0.9,
                )
            )
        elif cfg.kind == "area":
            fig.add_trace(
                go.Scatter(
                    **common,
                    mode="lines",
                    line=dict(color=cfg.color, width=cfg.line_width, shape="linear"),
                    fill="tozeroy",
                    fillcolor=_with_alpha(cfg.color, 0.28),
                )
            )
        elif cfg.kind == "spline":
            fig.add_trace(
                go.Scatter(
                    **common,
                    mode="lines",
                    line=dict(color=cfg.color, width=cfg.line_width, shape="spline", smoothing=1.1),
                )
            )
        elif cfg.kind == "line":
            fig.add_trace(
                go.Scatter(
                    **common,
                    mode="lines+markers",
                    line=dict(color=cfg.color, width=cfg.line_width, shape="linear"),
                    marker=dict(symbol="square", size=7, color=cfg.color),
                )
            )
        else:
            raise ValueError(f"Неизвестный тип серии: {cfg.kind!r}")

    fig.update_layout(
        title=title,
        template="plotly_white",
        hovermode="x unified",
        hoverlabel=dict(
            bgcolor="white",
            bordercolor="rgba(0,0,0,0.08)",
            font=dict(size=13, color="#1f1f1f"),
            namelength=-1,
        ),
        legend=dict(orientation="h", yanchor="bottom", y=0.98, xanchor="left", x=0),
        margin=dict(l=40, r=20, t=50, b=40),
        plot_bgcolor="white",
        paper_bgcolor="white",
        bargap=0.55,
    )
    fig.update_xaxes(
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikedash="solid",
        spikecolor="rgba(0,0,0,0.25)",
        spikethickness=1,
        tickformat=date_format,
        showgrid=False,
    )
    fig.update_yaxes(showgrid=True, gridcolor="rgba(0,0,0,0.06)", zeroline=False)

    return fig


def _with_alpha(hex_color: str, alpha: float) -> str:
    """Конвертирует '#RRGGBB' в 'rgba(r,g,b,alpha)' для полупрозрачной заливки area."""
    hex_color = hex_color.lstrip("#")
    r, g, b = (int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"
