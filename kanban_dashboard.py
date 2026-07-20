from pathlib import Path
import tentags

OUTPUT_DIR = Path(__file__).resolve().parent


def column_name(index):
    value = index + 1
    result = ""
    while value:
        value, remainder = divmod(value - 1, 26)
        result = chr(65 + remainder) + result
    return result


def span_style(width, opening, closing):
    return [opening] + [""] * (width - 2) + [closing]


def groups(*items):
    row = []
    for item in items:
        row.extend(item)
    return row


def centered_group_row(values, width):
    row = []
    for value in values:
        cells = [""] * width
        cells[(width - 1) // 2] = value
        row.extend(cells)
    return row


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


columns = [
    ("TODO", "#DBEAFE", "#1E40AF", [
        "Billing rules",
        "Onboarding copy",
        "Launch assets",
        "Analytics review",
    ]),
    ("DOING", "#FEF3C7", "#92400E", [
        "Payment API",
        "Dashboard UI",
        "Export load tests",
    ]),
    ("DONE", "#DCFCE7", "#166534", [
        "Data model",
        "Visual system",
        "PDF renderer",
        "XLSX links",
        "TenTags 2.1.14",
    ]),
]

style_rows = [
    span_style(
        12,
        "<cm><bg=#111827><color=white><center><b><fs=16>",
        "</fs></b></center></color></bg></cm>",
    ),
    groups(*[
        span_style(4, f"<cm><bg={bg}><color={fg}><center><b><fs=14>", "</fs></b></center></color></bg></cm>")
        for _, bg, fg, _ in columns
    ]),
]
title_row = [""] * 12
title_row[2] = "KANBAN"
title_row[5] = "DELIVERY"
title_row[9] = "BOARD"

data_rows = [
    title_row,
    centered_group_row([column[0] for column in columns], 4),
]

for index in range(5):
    row_style = []
    row_data = []
    for _, bg, fg, cards in columns:
        row_style.extend(span_style(
            4,
            f"<cm><bg={bg}><color={fg}><center><b>",
            "</b></center></color></bg></cm>",
        ))
        cells = [""] * 4
        if index < len(cards):
            cells[1] = cards[index]
        row_data.extend(cells)
    style_rows.append(row_style)
    data_rows.append(row_data)

style_rows.extend([
    groups(*[
        span_style(4, f"<cm><bg={fg}><color=white><center><b>", "</b></center></color></bg></cm>")
        for _, _, fg, _ in columns
    ]),
    span_style(
        12,
        "<cm><bg=#F8FAFC><color=#6B7280><center>",
        "</center></color></bg></cm>",
    ),
])
data_rows.extend([
    centered_group_row(["4 ITEMS", "3 ITEMS / WIP 4", "5 ITEMS"], 4),
    ["", "", "GENERATED", "", "", "WITH", "", "", "", "TENTAGS", "", ""],
])

model = compile_dashboard(
    style_rows,
    data_rows,
    cell_height=42,
    row_scales={1: 2, 2: 2, 8: 2},
)
print_outputs(export_dashboard("kanban_dashboard", model, orientation="landscape"))
