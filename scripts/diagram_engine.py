from __future__ import annotations

import html
import subprocess
import textwrap
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Theme:
    bg: str = "#F5F8FC"
    grid: str = "#DDE7F1"
    ink: str = "#18324D"
    muted: str = "#5F778E"
    line: str = "#86A1BA"
    panel: str = "#EEF4FA"
    white: str = "#FFFFFF"
    accent: str = "#1E7AF0"
    accent_soft: str = "#DAE9FF"
    green: str = "#35C58B"
    green_soft: str = "#DDF7EC"
    amber: str = "#F7B247"
    amber_soft: str = "#FFF0D4"
    red: str = "#F26F6F"
    red_soft: str = "#FFE2E2"


@dataclass
class SvgCanvas:
    width: int
    height: int
    theme: Theme = field(default_factory=Theme)
    parts: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.parts.extend(
            [
                f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" '
                f'viewBox="0 0 {self.width} {self.height}">',
                "<defs>",
                '<marker id="arrow-accent" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">',
                f'<path d="M0,0 L12,6 L0,12 z" fill="{self.theme.accent}" />',
                "</marker>",
                '<marker id="arrow-line" markerWidth="12" markerHeight="12" refX="10" refY="6" orient="auto">',
                f'<path d="M0,0 L12,6 L0,12 z" fill="{self.theme.line}" />',
                "</marker>",
                "</defs>",
                self.rect(0, 0, self.width, self.height, fill=self.theme.bg),
            ]
        )

    @staticmethod
    def esc(text: str) -> str:
        return html.escape(text, quote=True)

    def rect(self, x: float, y: float, w: float, h: float, **attrs: str) -> str:
        attr_str = " ".join(f'{key}="{value}"' for key, value in attrs.items())
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {attr_str} />'

    def line(self, x1: float, y1: float, x2: float, y2: float, **attrs: str) -> str:
        attr_str = " ".join(f'{key}="{value}"' for key, value in attrs.items())
        return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {attr_str} />'

    def circle(self, cx: float, cy: float, r: float, **attrs: str) -> str:
        attr_str = " ".join(f'{key}="{value}"' for key, value in attrs.items())
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" {attr_str} />'

    def polyline(self, points: list[tuple[float, float]], **attrs: str) -> str:
        point_str = " ".join(f"{x},{y}" for x, y in points)
        attr_str = " ".join(f'{key}="{value}"' for key, value in attrs.items())
        return f'<polyline points="{point_str}" {attr_str} />'

    def text(
        self,
        x: float,
        y: float,
        text: str,
        *,
        size: int = 24,
        fill: str | None = None,
        weight: int = 500,
        anchor: str = "start",
        width: int | None = None,
        line_height: float = 1.28,
    ) -> str:
        fill = fill or self.theme.ink
        lines = [text]
        if width:
            wrap_width = max(12, int(width / (size * 0.56)))
            lines = textwrap.wrap(text, width=wrap_width)
        parts = [
            (
                f'<text x="{x}" y="{y}" font-family="Aptos, Helvetica Neue, Arial, sans-serif" '
                f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">'
            )
        ]
        for index, entry in enumerate(lines):
            dy = 0 if index == 0 else size * line_height
            parts.append(f'<tspan x="{x}" dy="{dy}">{self.esc(entry)}</tspan>')
        parts.append("</text>")
        return "".join(parts)

    def add(self, *items: str) -> None:
        self.parts.extend(items)

    def add_grid(self, *, left: int = 80, top: int = 120, right: int = 80, bottom: int = 90, x_step: int = 140, y_step: int = 120) -> None:
        for x in range(left + 20, self.width - right, x_step):
            self.add(self.line(x, top, x, self.height - bottom, stroke=self.theme.grid, **{"stroke-width": "1"}))
        for y in range(top + 20, self.height - bottom, y_step):
            self.add(self.line(left, y, self.width - right, y, stroke=self.theme.grid, **{"stroke-width": "1"}))

    def add_stage_badge(self, number: int, x: float, y: float, label: str) -> None:
        self.add(
            self.circle(x, y, 18, fill=self.theme.white, stroke=self.theme.accent, **{"stroke-width": "2"}),
            self.text(x, y + 6, f"{number:02d}", size=13, fill=self.theme.accent, weight=700, anchor="middle"),
            self.text(x + 34, y + 6, label.upper(), size=13, fill=self.theme.muted, weight=700),
        )

    def add_card(self, x: float, y: float, w: float, h: float, *, accent_fill: str, title: str, subtitle: str, subtitle_width: int | None = None) -> None:
        self.add(
            self.rect(x + 10, y + 12, w, h, rx="34", fill="#DDE8F4", opacity="0.42"),
            self.rect(x, y, w, h, rx="34", fill=self.theme.white, stroke=self.theme.line, **{"stroke-width": "2"}),
            self.rect(x + 34, y + 24, w - 68, 18, rx="9", fill=accent_fill, opacity="0.18"),
            self.text(x + 34, y + 76, title, size=24, weight=720),
            self.text(x + 34, y + 110, subtitle, size=16, fill=self.theme.muted, width=subtitle_width or int(w - 72)),
        )

    def add_pill(self, x: float, y: float, w: float, h: float, *, fill: str, stroke: str, label: str, label_fill: str | None = None, label_size: int = 16) -> None:
        self.add(
            self.rect(x, y, w, h, rx=str(h / 2), fill=fill, stroke=stroke, **{"stroke-width": "1.5"}),
            self.text(x + w / 2, y + h / 2 + 6, label, size=label_size, fill=label_fill or stroke, weight=700, anchor="middle"),
        )

    def add_connector(self, points: list[tuple[float, float]], *, kind: str = "accent", width: int = 4, dashed: bool = False) -> None:
        stroke = self.theme.accent if kind == "accent" else self.theme.line
        marker = "url(#arrow-accent)" if kind == "accent" else "url(#arrow-line)"
        attrs: dict[str, str] = {
            "fill": "none",
            "stroke": stroke,
            "stroke-width": str(width),
            "marker-end": marker,
        }
        if dashed:
            attrs["stroke-dasharray"] = "10 10"
        self.add(self.polyline(points, **attrs))

    def add_ring_gauge(self, cx: float, cy: float, r: float, *, progress: float, label: str, accent: str) -> None:
        circumference = 2 * 3.14159 * r
        progress_len = circumference * progress
        remainder = max(1.0, circumference - progress_len)
        self.add(
            self.circle(cx, cy, r, fill="none", stroke="#DCE7F2", **{"stroke-width": "16"}),
            self.circle(
                cx,
                cy,
                r,
                fill="none",
                stroke=accent,
                **{
                    "stroke-width": "16",
                    "stroke-linecap": "round",
                    "stroke-dasharray": f"{progress_len:.2f} {remainder:.2f}",
                    "transform": f"rotate(-90 {cx} {cy})",
                },
            ),
            self.text(cx, cy + 10, label, size=28, weight=820, anchor="middle"),
        )

    def render(self) -> str:
        return "\n".join([*self.parts, "</svg>"])


def export_png(svg_path: Path, png_path: Path, width: int, height: int) -> None:
    subprocess.run(
        ["rsvg-convert", "-w", str(width), "-h", str(height), str(svg_path), "-o", str(png_path)],
        check=True,
    )
