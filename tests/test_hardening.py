"""Adversarial input and CLI integration regression tests."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from contracts import check, validate_contract


class HardeningTests(unittest.TestCase):
    def setUp(self):
        self.contract = {"fields": [{"name": "id", "type": "integer", "required": True}]}

    def test_reject_non_object_field(self):
        with self.assertRaises(ValueError):
            validate_contract({"fields": [None]})

    def test_reject_nonboolean_required(self):
        with self.assertRaises(ValueError):
            validate_contract({"fields": [{"name": "id", "type": "string", "required": "false"}]})

    def test_reject_invalid_allowed_list(self):
        with self.assertRaises(ValueError):
            validate_contract({"fields": [{"name": "id", "type": "string", "allowed": "abc"}]})

    def test_reject_extra_columns(self):
        self.assertFalse(check([{"id": "1", None: ["unexpected"]}], self.contract)["valid"])

    def test_missing_column(self):
        self.assertFalse(check([{}], self.contract)["valid"])

    def test_invalid_number_does_not_crash(self):
        contract = {"fields": [{"name": "amount", "type": "number"}]}
        self.assertFalse(check([{"amount": "1e999"}], contract)["valid"])

    def test_cli_exit_codes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            schema = root / "contract.json"
            source = root / "data.csv"
            schema.write_text(json.dumps(self.contract), encoding="utf-8")
            script = Path(__file__).resolve().parents[1] / "contracts.py"
            for value, expected in (("12", 0), ("bad", 1)):
                with self.subTest(value=value):
                    source.write_text("id\n" + value + "\n", encoding="utf-8")
                    result = subprocess.run(
                        [sys.executable, str(script), str(source), str(schema)],
                        capture_output=True, text=True, timeout=15, check=False,
                    )
                    self.assertEqual(result.returncode, expected, result.stderr)


if __name__ == "__main__":
    unittest.main()
