"""Regression tests for the Phase 23 FINAL runner's corrected output/checkpoint path.

These tests never execute the campaign and never write to the real
results/phase23_final_raw.json historical artifact; they only exercise the
path-resolution, checkpoint, and validation plumbing against isolated
temporary files.
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import phase23_final as p23


def _sample_record(run_id, method_id, workload_id, failure_id, repetition_id):
    return {
        "run_id": run_id,
        "attempt_id": f"attempt-{run_id}",
        "method_id": method_id,
        "workload_id": workload_id,
        "failure_scenario_id": failure_id,
        "repetition_id": repetition_id,
        "status": "VALID",
        "requests_total": 1200,
        "records": [],
        "provenance": {},
    }


class Phase23FinalCorrectedOutputTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.corrected_path = Path(self.tmpdir.name) / "phase23_final_corrected_raw.json"

    def _historical_stat(self):
        stat = p23.DEFAULT_RAW.stat()
        return (stat.st_size, stat.st_mtime_ns, stat.st_ino)

    def test_default_paths_preserve_existing_behavior(self):
        paths = p23.derive_paths(None)
        self.assertEqual(paths["raw"], p23.DEFAULT_RAW)
        self.assertEqual(paths["report_json"].name, "phase23_final_execution_report.json")
        self.assertEqual(paths["report_txt"].name, "phase23_final_execution_report.txt")

    def test_corrected_output_path_resolves_to_a_distinct_artifact(self):
        paths = p23.derive_paths(str(self.corrected_path))
        self.assertEqual(paths["raw"], self.corrected_path.resolve())
        self.assertNotEqual(paths["raw"], p23.DEFAULT_RAW)
        self.assertEqual(paths["report_json"].name, "phase23_final_corrected_execution_report.json")
        self.assertEqual(paths["report_txt"].name, "phase23_final_corrected_execution_report.txt")

    # (A) the historical file is never treated as a checkpoint for the corrected output path.
    def test_missing_corrected_output_never_falls_back_to_historical_checkpoint(self):
        loaded = p23.load_existing(self.corrected_path)
        self.assertEqual(loaded, {})
        self.assertFalse(self.corrected_path.exists())
        # the historical file's presence/content must be irrelevant to this call
        self.assertTrue(p23.DEFAULT_RAW.exists())

    # (B) a corrected output file resumes only from its own completed run IDs.
    def test_corrected_output_resumes_only_from_its_own_completed_run_ids(self):
        record = _sample_record("Proposed-W01-F0-rep-01", "Proposed", "W01", "F0", "rep-01")
        p23.write_checkpoint([record], self.corrected_path)
        loaded = p23.load_existing(self.corrected_path)
        self.assertEqual(set(loaded), {"Proposed-W01-F0-rep-01"})
        # a second, unrelated identity must not appear merely because the historical
        # artifact happens to contain it.
        self.assertNotIn("DPRS-W01-F0-rep-01", loaded)

    # (C) atomic checkpointing still works.
    def test_atomic_checkpoint_write_produces_valid_json_with_no_leftover_temp_files(self):
        record = _sample_record("HRS-W02-F1-rep-02", "HRS", "W02", "F1", "rep-02")
        p23.write_checkpoint([record], self.corrected_path)
        self.assertTrue(self.corrected_path.exists())
        with self.corrected_path.open() as stream:
            data = json.load(stream)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["run_id"], "HRS-W02-F1-rep-02")
        leftovers = [
            name for name in os.listdir(self.corrected_path.parent)
            if name.startswith(f"{self.corrected_path.stem}_") and name != self.corrected_path.name
        ]
        self.assertEqual(leftovers, [])
        # a second write must still replace atomically and keep valid content
        record2 = _sample_record("HRS-W02-F1-rep-03", "HRS", "W02", "F1", "rep-03")
        p23.write_checkpoint([record, record2], self.corrected_path)
        with self.corrected_path.open() as stream:
            data = json.load(stream)
        self.assertEqual({item["run_id"] for item in data}, {"HRS-W02-F1-rep-02", "HRS-W02-F1-rep-03"})

    # (D) validation reads the selected output file, not the historical one.
    def test_validation_reads_the_selected_output_not_the_historical_file(self):
        record = _sample_record("OGSA-W03-F2-rep-03", "OGSA", "W03", "F2", "rep-03")
        p23.write_checkpoint([record], self.corrected_path)
        records = p23.load_existing(self.corrected_path)
        result = p23.validate(records)
        # only the single corrected-artifact run is present, far from the full
        # 2250-run matrix -> proves validate() operated on the tiny selected
        # artifact rather than the complete historical dataset.
        self.assertEqual(result["checks"]["unique_runs"], 1)
        self.assertEqual(result["validation"], "FAIL")

    # (E) the historical pre-repair artifact remains byte-for-byte untouched.
    def test_historical_pre_repair_artifact_is_untouched_by_corrected_path_operations(self):
        before = self._historical_stat()
        p23.load_existing(self.corrected_path)
        p23.write_checkpoint([_sample_record("EIMORM-W01-F0-rep-01", "EIMORM", "W01", "F0", "rep-01")], self.corrected_path)
        p23.derive_paths(str(self.corrected_path))
        p23.main(["--output", str(self.corrected_path), "--dry-run"])
        after = self._historical_stat()
        # size/mtime/inode triad is unchanged: the file was neither rewritten,
        # truncated, nor replaced (os.replace() would change the inode).
        self.assertEqual(before, after)

    def test_dry_run_reports_selected_path_and_executes_no_campaign(self):
        result_path = Path(self.tmpdir.name) / "dry_run_stdout.txt"
        import contextlib
        import io

        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            p23.main(["--output", str(self.corrected_path), "--dry-run"])
        payload = json.loads(buffer.getvalue())
        self.assertTrue(payload["dry_run"])
        self.assertEqual(payload["selected_output_path"], str(self.corrected_path.resolve()))
        self.assertFalse(payload["uses_historical_default_path"])
        self.assertEqual(payload["completed_run_ids_source"], str(self.corrected_path.resolve()))
        self.assertFalse(payload["campaign_executed"])
        self.assertFalse(self.corrected_path.exists())  # dry-run must not create the checkpoint
        result_path.write_text(buffer.getvalue())


if __name__ == "__main__":
    unittest.main()
