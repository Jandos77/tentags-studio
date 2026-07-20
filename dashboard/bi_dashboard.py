from datetime import date
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


COLS = 12


def card_style(color, size):
    return span_style(
        3,
        f"<cm><bg={color}><color=white><center><b><fs={size}>",
        "</fs></b></center></color></bg></cm>",
    )


style_rows = [
    span_style(
        12,
        "<cm><bg=#111827><color=white><center><b><fs=20>",
        "</fs></b></center></color></bg></cm>",
    ),
    groups(
        card_style("#2563EB", 12),
        card_style("#059669", 12),
        card_style("#D97706", 12),
        card_style("#DC2626", 12),
    ),
    groups(
        card_style("#3B82F6", 22),
        card_style("#10B981", 22),
        card_style("#F59E0B", 22),
        card_style("#EF4444", 22),
    ),
    groups(
        card_style("#60A5FA", 9),
        card_style("#34D399", 9),
        card_style("#FBBF24", 9),
        card_style("#F87171", 9),
    ),
    span_style(
        12,
        "<cm><bg=#E5E7EB><color=#111827><center><b><fs=15>",
        "</fs></b></center></color></bg></cm>",
    ),
]

revenue = [3, 4, 4, 5, 5, 4]
expenses = [2, 3, 3, 3, 4, 3]
revenue_shades = {
    5: "#93C5FD",
    4: "#60A5FA",
    3: "#3B82F6",
    2: "#2563EB",
    1: "#1D4ED8",
}
expense_shades = {
    5: "#D1D5DB",
    4: "#9CA3AF",
    3: "#6B7280",
    2: "#4B5563",
    1: "#374151",
}
for level in range(4, 0, -1):
    chart_row = []
    for revenue_height, expense_height in zip(revenue, expenses):
        revenue_color = revenue_shades[level] if revenue_height >= level else "white"
        expense_color = expense_shades[level] if expense_height >= level else "white"
        chart_row.extend([
            f"<bg={revenue_color}></bg>",
            f"<bg={expense_color}></bg>",
        ])
    style_rows.append(chart_row)

style_rows.extend([
    groups(*[
        span_style(2, "<cm><bg=#F8FAFC><center><b>", "</b></center></bg></cm>")
        for _ in range(6)
    ]),
    groups(
        span_style(6, "<cm><bg=#DBEAFE><color=#1D4ED8><center><b>", "</b></center></color></bg></cm>"),
        span_style(6, "<cm><bg=#E5E7EB><color=#374151><center><b>", "</b></center></color></bg></cm>"),
    ),
    groups(
        span_style(6, "<cm><bg=#ECFDF5><color=#065F46><center><b><fs=13>", "</fs></b></center></color></bg></cm>"),
        span_style(6, "<cm><bg=#EFF6FF><color=#1E40AF><center><b><fs=13>", "</fs></b></center></color></bg></cm>"),
    ),
])

heatmap = [
    [0, 1, 3, 2, 4],
    [1, 2, 4, 3, 2],
    [3, 4, 2, 1, 0],
    [2, 3, 4, 4, 3],
    [0, 1, 2, 3, 4],
]
heat_colors = ["#EBEDF0", "#9BE9A8", "#40C463", "#30A14E", "#216E39"]
progress = [
    ("Alpha", 2, "75%", "#2563EB"),
    ("Migration", 3, "92%", "#10B981"),
    ("API", 1, "48%", "#F59E0B"),
    ("Uptime", 3, "100%", "#22C55E"),
    ("QA", 2, "81%", "#8B5CF6"),
]
for levels, (_, filled, _, color) in zip(heatmap, progress):
    style_rows.append(
        ["<bg=#F3F4F6><b></b></bg>"]
        + [f"<bg={heat_colors[level]}></bg>" for level in levels]
        + ["<bg=#F8FAFC><b></b></bg>"]
        + [f"<bg={color}></bg>" if index < filled else "<bg=#E5E7EB></bg>" for index in range(4)]
        + ["<bg=#F8FAFC><b></b></bg>"]
    )

style_rows.extend([
    groups(
        span_style(6, "<cm><bg=#F8FAFC><center><b>", "</b></center></bg></cm>"),
        span_style(6, "<cm><bg=#F8FAFC><center><b>", "</b></center></bg></cm>"),
    ),
    span_style(
        12,
        "<cm><bg=#FEF3C7><color=#92400E><center><b>",
        "</b></center></color></bg></cm>",
    ),
    span_style(
        12,
        "<cm><bg=#111827><color=#D1D5DB><center><fs=9>",
        "</fs></center></color></bg></cm>",
    ),
])

data_rows = [
    [f"<img src={LOGO_PATH} w=48 h=auto m=3>", "", "", "", "", "TEN TAGS BI DASHBOARD", "", "", "", "", "", ""],
    centered_group_row(["REVENUE", "ORDERS", "ACTIVE USERS", "NET PROFIT"], 3),
    centered_group_row(["$128K", "842", "5.4K", "$47K"], 3),
    centered_group_row(["+18.2% vs last month", "+9.4% conversion", "+624 this month", "36.8% margin"], 3),
    ["", "", "", "", "", "MONTHLY PERFORMANCE", "", "", "", "", "", ""],
    *[[""] * COLS for _ in range(4)],
    centered_group_row(["Jan", "Feb", "Mar", "Apr", "May", "Jun"], 2),
    centered_group_row(["Revenue", "Expenses"], 6),
    centered_group_row(["ACTIVITY HEATMAP", "DELIVERY PROGRESS"], 6),
]

for day, item in zip(["Mon", "Tue", "Wed", "Thu", "Fri"], progress):
    percent = item[2]
    data_rows.append([day, "", "", "", "", "", item[0], "", "", "", "", percent])

data_rows.extend([
    centered_group_row(["Less  -  More", "4-step progress"], 6),
    ["", "", "", "BEST: MAY", "", "", "", "", "MARGIN: 37%", "", "", ""],
    ["", "", "", f"GENERATED {date.today().isoformat()}", "", "", "", "", "TENTAGS 2.1.14", "", "", ""],
])

model = compile_dashboard(
    style_rows,
    data_rows,
    cell_height=17,
    row_scales={1: 3, 2: 2, 3: 2, 4: 2, 5: 2, 12: 2},
)
print_outputs(export_dashboard(
    "bi_dashboard",
    model,
    margins=(8, 8, 8, 8),
    page_size="A3",
))
