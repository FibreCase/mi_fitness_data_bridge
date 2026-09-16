"""Checks for the public fixture: no cloud account, no personal data."""
import csv
import importlib.util
import io
import json
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_synthetic_site", ROOT / "scripts/build_synthetic_site.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_site_sample_matches_real_synthetic_export():
    with patch("socket.socket.connect", side_effect=AssertionError("Network forbidden")):
        sample = module.build_sample()
    assert sample["synthetic"] is True
    assert set(sample["csv"]) == {f"{key}.csv" for key in sample["json"]["records"]}
    for records in sample["json"]["records"].values():
        for record in records:
            assert record["user_id"] == "synthetic-demo-user"
            assert not any("token" in key.lower() for key in record)
    sleep = list(csv.DictReader(io.StringIO(sample["csv"]["sleep.csv"].lstrip("\ufeff"))))
    assert sleep[0]["duration_minutes"] == "465"
    assert all(content.startswith("\ufeff") for content in sample["csv"].values())
    checked_in = (ROOT / "site/sample.js").read_text(encoding="utf-8")
    assert json.loads(checked_in.split("const SAMPLE = ", 1)[1].rstrip().removesuffix(";")) == sample


def test_export_closes_database_connection(tmp_path):
    from mi_fitness_mcp.export import export_database
    from mi_fitness_mcp.storage import Database

    db = tmp_path / "sample.db"
    Database(db)
    from mi_fitness_mcp import export
    original = export._connect_read_only
    connections = []

    def capture(path):
        conn = original(path)
        connections.append(conn)
        return conn

    import sqlite3

    import pytest

    with patch.object(export, "_connect_read_only", side_effect=capture):
        export_database(db, tmp_path / "out.json")
    with pytest.raises(sqlite3.ProgrammingError, match="closed"):
        connections[0].execute("SELECT 1")
