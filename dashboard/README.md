# TenTags Dashboard Gallery

Run all examples from this directory:

```powershell
python generate_all.py
```

Every example uses only the public TenTags API:

```text
Python matrices
    -> tentags.serialize.style/data
    -> tentags.compile(preamble, style, data)
    -> render_html / render_xlsx / render_pdf
```

Included dashboards:

- `dashboard.py` - A3 landscape BI dashboard with logo, KPI cards, two-series chart, heatmap, progress bars, legends, insight, and footer.
- `contribution_graph.py` - GitHub-style contribution heatmap.
- `calendar_july_2026.py` - July 2026 calendar with the current date highlighted.
- `gantt_dashboard.py` - Twelve-week product delivery Gantt.
- `kanban_dashboard.py` - TODO, DOING, and DONE delivery board.

Each script produces matching `.html`, `.xlsx`, and `.pdf` files next to itself.
