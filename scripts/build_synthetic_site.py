"""Build a static, account-free sample from the real exporter and synthetic seed.

No user-supplied database, credentials, configuration or network is read.
Only the disposable fixture created here can be exported by this script.
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
from synthetic_demo import seed  # noqa: E402

from mi_fitness_mcp.export import export_database  # noqa: E402
from mi_fitness_mcp.storage import Database  # noqa: E402


def build_sample() -> dict:
    with tempfile.TemporaryDirectory(prefix="mi-bridge-public-synthetic-") as directory:
        work = Path(directory)
        db_path = work / "synthetic.db"
        seed(Database(db_path))
        json_path = work / "synthetic.json"
        csv_path = work / "csv"
        export_database(db_path, json_path, output_format="json")
        csv_files = export_database(db_path, csv_path, output_format="csv")
        payload = json.loads(json_path.read_text(encoding="utf-8"))
        # Stable build output; these are explicitly synthetic presentation timestamps.
        payload["generated_at"] = "2026-07-15T20:00:00+00:00"
        for records in payload["records"].values():
            for row in records:
                assert row["user_id"] == "synthetic-demo-user"
                for field in ("created_at", "updated_at"):
                    if field in row:
                        row[field] = "2026-07-15 20:00:00"
        csv_outputs = {}
        # Reconstruct deterministic CSV from the exporter output, preserving its columns/BOM.
        import csv
        import io
        for path in csv_files:
            rows = list(csv.reader(io.StringIO(path.read_text(encoding="utf-8-sig"))))
            for row in rows[1:]:
                for field in ("created_at", "updated_at"):
                    if field in rows[0]:
                        row[rows[0].index(field)] = "2026-07-15 20:00:00"
            stream = io.StringIO(newline="")
            csv.writer(stream).writerows(rows)
            csv_outputs[path.name] = "\ufeff" + stream.getvalue()
        return {"synthetic": True, "json": payload, "csv": csv_outputs}


def main() -> None:
    sample = json.dumps(build_sample(), ensure_ascii=False, indent=2)
    (ROOT / "site" / "sample.js").write_text(
        "// Generated ONLY from examples/synthetic_demo.py. Never replace with personal exports.\n"
        "const SAMPLE = " + sample + ";\n", encoding="utf-8"
    )
    print("Built site/sample.js from synthetic records; no account or network used.")


if __name__ == "__main__":
    main()
