"""
Export Sprint 3-UI replay JSON for standalone renderers.

Usage:

    python scripts/export_sprint3_ui_replay_json.py
"""

from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


from ui.replay_export import write_replay_export


DEFAULT_OUTPUT = REPO_ROOT / "ui_replay_exports" / "eaios_sprint3_replay.json"


def main() -> None:
    output_path = write_replay_export(DEFAULT_OUTPUT)
    print(f"Wrote replay export: {output_path}")


if __name__ == "__main__":
    main()
