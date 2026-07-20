from pathlib import Path
import calendar
import datetime
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


# Get current date info
today = datetime.date.today()
year = today.year
month = today.month

month_name = today.strftime("%B").upper()
title_text = f"{month_name} {year}"

weekdays = ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]

# Dynamically generate weeks for the current month
cal = calendar.Calendar(firstweekday=0)
month_weeks = cal.monthdayscalendar(year, month)

weeks = []
for w in month_weeks:
    weeks.append([str(d) if d != 0 else "" for d in w])

style_rows = [
    span_style(
        7,
        "<cm><bg=#1E3A8A><color=white><center><b><fs=20>",
        "</fs></b></center></color></bg></cm>",
    ),
    ["<bg=#DBEAFE><color=#1E3A8A><center><b></b></center></color></bg>"] * 7,
]
data_rows = [
    ["", "", "", title_text, "", "", ""],
    weekdays,
]

for week in weeks:
    row_styles = []
    for col, day in enumerate(week):
        if day == str(today.day):
            row_styles.append("<bg=#2563EB><color=white><center><b></b></center></color></bg>")
        elif col >= 5 and day:
            row_styles.append("<bg=#EFF6FF><color=#1D4ED8><center></center></color></bg>")
        elif day:
            row_styles.append("<bg=white><color=#111827><center></center></color></bg>")
        else:
            row_styles.append("<bg=#F8FAFC></bg>")
    style_rows.append(row_styles)
    data_rows.append(week)

style_rows.append(span_style(
    7,
    "<cm><bg=#F3F4F6><color=#4B5563><center><b>",
    "</b></center></color></bg></cm>",
))

today_weekday = today.strftime("%A")
today_month_name = today.strftime("%B")
footer_text = f"Today: {today_weekday}, {today.day} {today_month_name} {year}"
data_rows.append(["", "", "", footer_text, "", "", ""])

footer_row_1based = 3 + len(weeks)

model = compile_dashboard(
    style_rows,
    data_rows,
    cell_height=38,
    row_scales={1: 2, footer_row_1based: 2},
)

export_name = f"calendar_{today.strftime('%B').lower()}_{today.day}_{year}"
print_outputs(export_dashboard(export_name, model, orientation="landscape"))
