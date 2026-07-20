from pathlib import Path
import tentags

OUTPUT_DIR = Path(__file__).resolve().parent / "export_files"


def column_name(index):
    value = index + 1
    result = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(65 + remainder) + result
    return result


def span_style(width, opening, closing):
    return [opening] + [""] * (width - 2) + [closing]


def compile_dashboard(
    style_rows,
    data_rows,
    *,
    cell_height=20,
    row_scales=None,
    col_scales=None,
    border_color="#D6DCE5",
):
    rows = len(data_rows)
    cols = len(data_rows[0]) if data_rows else 0
    if rows == 0 or cols == 0:
        raise ValueError("Dashboard must contain at least one cell.")
    if len(style_rows) != rows:
        raise ValueError("Style and data row counts must match.")
    if any(len(row) != cols for row in style_rows + data_rows):
        raise ValueError("Every style and data row must match the dashboard width.")

    row_scales = dict(row_scales or {})
    col_scales = dict(col_scales or {})
    scale_entries = []
    for col in range(cols):
        vertical = row_scales.get(1, 1) if col == 0 else 1
        horizontal = col_scales.get(col + 1, 1)
        scale_entries.append(f"{column_name(col)}1={vertical},{horizontal}")
    for row, vertical in sorted(row_scales.items()):
        if row != 1:
            scale_entries.append(f"A{row}={vertical},1")

    preamble = (
        f'{rows},{cols},1,"{border_color}","solid-1",0,{cell_height},'
        f'scale({";".join(scale_entries)})'
    )
    style = tentags.serialize.style(
        style_rows,
        expected_rows=rows,
        expected_cols=cols,
    )
    data = tentags.serialize.data(
        data_rows,
        expected_rows=rows,
        expected_cols=cols,
    )
    return tentags.compile(preamble, style, data)


def export_dashboard(
    name,
    model,
    *,
    orientation="landscape",
    margins=(20, 20, 20, 20),
    page_size="A4",
):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    html_path = OUTPUT_DIR / f"{name}.html"
    xlsx_path = OUTPUT_DIR / f"{name}.xlsx"
    pdf_path = OUTPUT_DIR / f"{name}.pdf"

    html_path.write_text(tentags.render_html(model), encoding="utf-8")
    tentags.render_xlsx(model, xlsx_path)
    tentags.render_pdf(
        model,
        str(pdf_path),
        settings={
            "page_size": page_size,
            "orientation": orientation,
            "margins": margins,
        },
    )
    return html_path, xlsx_path, pdf_path


def print_outputs(paths):
    for path in paths:
        print(f"Created: {path}")


weeks = [f"W{number}" for number in range(1, 13)]
tasks = [
    ("Research", 1, 3, "Done", "#2563EB"),
    ("UX Design", 2, 5, "Done", "#8B5CF6"),
    ("API Build", 4, 9, "Active", "#10B981"),
    ("Web Client", 5, 10, "Active", "#F59E0B"),
    ("QA & Security", 8, 11, "Planned", "#EF4444"),
    ("Launch", 11, 12, "Planned", "#06B6D4"),
]

style_rows = [
    span_style(
        14,
        "<cm><bg=#111827><color=white><center><b><fs=16>",
        "</fs></b></center></color></bg></cm>",
    ),
    ["<bg=#E5E7EB><b></b></bg>"]
    + ["<bg=#E5E7EB><center><b></b></center></bg>"] * 12
    + ["<bg=#E5E7EB><b></b></bg>"],
]
title_row = [""] * 14
title_row[4] = "PRODUCT"
title_row[7] = "DELIVERY"
title_row[10] = "GANTT"

data_rows = [
    title_row,
    ["Task"] + weeks + ["Status"],
]

for task, start, end, status, color in tasks:
    style_rows.append(
        ["<bg=#F8FAFC><left><b></b></left></bg>"]
        + [f"<bg={color}></bg>" if start <= week <= end else "<bg=white></bg>" for week in range(1, 13)]
        + [f"<bg={color}><color=white><center><b></b></center></color></bg>"]
    )
    data_rows.append([task] + [""] * 12 + [status])

style_rows.extend([
    span_style(
        14,
        "<cm><bg=#DBEAFE><color=#1E40AF><center><b>",
        "</b></center></color></bg></cm>",
    ),
    span_style(
        14,
        "<cm><bg=#F8FAFC><color=#6B7280><center>",
        "</center></color></bg></cm>",
    ),
])
checkpoint_row = [""] * 14
checkpoint_row[4] = "CURRENT"
checkpoint_row[8] = "WEEK 7"
footer_row = [""] * 14
footer_row[0] = "6 TASKS"
footer_row[6] = "12"
footer_row[8] = "WEEKS"
footer_row[13] = "ROADMAP"
data_rows.extend([checkpoint_row, footer_row])

model = compile_dashboard(
    style_rows,
    data_rows,
    cell_height=28,
    row_scales={1: 2, 9: 2},
    col_scales={1: 4, 14: 2},
)
print_outputs(export_dashboard("gantt_dashboard", model, orientation="landscape"))
