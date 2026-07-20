import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "bi_dashboard.py",
    "contribution_graph.py",
    "calendar_dashboard.py",
    "gantt_dashboard.py",
    "kanban_dashboard.py",
]

for script in SCRIPTS:
    print(f"\nGenerating {script}...")
    runpy.run_path(str(ROOT / script), run_name="__main__")
