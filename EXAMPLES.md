# TenTags — Examples & Reference Guide

A complete guide to TenTags: all tags, template engine integrations, and passing arguments from backend to templates.

---

## Table of Contents

1. [Formula Structure](#1-formula-structure)
2. [Tag Reference](#2-tag-reference)
3. [Python API](#3-python-api)
4. [Django — Template Tags](#4-django--template-tags)
5. [Flask — Jinja2](#5-flask--jinja2)
6. [FastAPI — Jinja2](#6-fastapi--jinja2)
7. [Decoupled API: preamble + style + data](#7-decoupled-api-preamble--style--data)
8. [Real-World Examples](#8-real-world-examples)

---

## 1. Formula Structure

Every TenTags formula has three parts:

```
ROWS, COLS, BORDER_WIDTH, "BORDER_COLOR", "BORDER_STYLE", STRETCH, CELL_HEIGHT [, scale(...)], data(...)
```

| Parameter | Type | Description |
|---|---|---|
| `ROWS` | int | Number of rows |
| `COLS` | int | Number of columns |
| `BORDER_WIDTH` | int | Border thickness (px) |
| `BORDER_COLOR` | string | Border color (`"black"`, `"#ccc"`) |
| `BORDER_STYLE` | string | Border style (`"solid"`, `"solid-1"`, `"solid-0"`) |
| `STRETCH` | int | `0` = fixed height, `1` = auto-stretch |
| `CELL_HEIGHT` | int | Cell height in px |
| `scale(...)` | extension | Optional relative row and column scale for this table |
| `data(...)` | block | Cell contents |

**Separators inside `data()`:**
- `,` — next cell (next column)
- `;` — next row

```python
import tentags

html = tentags.render('2, 3, 1, "black", "solid", 0, 40, data(A, B, C; D, E, F)')
```

### Relative row and column scale

`scale(...)` is an optional part of the preamble. It changes logical grid proportions without introducing renderer-specific pixels, Excel objects, or PDF coordinates.

```python
from pathlib import Path
import tentags

output_dir = Path("demo_output")
output_dir.mkdir(exist_ok=True)

preamble = (
    '5,4,1,"#64748b","solid-1",0,28,'
    'scale(A1=2,3;C5=2,2;D3=3,5)'
)

style = """style(
<center><bg=blue><color=white><b>, , , </b></color></bg>;
<bg=white>, , , </bg>;
<bg=#f8fafc>, , , </bg>;
<bg=white>, , , </bg>;
<bg=yellow>, , , </bg></center>
)"""

data = """data(
Column A x3, Column B x1, Column C x2, Column D x5;
Row 2 x1, Standard, Standard, Standard;
Row 3 x3, Tall, Tall, Tall;
Row 4 x1, Standard, Standard, Standard;
Row 5 x2, Medium, Medium, Medium
)"""

model = tentags.compile(preamble, style, data)

(output_dir / "scale_demo.html").write_text(
    tentags.render_html(model),
    encoding="utf-8",
)
tentags.render_xlsx(model, output_dir / "scale_demo.xlsx")
tentags.render_pdf(model, output_dir / "scale_demo.pdf")
```

In this example:

- `A1=2,3` makes row 1 twice as high and column A three times as wide as their standard sizes.
- `C5=2,2` makes row 5 twice as high and column C twice as wide.
- `D3=3,5` makes row 3 three times as high and column D five times as wide.
- The address identifies a complete row and column; it does not assign a private size to one cell.

Rules:

- Vertical and horizontal values must be integers from `1` to `5`.
- `1` means the standard size.
- Repeated rows and columns use the maximum value for their own axis.
- The address must be a local A1 cell inside the current table.
- Ranges, marks, and `Table!List!A1` addresses are invalid inside `scale(...)`.
- A vertical value greater than `1` requires `CELL_HEIGHT` greater than `0`.
- Each MultiTable item may use its own `scale(...)` in its own preamble.

The Serializer API produces the same canonical DSL without creating a second compiler path:

```python
preamble = tentags.serialize.preamble(
    5,
    4,
    border_color="#64748b",
    border_style="solid-1",
    cell_height=28,
    scale={
        "A1": (2, 3),
        "C5": (2, 2),
        "D3": (3, 5),
    },
)

model = tentags.compile(preamble, style, data)
```

For MultiTable, put `scale(...)` in each table item's own preamble. Different tables can therefore use different row and column proportions:

```python
tables = [
    {
        "document": "Report",
        "table_name": "Summary",
        "sheet_name": "Summary",
        "preamble": '2,3,1,"black","solid-1",0,28,scale(A1=2,3)',
        "style": "style(<bg=blue><color=white><b>, , </b></color></bg>; , , )",
        "data": "data(Name,Value,Status;Revenue,125000,Closed)",
    },
    {
        "document": "Report",
        "table_name": "Details",
        "sheet_name": "Details",
        "preamble": '3,2,1,"black","solid-1",0,24,scale(B1=1,4;A3=2,1)',
        "style": "style(,; ,; ,)",
        "data": "data(Item,Description;A,Standard;B,Extended details)",
    },
]
```

---

## 2. Tag Reference

Tags are applied **inside cells** within `style()` or `data()` blocks.
All tags must be **closed**: `<tag>content</tag>`.

### Typography

| Tag | Effect | CSS |
|---|---|---|
| `<b>text</b>` | **Bold** | `font-weight: bold` |
| `<i>text</i>` | *Italic* | `font-style: italic` |
| `<u>text</u>` | Underline | `text-decoration: underline` |
| `<s>text</s>` | Strikethrough | `text-decoration: line-through` |
| `<fs=18>text</fs>` | Font size 18px | `font-size: 18px` |

```python
# Bold + italic
tentags.render('1,1,1,"black","solid",0,40, data(<b><i>Important!</i></b>)')

# Underline
tentags.render('1,1,1,"black","solid",0,40, data(<u>Terms and Conditions</u>)')

# Strikethrough old price + new price
tentags.render('1,2,1,"black","solid",0,40, data(<s>"$199"</s>, "$99"))')

# Large font
tentags.render('1,1,1,"black","solid",0,60, data(<fs=24><b>TOTAL</b></fs>)')

# Combine all
tentags.render('1,1,1,"black","solid",0,40, data(<b><u><s>Bold + underlined + struck</s></u></b>)')
```

---

### Color & Background

| Tag | Description |
|---|---|
| `<color=red>text</color>` | Text color (name or hex) |
| `<bg=#f0f0f0>text</bg>` | Cell background color |

```python
# Named colors
tentags.render('1,3,1,"black","solid",0,40, data(<color=red>Loss</color>, <color=green>Profit</color>, <color=blue>Neutral</color>)')

# Hex colors
tentags.render('1,2,1,"#ccc","solid",0,40, data(<bg=#1e293b><color=white>Header</color></bg>, <bg=#f8fafc>Data</bg>)')

# Colored badge
tentags.render('1,1,1,"black","solid",0,50, data(<bg=#dcfce7><color=#166534><b>+$60,000</b></color></bg>)')
```

---

### Alignment

| Tag | Description |
|---|---|
| `<left>text</left>` | Align left |
| `<center>text</center>` | Align center |
| `<right>text</right>` | Align right |

```python
tentags.render('1,3,1,"black","solid",0,40, data(<left>Left</left>, <center>Center</center>, <right>Right</right>)')
```

---

### Cell Merging

| Tag | Description |
|---|---|
| `<cm>text, , </cm>` | Joins N columns (one `,` per extra cell). HTML hides internal borders; Excel and PDF create native merged regions. |
| `<rm>text</rm>` | Joins cells vertically. Mark each participating cell with `<rm>`. |

```python
# Merge 3 columns
tentags.render('2,3,1,"black","solid",0,40, data(<cm>Header across 3 columns, , </cm>; A, B, C)')

# Merge 2 rows
tentags.render('2,2,1,"black","solid",0,40, data(<rm>Merged cell</rm>, Right 1; <rm> </rm>, Right 2)')
```

---

### Links

| Tag | Description |
|---|---|
| `<url=https://...>text</url>` | Clickable hyperlink |

> **Best practice:** Write `<url>` inside `data()`, not `style()`.
> This keeps your style template reusable across different links.

```python
# Simple link
tentags.render('1,1,1,"black","solid",0,40, data(<url=https://example.com>Visit Site</url>)')

# Bold link
tentags.render('1,1,1,"black","solid",0,40, data(<url=https://example.com><b>Download PDF</b></url>)')

# Decoupled: URL in data(), formatting in style()
tentags.render(
    '1,1,1,"black","solid",0,40',
    'style(<b><left></left></b>)',
    'data(<url=https://example.com>Visit Site</url>)'
)
```

**Rendering per target:**
- **HTML** — `<a href="...">text</a>` inside the `<td>`
- **Excel (XLSX)** — native hyperlink + blue underline font
- **PDF** — clickable `<link href="...">` via ReportLab

---

### Images

`<img>` is a single TenTags element with compact `key=value` attributes.

| Tag | Description |
|---|---|
| `<img src=logo.png w=120 h=auto m=15>` | Image with local source, automatic height, and 15px margin |
| `<img src=https://example.com/image.png w=300 h=auto>` | Image with remote source |

Size rules:
- `w` and `h` are pixels by default.
- `h=auto` preserves proportions.
- `m` is margin in pixels on all four sides.
- If the sixth preamble argument (`stretch`) is `1`, image cells can expand with the rendered image size.
- If `stretch` is `0`, image height is forced to the seventh preamble argument (`cell_height`) and width becomes `auto`.
- In `stretch=1` mode, if only `w` is provided, height is automatic.
- In `stretch=1` mode, if only `h` is provided, width is automatic.
- In `stretch=1` mode, if both are numbers, the image is rendered at exactly that size.

```python
tentags.render('1,1,1,"black","solid",1,80, data(<img src=logo.png w=120 h=auto m=15>)')

tentags.render('1,1,1,"black","solid",1,80, data(<img src=https://pycells.com/assets/img/PyCells_mds.png w=120 h=auto>)')

tentags.render('1,2,1,"black","solid",0,80, data(<img src=photo.jpg w=200 h=150>, <img src=qrcode.png w=80 h=80>)')
```

**Rendering per target:**
- **HTML** — native `<img>` inside the `<td>`.
- **Excel (XLSX)** — local files are embedded when supported by `openpyxl`; remote URLs fall back to a linked `src`.
- **PDF** — falls back to the image `src` text.

---

### CSV Import

```python
# From a local file
tentags.render('5,3,1,"black","solid",0,40, data(csv("data/sales.csv")))')

# From a URL
tentags.render('5,3,1,"black","solid",0,40, data(csv("https://example.com/data.csv")))')
```

---

## 3. Python API

### Simple Rendering

```python
import tentags

# Full formula in one string
html = tentags.render('2,2,1,"black","solid",0,40, data(A, B; C, D)')

# With context variables
context = {'name': 'Alice', 'role': 'Admin'}
html = tentags.render('1,2,1,"black","solid",0,40, data(name, role)', context)
```

### Compile once, render to multiple formats

```python
import tentags

model = tentags.parse('2,2,1,"black","solid",0,40, data(A, B; C, D)')

html = tentags.render_html(model)           # HTML string
tentags.render_xlsx(model, 'out.xlsx')      # Excel file
tentags.render_pdf(model,  'out.pdf')       # PDF file
```

### Decoupled API

```python
import tentags

preamble = '3, 3, 1, "#ccc", "solid", 0, 40'
style    = '''style(
    <bg=#1e293b><color=white><b><cm> , , </cm></b></color></bg>;
    <bg=#f1f5f9><b><left></left></b></bg>, <bg=#f1f5f9><b><center></center></b></bg>, <bg=#f1f5f9><b><right></right></b></bg>;
    <left></left>, <center></center>, <right></right>
)'''
data     = 'data(Department Report, , ; Department, Employees, Budget; Engineering, 12, "$500,000")'

html  = tentags.render(preamble, style, data)

# Same style template, different data
html2 = tentags.render(preamble, style, 'data(Department Report, , ; Department, Employees, Budget; Marketing, 8, "$200,000")')
```

### Serializer API

The Serializer API converts Python structures into TenTags DSL strings. It is not a second compiler and not a mutable object API. The canonical namespace is `tentags.serialize`; top-level `dumps_*` functions remain available as convenience aliases. The canonical path stays:

```text
Python structures -> tentags.serialize.* -> TenTags DSL -> compile() -> IR -> HTML/PDF/XLSX
```

```python
import tentags

records = [
    {"period": "January", "revenue": 125000, "status": "Closed"},
    {"period": "July", "revenue": 158900, "status": "Review"},
]

STATUS_COLORS = {
    "Closed": {"bg": "#dcfce7", "fg": "#166534"},
    "Review": {"bg": "#fef3c7", "fg": "#92400e"},
}

data_rows = [
    ["<color=#ffffff><b>Period</b></color>", "<right><color=#ffffff><b>Revenue</b></color></right>", "<center><color=#ffffff><b>Status</b></color></center>"],
]
style_rows = [
    ["<bg=#0f172a><b></b></bg>"] * 3,
]

for index, record in enumerate(records):
    base_bg = "#ffffff" if index % 2 == 0 else "#f8fafc"
    status = STATUS_COLORS[record["status"]]
    style_rows.append([
        f"<bg={base_bg}></bg>",
        f"<bg={base_bg}></bg>",
        f"<bg={status['bg']}></bg>",
    ])
    data_rows.append([
        record["period"],
        f"<right>{record['revenue']}</right>",
        f"<center><color={status['fg']}>{record['status']}</color></center>",
    ])

preamble = tentags.serialize.preamble(len(data_rows), 3, border_color="#64748b", border_style="solid-1", cell_height=28)
style = tentags.serialize.style(style_rows, expected_rows=len(data_rows), expected_cols=3)
data = tentags.serialize.data(data_rows, expected_rows=len(data_rows), expected_cols=3)

model = tentags.compile(preamble, style, data)
html = tentags.render_html(model)
tentags.render_pdf(model, "serializer_report.pdf")
tentags.render_xlsx(model, "serializer_report.xlsx")
```

The same serializer output can be used inside `multitable_*` items:

```python
dashboard_rows = [
    ["Section", "Target"],
    ["Invoice", "<url=goto:Invoice!Items!A1>Open</url>"],
]

invoice_rows = [
    ["Item", "Total"],
    ["Paper", "<url=goto:Dashboard!Menu!A1>$25</url>"],
]

tables = [
    {
        "document": "Dashboard",
        "table_name": "Menu",
        "sheet_name": "Menu",
        "title": "Dashboard Menu",
        "preamble": tentags.serialize.preamble(len(dashboard_rows), 2, border_color="#64748b", border_style="solid-1", cell_height=24),
        "style": tentags.serialize.style([["<bg=#dbeafe><b></b></bg>"] * 2, ["<bg=#ffffff></bg>"] * 2]),
        "data": tentags.serialize.data(dashboard_rows),
    },
    {
        "document": "Invoice",
        "table_name": "Items",
        "sheet_name": "Items",
        "title": "Invoice Items",
        "preamble": tentags.serialize.preamble(len(invoice_rows), 2, border_color="#64748b", border_style="solid-1", cell_height=24),
        "style": tentags.serialize.style([["<bg=#ffedd5><b></b></bg>"] * 2, ["<bg=#ffffff></bg>"] * 2]),
        "data": tentags.serialize.data(invoice_rows),
    },
]

html = tentags.multitable_html(tables, settings={
    "table_order": ["Dashboard!Menu", "Invoice!Items"],
    "tables_per_row": 2,
    "layout": "grid",
    "cols": 2,
})
```

### SQLite database serialization

This pattern reads records from a database, builds Python matrices, serializes them to TenTags DSL, and still compiles through the normal `compile(preamble, style, data)` entry point.

```python
import sqlite3
import tentags

conn = sqlite3.connect("demo_output/finance.db")
conn.row_factory = sqlite3.Row
records = [
    dict(row)
    for row in conn.execute(
        "SELECT period, revenue, expenses, profit, status FROM monthly_report ORDER BY period"
    )
]
conn.close()

STATUS_COLORS = {
    "Closed": {"bg": "#dcfce7", "fg": "#166534"},
    "Review": {"bg": "#fef3c7", "fg": "#92400e"},
    "Forecast": {"bg": "#dbeafe", "fg": "#1e3a8a"},
}

data_rows = [[
    "<color=#ffffff><b>Period</b></color>",
    "<right><color=#ffffff><b>Revenue</b></color></right>",
    "<right><color=#ffffff><b>Expenses</b></color></right>",
    "<right><color=#ffffff><b>Profit</b></color></right>",
    "<center><color=#ffffff><b>Status</b></color></center>",
]]
style_rows = [["<bg=#0f172a><b></b></bg>"] * 5]

for index, record in enumerate(records):
    base_bg = "#ffffff" if index % 2 == 0 else "#f8fafc"
    status = STATUS_COLORS[record["status"]]
    style_rows.append([
        f"<bg={base_bg}></bg>",
        f"<bg={base_bg}></bg>",
        f"<bg={base_bg}></bg>",
        f"<bg={base_bg}></bg>",
        f"<bg={status['bg']}></bg>",
    ])
    data_rows.append([
        record["period"],
        f"<right>{record['revenue']}</right>",
        f"<right>{record['expenses']}</right>",
        f"<right><color=#16a34a><b>{record['profit']}</b></color></right>",
        f"<center><color={status['fg']}>{record['status']}</color></center>",
    ])

preamble = tentags.serialize.preamble(len(data_rows), 5, border_color="#64748b", border_style="solid-1", cell_height=28)
style = tentags.serialize.style(style_rows, expected_rows=len(data_rows), expected_cols=5)
data = tentags.serialize.data(data_rows, expected_rows=len(data_rows), expected_cols=5)

model = tentags.compile(preamble, style, data)

with open("demo_output/financial_report.html", "w", encoding="utf-8") as f:
    f.write(tentags.render_html(model))

tentags.render_pdf(model, "demo_output/financial_report.pdf")
tentags.render_xlsx(model, "demo_output/financial_report.xlsx")
```

For a database-driven multitable report, build one serialized table dictionary per query:

```python
def table_from_query(conn, document, table_name, sheet_name, title, sql, columns):
    rows = [list(columns)]
    rows.extend([list(row) for row in conn.execute(sql)])

    style_rows = [["<bg=#dbeafe><b></b></bg>"] * len(columns)]
    style_rows.extend([["<bg=#ffffff></bg>"] * len(columns) for _ in rows[1:]])

    return {
        "document": document,
        "table_name": table_name,
        "sheet_name": sheet_name,
        "title": title,
        "preamble": tentags.serialize.preamble(len(rows), len(columns), border_color="#64748b", border_style="solid-1", cell_height=24),
        "style": tentags.serialize.style(style_rows, expected_rows=len(rows), expected_cols=len(columns)),
        "data": tentags.serialize.data(rows, expected_rows=len(rows), expected_cols=len(columns)),
    }

conn = sqlite3.connect("demo_output/business.db")

tables = [
    table_from_query(
        conn,
        "Dashboard",
        "Menu",
        "Menu",
        "Dashboard Menu",
        "SELECT section, target FROM dashboard_links",
        ["Section", "Target"],
    ),
    table_from_query(
        conn,
        "Invoice",
        "Items",
        "Items",
        "Invoice Items",
        "SELECT item, total FROM invoice_items",
        ["Item", "Total"],
    ),
]

tentags.multitable_html(tables, settings={
    "output": "demo_output/db_multitable_report.html",
    "table_order": ["Dashboard!Menu", "Invoice!Items"],
    "tables_per_row": 2,
    "layout": "grid",
    "cols": 2,
    "full_page": True,
})
```

### Multitable export settings

Multitable means several separate logical Lists/Tables, not one large grid. Each List has its own `preamble`, `style(...)`, `data(...)`, title, and XLSX sheet name. File output and visual layout are controlled through library-level `settings=...` dictionaries.

```python
import tentags

tables = [
    {
        "document": "Dashboard",
        "table_name": "Menu",
        "sheet_name": "Menu",
        "title": "Dashboard Menu",
        "preamble": '2,2,1,"#0f172a","solid",0,24',
        "style": "style(<bg=#dbeafe><b></b></bg>, <bg=#dbeafe><b></b></bg>; <bg=#eff6ff></bg>, <bg=#eff6ff></bg>)",
        "data": "data(<mark=Top>Section, Link; Invoice, <url=goto:Invoice!Items!A1>Open invoice</url>)",
    },
    {
        "document": "Invoice",
        "table_name": "Items",
        "sheet_name": "Items",
        "title": "Invoice Items",
        "preamble": '2,2,1,"#7c2d12","solid",0,24',
        "style": "style(<bg=#ffedd5><b></b></bg>, <bg=#ffedd5><b></b></bg>; <bg=#fff7ed></bg>, <bg=#fff7ed></bg>)",
        "data": "data(Item, Total; Paper, <url=goto:Dashboard!Menu!Top>$25</url>)",
    },
]

TABLE_ORDER = ["Dashboard!Menu", "Invoice!Items"]
COLUMNS = {
    "Dashboard!Menu": ["Section", "Link"],
    "Invoice!Items": ["Item", "Total"],
}

HTML_SETTINGS = {
    "output": "demo_output/multitable_demo.html",
    "table_order": TABLE_ORDER,
    "columns": COLUMNS,
    "tables_per_row": 2,
    "html_title": "Multitable Demo",
    "layout": "grid",
    "cols": 2,
    "gap": "30px",
    "full_page": True,
}

XLSX_SHEETS_SETTINGS = {
    "output": "demo_output/multitable_demo.xlsx",
    "table_order": TABLE_ORDER,
    "columns": COLUMNS,
    "tables_per_sheet": 1,
    "mode": "sheets",
}

XLSX_STACKED_SETTINGS = {
    "output": "demo_output/multitable_demo_stacked.xlsx",
    "table_order": TABLE_ORDER,
    "columns": COLUMNS,
    "tables_per_sheet": "all",
    "stacked_sheet_name": "Report",
    "mode": "stacked",
    "gap": 2,
    "show_titles": True,
}

PDF_SETTINGS = {
    "output": "demo_output/multitable_demo.pdf",
    "table_order": TABLE_ORDER,
    "columns": COLUMNS,
    "tables_per_row": "auto",
    "tables_per_page": "auto",
    "gap": 16,
    "page_size": "A4",
    "orientation": "landscape",
    "page_break_after_each": False,
    "margins": (24, 24, 36, 36),
}

html = tentags.multitable_html(tables, settings=HTML_SETTINGS)
tentags.multitable_xlsx(tables, settings=XLSX_SHEETS_SETTINGS)
tentags.multitable_xlsx(tables, settings=XLSX_STACKED_SETTINGS)
tentags.multitable_pdf(tables, settings=PDF_SETTINGS)
```

---

## 4. Django — Template Tags

### Setup

```python
# settings.py
INSTALLED_APPS = [
    ...
    'tentags',
]
```

After this, tags are available via `{% load tentags %}`.

---

### `{% tt %}` — formula directly in the template

```python
# views.py
def report_view(request):
    return render(request, 'report.html', {
        'dept':     'Engineering',
        'revenue':  '$240,000',
        'expenses': '$180,000',
        'profit':   '+$60,000',
    })
```

```html
{# report.html #}
{% load tentags %}

{% tt %}
3, 4, 1, "#cbd5e1", "solid", 0, 45,
style(
    <fs=18><bg=#1e293b><color=white><b><cm> , , , </cm></b></color></bg></fs>;
    <bg=#f1f5f9><b><left></left></b></bg>,
    <bg=#f1f5f9><b><center></center></b></bg>,
    <bg=#f1f5f9><b><center></center></b></bg>,
    <bg=#f1f5f9><b><right></right></b></bg>;
    <left></left>, <right></right>, <right></right>, <right></right>
),
data(
    Financial Report, , , ;
    Department, Revenue, Expenses, Net Profit;
    {{ dept }}, {{ revenue }}, {{ expenses }},
    <bg=#dcfce7><color=#166534><b><right>{{ profit }}</right></b></color></bg>
)
{% endtt %}
```

---

### `{% tentags_inline %}` — formula passed from backend

```python
# views.py
def badge_view(request):
    user_name = "Alice Johnson"
    formula = (
        f"1, 2, 1, '#38bdf8', 'solid', 0, 50, "
        f"data(<b>User:</b> {user_name}, Role: Admin)"
    )
    return render(request, 'badge.html', {'formula': formula})
```

```html
{# badge.html #}
{% load tentags %}

{% tentags_inline formula %}
```

---

### `{% tentags_inline %}` — decoupled mode (3 arguments)

Pass `preamble`, `style`, and `data` as separate variables — one style template reused for multiple rows:

```python
# views.py
def user_table_view(request):
    preamble    = "1, 2, 1, '#10b981', 'solid', 0, 50"
    style_block = "style(<b><left></left></b>, <right></right>)"
    users = [("Alice", "Admin"), ("Bob", "Editor"), ("Charlie", "Viewer")]

    return render(request, 'users.html', {
        'preamble':    preamble,
        'style_block': style_block,
        'data_blocks': [f"data({name}, {role})" for name, role in users],
    })
```

```html
{# users.html #}
{% load tentags %}

{% for data_block in data_blocks %}
    {# Same style template — different data each iteration #}
    {% tentags_inline preamble style_block data_block %}
{% endfor %}
```

---

### All tags in a single `{% tt %}`

```html
{% load tentags %}

{% tt %}
2, 6, 1, "#e2e8f0", "solid", 0, 50,
style(
    <left></left>, <center></center>, <center></center>,
    <center></center>, <center></center>, <right></right>
),
data(
    <b>Bold</b>,
    <i>Italic</i>,
    <u>Underline</u>,
    <s>Strikethrough</s>,
    <url=https://example.com><b>Link</b></url>,
    <color=green><b>+500</b></color>;
    <fs=14><left>{{ user_name }}</left></fs>,
    <bg=#f0f9ff><center>{{ user_role }}</center></bg>,
    <u><center>{{ join_date }}</center></u>,
    <s><right>{{ old_price }}</right></s>,
    <url={{ profile_url }}><color=blue><center>Profile</center></color></url>,
    <bg=#dcfce7><color=#166534><b><right>{{ balance }}</right></b></color></bg>
)
{% endtt %}
```

---

## 5. Flask — Jinja2

### Setup

```python
from flask import Flask, render_template
from tentags.contrib.flask import init_app

app = Flask(__name__)
init_app(app)  # registers {% tt %}, {% tentags %} and {{ tentags(...) }}
```

---

### `{% tt %}` with Jinja2 variables and loops

```python
@app.route('/products')
def products():
    return render_template('products.html', items=[
        {'name': 'Laptop Pro',     'price': '$1,200', 'stock': 45},
        {'name': 'Wireless Mouse', 'price': '$29',    'stock': 200},
        {'name': 'USB-C Hub',      'price': '$49',    'stock': 0},
    ])
```

```html
{# templates/products.html #}

{% tt %}
{{ items|length + 1 }}, 3, 1, "#e2e8f0", "solid", 0, 40,
style(
    <bg=#0f172a><color=white><b><left>Product</left></b></color></bg>,
    <bg=#0f172a><color=white><b><center>Price</center></b></color></bg>,
    <bg=#0f172a><color=white><b><center>Stock</center></b></color></bg>
),
data(
    Product, Price, Stock;
    {% for p in items %}
    <left>{{ p.name }}</left>,
    <center>{{ p.price }}</center>,
    {% if p.stock == 0 %}
        <bg=#fee2e2><color=#991b1b><center>Out of Stock</center></color></bg>
    {% elif p.stock < 50 %}
        <bg=#fef9c3><color=#92400e><center>{{ p.stock }} pcs</center></color></bg>
    {% else %}
        <bg=#dcfce7><color=#166534><center>{{ p.stock }} pcs</center></color></bg>
    {% endif %}
    {% if not loop.last %};{% endif %}
    {% endfor %}
)
{% endtt %}
```

---

### `{{ tentags(...) }}` — global function in template

```python
@app.route('/user/<username>')
def user_profile(username):
    return render_template('profile.html',
        preamble    = '1, 2, 1, "#38bdf8", "solid", 0, 50',
        style_block = 'style(<b><left></left></b>, <right></right>)',
        data_block  = f'data(User: {username}, Role: Admin)'
    )
```

```html
{# templates/profile.html #}

{# Decoupled: 3 arguments from backend #}
{{ tentags(preamble, style_block, data_block) }}

{# Or inline in the template #}
{{ tentags('1,1,1,"black","solid",0,40, data(Welcome ' ~ username ~ ')') }}
```

---

### Pricing table with links and strikethrough

```python
@app.route('/pricing')
def pricing():
    return render_template('pricing.html', plans=[
        {'name': 'Starter',    'old': '$29',  'price': '$19',  'url': '/buy/starter'},
        {'name': 'Pro',        'old': '$79',  'price': '$49',  'url': '/buy/pro'},
        {'name': 'Enterprise', 'old': None,   'price': '$199', 'url': '/buy/enterprise'},
    ])
```

```html
{# templates/pricing.html #}

{% tt %}
{{ plans|length }}, 2, 1, "#e2e8f0", "solid", 0, 55,
data(
    {% for p in plans %}
    <url={{ p.url }}><b><left>{{ p.name }}</left></b></url>,
    <center>
        {% if p.old %}<s>{{ p.old }}</s>  {% endif %}<b>{{ p.price }}</b>
    </center>
    {% if not loop.last %};{% endif %}
    {% endfor %}
)
{% endtt %}
```

---

## 6. FastAPI — Jinja2

### Setup

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from tentags.contrib.fastapi import register_templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")
register_templates(templates)  # registers tags and functions
```

---

### `{% tt %}` in FastAPI

```python
@app.get('/dashboard')
async def dashboard(request: Request):
    return templates.TemplateResponse('dashboard.html', {
        'request': request,
        'kpi': [
            {'metric': 'Revenue',    'value': '$1,200,000', 'change': '+12%',  'up': True},
            {'metric': 'Users',      'value': '45,230',     'change': '+8%',   'up': True},
            {'metric': 'Conversion', 'value': '3.4%',       'change': '-0.2%', 'up': False},
        ]
    })
```

```html
{# templates/dashboard.html #}

{% tt %}
{{ kpi|length + 1 }}, 3, 1, "#e2e8f0", "solid", 0, 50,
style(
    <bg=#0f172a><color=white><b><left></left></b></color></bg>,
    <bg=#0f172a><color=white><b><center></center></b></color></bg>,
    <bg=#0f172a><color=white><b><right></right></b></color></bg>
),
data(
    Metric, Value, Change;
    {% for row in kpi %}
    <left>{{ row.metric }}</left>,
    <b><center>{{ row.value }}</center></b>,
    {% if row.up %}
        <bg=#dcfce7><color=#166534><b><right>{{ row.change }}</right></b></color></bg>
    {% else %}
        <bg=#fee2e2><color=#991b1b><b><right>{{ row.change }}</right></b></color></bg>
    {% endif %}
    {% if not loop.last %};{% endif %}
    {% endfor %}
)
{% endtt %}
```

---

### Invoice via decoupled API

```python
@app.get('/invoice/{invoice_id}')
async def invoice(request: Request, invoice_id: int):
    items = [
        ('Backend Development', 40, '$150/hr', '$6,000'),
        ('UI/UX Design',        20, '$100/hr', '$2,000'),
        ('QA Testing',          15, '$80/hr',  '$1,200'),
    ]
    rows = '; '.join(
        f'<left>{n}</left>, <center>{q}</center>, <center>{p}</center>, <b><right>{t}</right></b>'
        for n, q, p, t in items
    )
    return templates.TemplateResponse('invoice.html', {
        'request':     request,
        'preamble':    f'{len(items) + 2}, 4, 1, "#e2e8f0", "solid", 0, 42',
        'style_block': 'style(<fs=16><b><cm>Invoice, , , </cm></b></fs>; <bg=#3b82f6><color=white><b></b></color></bg>, <bg=#3b82f6><color=white><b><center></center></b></color></bg>, <bg=#3b82f6><color=white><b><center></center></b></color></bg>, <bg=#3b82f6><color=white><b><right></right></b></color></bg>)',
        'data_block':  f'data(Invoice #{invoice_id}, , , ; Description, Qty, Rate, Total; {rows})',
    })
```

```html
{# templates/invoice.html #}
{{ tentags(preamble, style_block, data_block) }}
```

---

## 7. Decoupled API: preamble + style + data

### The Principle

```
preamble → table dimensions, border, cell height
style()  → cell formatting (style tags)
data()   → actual cell content (text, numbers, links)
```

**Key advantage:** `style()` becomes a **reusable template** — define it once, apply with any data.

### One template — three months

```python
import tentags

preamble = '2, 3, 1, "#cbd5e1", "solid", 0, 45'
style = '''style(
    <bg=#0f172a><color=white><b><cm> , , </cm></b></color></bg>;
    <left></left>, <center></center>, <right></right>
)'''

html_jan = tentags.render(preamble, style, 'data(January, , ; Sales, 1200, "$36,000")')
html_feb = tentags.render(preamble, style, 'data(February, , ; Sales, 1450, "$43,500")')
html_mar = tentags.render(preamble, style, 'data(March, , ; Sales, 1800, "$54,000")')
```

---

### URL in decoupled mode

`<url>` is the one tag recommended in `data()` rather than `style()`,
because each row has a different link while the visual formatting stays the same:

```python
# style stays generic — no URL baked in
preamble = '1, 2, 1, "#e2e8f0", "solid", 0, 40'
style    = 'style(<b><left></left></b>, <right></right>)'

# URL lives in data() — unique per row
links = [
    'data(<url=https://github.com>GitHub</url>, Repository)',
    'data(<url=https://docs.example.com>Documentation</url>, API Reference)',
    'data(<url=mailto:support@example.com>Support</url>, Send an email)',
]
for data in links:
    html = tentags.render(preamble, style, data)
```

```html
{# Django #}
{% load tentags %}
{% for item in items %}
    {% tentags_inline preamble style_template item.data_block %}
{% endfor %}

{# Flask / FastAPI (Jinja2) #}
{% for item in items %}
    {{ tentags(preamble, style_template, item.data_block) }}
{% endfor %}
```

---

### data() overrides style()

```python
style = 'style(<color=gray></color>)'       # gray by default
data  = 'data(<color=red>CRITICAL</color>)' # data wins

html = tentags.render(preamble, style, data)
# → text will be red
```

---

## 8. Real-World Examples

### Financial Dashboard (all formats)

```python
import tentags

preamble = '5, 4, 1, "#e2e8f0", "solid", 0, 45'
style = '''style(
    <fs=18><bg=#1e293b><color=white><b><cm> , , , </cm></b></color></bg></fs>;
    <bg=#f1f5f9><b><left></left></b></bg>,
    <bg=#f1f5f9><b><center></center></b></bg>,
    <bg=#f1f5f9><b><center></center></b></bg>,
    <bg=#f1f5f9><b><right></right></b></bg>
)'''
data = '''data(
    Q3 Financial Dashboard, , , ;
    Department, Revenue, Expenses, Net Profit;
    <left>Engineering</left>, <right>"$240,000"</right>, <right>"$180,000"</right>,
        <bg=#dcfce7><color=#166534><b><right>"+$60,000"</right></b></color></bg>;
    <left>Sales & Marketing</left>, <right>"$310,000"</right>, <right>"$210,000"</right>,
        <bg=#dcfce7><color=#166534><b><right>"+$100,000"</right></b></color></bg>;
    <left>Operations</left>, <right>"$120,000"</right>, <right>"$140,000"</right>,
        <bg=#fee2e2><color=#991b1b><b><right>"-$20,000"</right></b></color></bg>
)'''

model = tentags.compile(preamble, style, data)
html  = tentags.render_html(model)
tentags.render_xlsx(model, 'dashboard.xlsx')
tentags.render_pdf(model,  'dashboard.pdf')
```

---

### Link list with formatting

```python
import tentags

preamble = '3, 3, 1, "#e2e8f0", "solid", 0, 45'
style    = '''style(
    <b><left></left></b>, <center></center>, <right></right>;
    <b><left></left></b>, <center></center>, <right></right>;
    <b><left></left></b>, <center></center>, <right></right>
)'''

entries = [
    ('<url=https://github.com/tentags>GitHub Repository</url>', 'Open Source', '<color=green>Active</color>'),
    ('<url=https://pypi.org/project/tentags>PyPI Package</url>', 'v2.1.5',     '<u>Stable</u>'),
    ('<url=https://tentags.readthedocs.io>Documentation</url>',  'Read the Docs', '<color=blue>Online</color>'),
]
rows = '; '.join(f'{link}, {badge}, {status}' for link, badge, status in entries)
html = tentags.render(preamble, style, f'data({rows})')
```

---

### Invoice (XLSX + PDF)

```python
import tentags

items = [
    ('Backend API Development', '40 hrs', '$150/hr', '$6,000'),
    ('UI/UX Design',            '20 hrs', '$100/hr', '$2,000'),
    ('QA Testing',              '15 hrs', '$80/hr',  '$1,200'),
    ('DevOps Setup',            '10 hrs', '$120/hr', '$1,200'),
]

rows_str = '; '.join(
    f'<left>{name}</left>, <center>{qty}</center>, <center>{rate}</center>, <b><right>{total}</right></b>'
    for name, qty, rate, total in items
)

preamble = f'{len(items) + 3}, 4, 1, "#e2e8f0", "solid", 0, 42'
style = '''style(
    <fs=16><bg=white><b><left><cm>INVOICE #1024, , , </cm></left></b></bg></fs>;
    <left><cm>Date: 2026-07-15, , , </cm></left>;
    <bg=#3b82f6><color=white><b>Description</b></color></bg>,
        <bg=#3b82f6><color=white><b><center>Qty</center></b></color></bg>,
        <bg=#3b82f6><color=white><b><center>Rate</center></b></color></bg>,
        <bg=#3b82f6><color=white><b><right>Total</right></b></color></bg>
)'''
data = f'data(INVOICE #1024, , , ; Date: 2026-07-15, , , ; Description, Qty, Rate, Total; {rows_str})'

model = tentags.compile(preamble, style, data)
tentags.render_xlsx(model, 'invoice.xlsx')
tentags.render_pdf(model,  'invoice.pdf')
```

---

### Dynamic table from database (FastAPI + SQLAlchemy)

```python
@app.get('/sales-report')
async def sales_report(request: Request, db: Session = Depends(get_db)):
    rows_db = db.query(Sale).filter(Sale.month == 'July').all()

    header = (
        '<bg=#1e293b><color=white><b>Manager</b></color></bg>, '
        '<bg=#1e293b><color=white><b><center>Sales</center></b></color></bg>, '
        '<bg=#1e293b><color=white><b><right>Revenue</right></b></color></bg>'
    )

    data_rows = []
    for row in rows_db:
        bg    = '#dcfce7' if row.total > 50000 else '#fef9c3'
        color = '#166534' if row.total > 50000 else '#92400e'
        data_rows.append(
            f'<left>{row.manager_name}</left>, '
            f'<center>{row.count}</center>, '
            f'<bg={bg}><color={color}><b><right>${row.total:,.0f}</right></b></color></bg>'
        )

    data = 'data(' + header + '; ' + '; '.join(data_rows) + ')'
    preamble = f'{len(rows_db) + 1}, 3, 1, "#e2e8f0", "solid", 0, 45'
    html_table = tentags.render(f'{preamble}, {data}')

    return templates.TemplateResponse('sales.html', {
        'request': request,
        'table': html_table
    })
```

```html
{# sales.html #}
{{ table | safe }}
```

---

## Quick Reference

### All Tags

| Category | Tag | Description |
|---|---|---|
| Typography | `<b>`, `<i>`, `<u>`, `<s>` | Bold, italic, underline, strikethrough |
| Font size | `<fs=N>` | Font size in px |
| Color | `<color=...>`, `<bg=...>` | Text color / cell background |
| Alignment | `<left>`, `<center>`, `<right>` | Horizontal text alignment |
| Merging | `<cm>`, `<rm>` | Horizontal / vertical cell joining |
| Link | `<url=https://...>` | Clickable hyperlink |
| Image | `<img src=... w=... h=... m=...>` | Single image element |
| Data | `csv("path")` | Inline CSV import |

### Where to write tags

| Tag | Recommended in |
|---|---|
| `<b>`, `<i>`, `<u>`, `<s>`, `<color>`, `<bg>`, `<fs>`, `<left>`, `<center>`, `<right>`, `<cm>`, `<rm>` | `style()` or `data()` — use `style()` for reusable presentation |
| `<url=...>` | `data()` — unique per row |
| `<img src=...>` | `data()` — unique visual content per row |
| `{{ variable }}` (Django / Jinja2) | `data()` — dynamic content from backend |

### Decoupled block order

```
preamble  →  style()  →  data()
```

### Framework comparison

| Feature | Django | Flask (Jinja2) | FastAPI (Jinja2) |
|---|---|---|---|
| Block tag | `{% tt %}...{% endtt %}` | `{% tt %}...{% endtt %}` | `{% tt %}...{% endtt %}` |
| Setup | `'tentags'` in `INSTALLED_APPS` | `init_app(app)` | `register_templates(templates)` |
| Load tags | `{% load tentags %}` | automatic | automatic |
| Inline render | `{% tentags_inline formula %}` | `{{ tentags(formula) }}` | `{{ tentags(formula) }}` |
| Decoupled inline | `{% tentags_inline p s d %}` | `{{ tentags(p, s, d) }}` | `{{ tentags(p, s, d) }}` |
| Template variables | `{{ var }}` | `{{ var }}` | `{{ var }}` |
