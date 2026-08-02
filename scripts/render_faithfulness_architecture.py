from __future__ import annotations

from pathlib import Path

from diagram_engine import SvgCanvas, Theme, export_png


WIDTH = 1800
HEIGHT = 1060
ASSET_DIR = Path("content/01-faithfulness/assets")
SVG_PATH = ASSET_DIR / "faithfulness-architecture-board.svg"
PNG_PATH = ASSET_DIR / "faithfulness-architecture-board.png"
THEME = Theme()


def draw_question(canvas: SvgCanvas, x: int, y: int) -> None:
    canvas.add_card(
        x,
        y,
        292,
        244,
        accent_fill=THEME.accent,
        title="User question",
        subtitle="A fluent answer is not enough. The system still has to prove support.",
    )
    canvas.add(
        canvas.rect(x + 42, y + 154, 206, 66, rx="26", fill=THEME.panel, stroke=THEME.line, **{"stroke-width": "1.5"}),
        canvas.text(x + 145, y + 194, "Which flat has a gym?", size=19, weight=720, anchor="middle"),
    )


def draw_retrieval(canvas: SvgCanvas, x: int, y: int) -> None:
    canvas.add_card(
        x,
        y,
        292,
        244,
        accent_fill=THEME.green,
        title="Retrieved context",
        subtitle="Listings and evidence snippets arrive before any judgment is made.",
    )
    doc_x = x + 98
    doc_y = y + 122
    for index, dx in enumerate((24, 12, 0)):
        canvas.add(
            canvas.rect(doc_x + dx, doc_y + index * 12, 84, 118, rx="18", fill=THEME.white, stroke=THEME.line, **{"stroke-width": "2"}),
            canvas.rect(doc_x + dx + 16, doc_y + index * 12 + 24, 52, 10, rx="5", fill=THEME.accent_soft),
            canvas.rect(doc_x + dx + 16, doc_y + index * 12 + 44, 44, 8, rx="4", fill="#E6EEF6"),
            canvas.rect(doc_x + dx + 16, doc_y + index * 12 + 60, 48, 8, rx="4", fill="#E6EEF6"),
            canvas.rect(doc_x + dx + 16, doc_y + index * 12 + 76, 36, 8, rx="4", fill="#E6EEF6"),
        )


def draw_answer_claims(canvas: SvgCanvas, x: int, y: int) -> None:
    canvas.add_card(
        x,
        y,
        374,
        300,
        accent_fill=THEME.amber,
        title="Answer becomes claims",
        subtitle="The answer is decomposed into smaller factual checks before scoring.",
    )
    answer_x = x + 34
    answer_y = y + 142
    canvas.add(
        canvas.rect(answer_x, answer_y, 196, 112, rx="22", fill=THEME.panel, stroke=THEME.line, **{"stroke-width": "1.6"}),
        canvas.text(answer_x + 18, answer_y + 34, "Generated answer", size=17, fill=THEME.muted, weight=700),
        canvas.text(answer_x + 18, answer_y + 66, "2 BHK, gym, near metro", size=18, weight=720),
        canvas.text(answer_x + 18, answer_y + 96, "sounds fluent, needs proof", size=16, fill=THEME.muted),
    )
    claims = [
        ("Claim A", "2 BHK", THEME.accent_soft),
        ("Claim B", "Gym", THEME.green_soft),
        ("Claim C", "Near metro", THEME.amber_soft),
    ]
    for index, (name, body, fill) in enumerate(claims):
        py = answer_y + 6 + index * 56
        canvas.add(
            canvas.rect(x + 246, py, 112, 40, rx="20", fill=fill, stroke=THEME.line, **{"stroke-width": "1.4"}),
            canvas.text(x + 262, py + 26, name, size=14, fill=THEME.muted, weight=700),
            canvas.text(x + 350, py + 26, body, size=15, weight=720, anchor="end"),
        )


def draw_verification(canvas: SvgCanvas, x: int, y: int) -> None:
    canvas.add_card(
        x,
        y,
        430,
        300,
        accent_fill=THEME.accent,
        title="Evidence verification",
        subtitle="Each claim is checked only against retrieved evidence.",
    )
    rows = [
        ("Claim A", "supported", THEME.green, THEME.green_soft),
        ("Claim B", "unsupported", THEME.red, THEME.red_soft),
        ("Claim C", "partial", THEME.amber, THEME.amber_soft),
    ]
    for index, (label, status, accent, soft) in enumerate(rows):
        ry = y + 126 + index * 74
        canvas.add(
            canvas.rect(x + 34, ry, 286, 54, rx="22", fill=THEME.white, stroke=THEME.line, **{"stroke-width": "1.5"}),
            canvas.rect(x + 50, ry + 12, 110, 30, rx="15", fill=THEME.panel),
            canvas.text(x + 104, ry + 33, label, size=16, weight=720, anchor="middle"),
            canvas.line(x + 178, ry + 27, x + 248, ry + 27, stroke=THEME.line, **{"stroke-width": "2"}),
        )
        canvas.add_pill(x + 286, ry + 9, 140, 36, fill=soft, stroke=accent, label=status, label_fill=accent)


def draw_audit(canvas: SvgCanvas, x: int, y: int) -> None:
    canvas.add(
        canvas.rect(x + 10, y + 12, 316, 222, rx="34", fill="#DDE8F4", opacity="0.42"),
        canvas.rect(x, y, 316, 222, rx="34", fill=THEME.white, stroke=THEME.line, **{"stroke-width": "2"}),
        canvas.text(x + 34, y + 56, "Judge audit", size=24, weight=720),
        canvas.text(x + 34, y + 90, "The score matters only if the judge holds up under repeat checks.", size=17, fill=THEME.muted, width=240),
    )
    items = [
        ("kappa", "judge vs human"),
        ("replicates", "stability check"),
        ("order bias", "pair audit"),
    ]
    for index, (title, tail) in enumerate(items):
        py = y + 118 + index * 36
        canvas.add(
            canvas.circle(x + 42, py, 6, fill=THEME.accent),
            canvas.text(x + 62, py + 5, title, size=16, weight=720),
            canvas.text(x + 152, py + 5, tail, size=15, fill=THEME.muted),
        )


def draw_score(canvas: SvgCanvas, x: int, y: int) -> None:
    canvas.add(
        canvas.rect(x + 10, y + 12, 316, 222, rx="34", fill="#DDE8F4", opacity="0.42"),
        canvas.rect(x, y, 316, 222, rx="34", fill=THEME.white, stroke=THEME.line, **{"stroke-width": "2"}),
        canvas.text(x + 34, y + 56, "Faithfulness score", size=24, weight=720),
    )
    canvas.add_ring_gauge(x + 102, y + 138, 48, progress=0.67, label="0.67", accent=THEME.green)
    canvas.add(
        canvas.text(x + 182, y + 126, "2 of 3 claims", size=20, weight=720),
        canvas.text(x + 182, y + 160, "supported by context", size=18, fill=THEME.muted),
    )
    canvas.add_pill(x + 184, y + 178, 98, 30, fill=THEME.green_soft, stroke=THEME.green, label="grounded", label_fill=THEME.green, label_size=14)


def build_svg() -> str:
    canvas = SvgCanvas(WIDTH, HEIGHT, THEME)
    canvas.add_grid(x_step=136, y_step=118)

    canvas.add(
        canvas.text(110, 102, "Faithfulness Evaluator Architecture", size=42, weight=820),
        canvas.text(110, 146, "Checks whether answer claims are supported by retrieved context.", size=21, fill=THEME.muted),
        canvas.rect(1238, 82, 382, 40, rx="20", fill=THEME.accent_soft, stroke=THEME.accent, **{"stroke-width": "1.5"}),
        canvas.text(1429, 108, "Grounding to retrieved context, not world truth", size=16, fill=THEME.accent, weight=700, anchor="middle"),
    )

    top_y = 258
    x1, x2, x3, x4 = 108, 446, 796, 1228
    draw_question(canvas, x1, top_y)
    draw_retrieval(canvas, x2, top_y)
    draw_answer_claims(canvas, x3, top_y)
    draw_verification(canvas, x4, top_y)

    canvas.add_stage_badge(1, x1 + 42, 228, "Question")
    canvas.add_stage_badge(2, x2 + 42, 228, "Retrieval")
    canvas.add_stage_badge(3, x3 + 42, 228, "Answer + claims")
    canvas.add_stage_badge(4, x4 + 42, 228, "Verification")

    canvas.add_connector([(x1 + 292, 380), (x2, 380)])
    canvas.add_connector([(x2 + 292, 380), (x3, 380)])
    canvas.add_connector([(x3 + 374, 410), (x4, 410)])

    lower_y = 648
    audit_x = 970
    score_x = 1322
    draw_audit(canvas, audit_x, lower_y)
    draw_score(canvas, score_x, lower_y)

    canvas.add_stage_badge(6, audit_x + 116, 608, "Judge audit")
    canvas.add_stage_badge(5, score_x + 118, 608, "Score")

    split_x = x4 + 184
    split_y = top_y + 300
    canvas.add_connector([(split_x, split_y), (split_x, 594), (score_x + 110, 594), (score_x + 110, lower_y)], kind="accent")
    canvas.add_connector([(split_x - 148, split_y), (split_x - 148, 586), (audit_x + 110, 586), (audit_x + 110, lower_y)], kind="line", width=3, dashed=True)
    canvas.add(canvas.text(1158, 580, "audit the judge before trusting the metric", size=16, fill=THEME.muted, anchor="middle"))

    canvas.add(
        canvas.rect(108, 904, 610, 88, rx="24", fill=THEME.white, stroke=THEME.line, **{"stroke-width": "1.5"}),
        canvas.text(142, 944, "Production reading", size=18, fill=THEME.muted, weight=700),
        canvas.text(142, 974, "This measures support from retrieved evidence. It does not certify global truth.", size=22, weight=760),
        canvas.rect(1338, 936, 334, 42, rx="21", fill=THEME.white, stroke=THEME.line, **{"stroke-width": "1.5"}),
        canvas.text(1505, 963, "saran.build / paper-to-production", size=16, fill=THEME.muted, weight=700, anchor="middle"),
    )

    return canvas.render()


def main() -> None:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    SVG_PATH.write_text(build_svg(), encoding="utf-8")
    export_png(SVG_PATH, PNG_PATH, WIDTH, HEIGHT)
    print(f"Wrote {SVG_PATH}")
    print(f"Wrote {PNG_PATH}")


if __name__ == "__main__":
    main()
