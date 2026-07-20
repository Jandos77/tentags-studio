from pathlib import Path

import tentags


OUTPUT_DIR = Path(__file__).resolve().parent
LOGO_PATH = "D:/TenTags/tentags_logo.png"


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
