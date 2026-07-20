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


weeks = 13
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
levels = [
    [0, 1, 3, 0, 2, 4, 3, 1, 0, 2, 4, 4, 1],
    [1, 0, 2, 4, 3, 3, 1, 0, 2, 3, 4, 2, 0],
    [3, 4, 4, 2, 1, 0, 1, 3, 4, 2, 0, 1, 2],
    [2, 3, 4, 4, 2, 1, 0, 2, 3, 4, 3, 1, 0],
    [0, 1, 2, 4, 4, 3, 2, 1, 3, 4, 4, 3, 2],
    [0, 0, 1, 2, 4, 3, 2, 0, 1, 3, 4, 2, 1],
    [0, 1, 2, 3, 4, 2, 1, 0, 2, 4, 3, 2, 0],
]
colors = ["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"]

style_rows = [
    span_style(
        14,
        "<cm><bg=#0D1117><color=white><center><b><fs=16>",
        "</fs></b></center></color></bg></cm>",
    ),
    ["<bg=#F6F8FA><b></b></bg>"] + ["<bg=#F6F8FA></bg>"] * weeks,
]
data_rows = [
    ["", "", "", "", "GITHUB", "", "", "", "ACTIVITY", "", "", "", "", ""],
    ["Day", "Apr", "", "", "May", "", "", "", "Jun", "", "", "", "Jul", ""],
]

for day, day_levels in zip(days, levels):
    style_rows.append(
        ["<bg=#F6F8FA><b></b></bg>"]
        + [f"<bg={colors[level]}></bg>" for level in day_levels]
    )
    data_rows.append([day] + [""] * weeks)

style_rows.append(
    ["<bg=#F6F8FA><center><b><fs=9></fs></b></center></bg>"] * 9
    + [f"<bg={color}></bg>" for color in colors[:-1]]
    + ["<bg=#216E39><color=white><center><b><fs=9></fs></b></center></color></bg>"]
)
data_rows.append([
    "", "", "487 TOTAL", "", "", "13 WEEKS", "", "", "LESS",
    "", "", "", "", "MORE",
])

model = compile_dashboard(
    style_rows,
    data_rows,
    cell_height=24,
    row_scales={1: 2, 10: 2},
    col_scales={1: 2},
    border_color="#FFFFFF",
)
print_outputs(export_dashboard("contribution_graph", model, orientation="landscape"))
