<p align="center">
  <img src="TenTags_Demo_Studio/tentags_studio_icon.png?v=2" width="128" alt="TenTags Studio Logo">
</p>


<p align="center">
  <img src="TTS_screen.png?v=2" width="900" alt="TenTags Studio Logo">
</p>


# 🏷️ TenTags Studio & Gallery

[![Version](https://img.shields.io/badge/version-1.0.2-blue.svg)](https://github.com/Jandos77/tentags-studio)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)

A professional low-code visual designer and programmatically compiled dashboard generation suite powered by the **TenTags** library. This project allows developers to visually design complex styled matrices and export them into high-fidelity PDF documents, formatted Excel spreadsheets, and clean HTML pages.

---

## 🌟 Key Features

### 🖥️ TenTags Studio (`tentags_maker.py`)
- **Live Preview Grid**: Real-time visual feedback of cell contents, background colors, custom margins, and custom text styles.
- **Advanced Cell Properties**: Apply font variations (bold, italic, underline, strike), alignment, sizes, foreground/background colors, hyperlinks, and target marks.
- **Spans & Merges**: Visual horizontal (`<cm>`) and vertical (`<rm>`) cell merging.
- **Image Integration**: Load local or remote (HTTP/HTTPS) images inside cells with dynamic width, height, and margin properties.
- **Output Settings Manager**: Configure margins, paper sizes (A3, A4, Letter, etc.), orientations, sheet names, fit-to-page, and gridlines.
- **Live Code Sync (AST-driven)**: Write manual Python code or design visually; the app utilizes Python's Abstract Syntax Trees (AST) to keep both views perfectly synchronized.
- **Asynchronous Compilation & Execution**: Safe script execution in background worker threads with real-time process monitoring.
- **CSV Data & Style Templates**: Load style structures and raw table content directly from CSV files, or export style and data matrices back to CSV. It features automatic dimension synchronization, cell padding for mismatched matrices, and smart auto-alignment for sequential imports.

### 📊 Programmatic Dashboard Gallery
A collection of pre-designed professional dashboards demonstrating the power of the library:
- **BI Dashboard** (`bi_dashboard.py`): A3 landscape BI layout with KPI cards, multi-series charts, contribution heatmaps, progress indicators, and custom branding.
- **GitHub-style Contribution Graph** (`contribution_graph.py`): Git activity heatmaps with custom gradient color mappings.
- **Interactive Calendar** (`calendar_dashboard.py`): Calendar layout highlighting current date and weekend styles.
- **Project Gantt Chart** (`gantt_dashboard.py`): Twelve-week timeline mapping product delivery phases and tracking.
- **Kanban Delivery Board** (`kanban_dashboard.py`): Three-column (Todo, Doing, Done) work organization board.

---

## 📑 TenTags DSL Syntax & 2x2 Example

TenTags uses a compact, matrix-based Domain Specific Language (DSL) to define table structures, styling, and data.

### 1. Preamble Syntax
The preamble string defines the grid dimensions, borders, and general settings:
`'rows, cols, show_grid, grid_color, grid_style, scale_factor, cell_height'`
- **rows / cols**: Number of grid rows and columns.
- **show_grid**: `1` to render gridlines, `0` to hide them.
- **grid_color / grid_style**: Gridline border hex color and line style (e.g., `"solid-1"`, `"dashed-1"`).
- **scale_factor**: Base scale value.
- **cell_height**: Base row height in pixels.

### 2. Style & Data Syntax
- **Style Matrix**: Encased in `style(...)`. Contains styling XML tags separated by commas for columns and semicolons for rows.
- **Data Matrix**: Encased in `data(...)`. Contains text strings, images, or links separated by commas and semicolons.

#### Supported Styling Tags:
- `<bg=...>`: Sets the cell background color.
- `<color=...>`: Sets the text/foreground color.
- `<b>`, `<i>`, `<u>`, `<s>`: Applies bold, italic, underline, or strikethrough.
- `<fs=...>`: Custom font size (e.g., `<fs=16px>`).
- `<center>`, `<left>`, `<right>`: Alignment of the cell content.
- `<cm>`, `<rm>`: Marks cell merges (column merge / row merge).
- `<url=...>`: Creates a hyperlink.
- `<img src=... w=... h=... m=...>`: Embeds an image with width (`w`), height (`h`), and margin (`m`).

#### Color Formats:
You can specify colors in two formats:
1. **Hex Codes (Recommended)**: Any standard 3-digit or 6-digit hex code (e.g., `bg=#1e293b`, `color=#ffffff`).
2. **Color Names**: Standard color names: `black`, `white`, `red`, `green`, `blue`, `yellow`, `cyan`, `magenta`, `gray` (or `grey`), `orange`, `pink`, `purple`, `brown`.

### 3. A Simple 2x2 Table Example

Here is a minimal self-contained Python script building a 2x2 table:

```python
import tentags

# 1. Preamble: 2 rows, 2 columns, border color #cbd5e1, cell height 40
preamble = '2,2,1,"#cbd5e1","solid-1",1,40'

# 2. Style: Green header row, white data row
style = """style(
<center><bg=green><color=white><b>, <center><bg=green><color=white><b>;
<left><bg=white><color=black>, <left><bg=white><color=black>
)"""

# 3. Data: Header labels and cell values
data = """data(
Header 1, Header 2;
Value A, Value B
)"""

# Compile the table model
model = tentags.compile(preamble, style, data)

# Export to HTML
html_output = tentags.render_html(model)
with open("table.html", "w", encoding="utf-8") as f:
    f.write(html_output)
```

---

## 📁 Repository Structure

```text
d:\TenTags Studio
├── export_files/              # Auto-created output folder for HTML/PDF/XLSX exports (git-ignored)
├── TenTags_Demo_Studio/
│   └── tentags_maker.py       # Main visual studio desktop application (Tkinter)
├── bi_dashboard.py            # BI report compiler script
├── calendar_dashboard.py      # Monthly calendar builder
├── contribution_graph.py      # Git contributions graph compiler
├── gantt_dashboard.py         # Product delivery Gantt chart builder
├── kanban_dashboard.py        # Project Kanban board builder
├── dashboard_common.py        # General helper scripts for compile and export
├── studio_renderers.py        # PDF/XLSX image path resolution adapters
├── generate_all.py            # Automated test runner to export all dashboards
├── requirements.txt           # Project dependencies
├── .gitignore                 # Tracked file exclusions
├── LICENSE                    # Apache 2.0 license file
└── README.md                  # Project documentation (this file)
```

---

## 🚀 Quick Start

### 1. Prerequisites
Ensure you have Python 3.8+ installed on your system.

### 2. Installation
Clone the repository and install the required dependencies (including `tentags`, `Pillow`, `openpyxl`, and others):

```powershell
# Clone the repository
git clone https://github.com/Jandos77/tentags-studio.git
cd tentags-studio

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the TenTags Studio
Start the desktop UI compiler to visually build and export your dashboards:

```powershell
python TenTags_Demo_Studio/tentags_maker.py
```

### 4. Compile all Gallery Dashboards
To compile and generate HTML, PDF, and XLSX files for all gallery dashboards:

```powershell
python generate_all.py
```
This generates all corresponding `.html`, `.xlsx`, and `.pdf` files in the `export_files/` directory at the project root. 

> [!NOTE]
> The `export_files/` directory is created automatically on the first compilation run. You do not need to create it manually, and it is excluded from Git tracking to keep the repository clean.

---

## 🛠️ Technology Stack
- **GUI Engine**: Tkinter (Standard Tcl/Tk Python wrapper)
- **Image Processing**: Pillow (PIL)
- **Formatting Engines**: `openpyxl`, `reportlab` (internal to `tentags` rendering)
- **Compiler**: Python `ast` (Abstract Syntax Trees) & `subprocess` execution

---

## 📝 Release History

### v1.0.2 (Current)
- **Output Settings UI**: Added custom file name entry input block in Output panel.
- **Auto-Sync and Auto-Export**: Automatic synchronization of Output panel settings (like filename and format toggles) upon `Regenerate` or `Copy Code` calls.
- **Raw Script copy**: Automated raw Python script execution backup in the exports folder under the custom name.
- **One-click Directory access**: Added `📂 Open Exports` shortcut button to the toolbar to open output files directory directly.
- **Safe Visual Reset**: Upgraded editor clearing routine to sync GUI views directly without writing empty files to storage.

### v1.0.1
- **CSV Data & Style Exports**: Added `Save Data as CSV` and `Save Style as CSV` toolbar buttons to save visual designer grids back to templates.
- **Visual Clear Option**: Added `Clear Data & Style` toolbar button with confirmation dialogs to quickly reset data/style matrices.
- **Website Template Gallery**: Developed a responsive templates gallery on the official website showcasing matched BI, Kanban, and Financial layouts.

### v1.0.0
- **Initial Launch**: AST-driven bi-directional visual editor, programmatic compilation pipelines, and HTML/Excel/PDF rendering outputs.
- **CSV Imports**: Built-in visual loaders to load data and styles from CSV with dimension-syncing padding helpers.

---

## 🧑‍💻 Author

- **Name**: Zhandos Mambetali
- **Email**: [zhandos.mambetali@gmail.com](mailto:zhandos.mambetali@gmail.com)
- **GitHub**: [Jandos77](https://github.com/Jandos77)

---

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
