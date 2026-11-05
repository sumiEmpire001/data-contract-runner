import tempfile
import unittest
from pathlib import Path
from contracts import check,validate_contract,validate_value,run


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.contract={"fields":[{"name":"id","type":"integer","required":True},{"name":"status","type":"string","allowed":["active","paused"]}]}
    def test_valid(self):
        self.assertTrue(check([{"id":"12","status":"active"}],self.contract)["valid"])
    def test_required(self):
        self.assertFalse(check([{"id":"","status":"active"}],self.contract)["valid"])
    def test_integer(self):
        self.assertEqual(validate_value("1.2",{"type":"integer"}),"not an integer")
    def test_boolean(self):
        self.assertEqual(validate_value("maybe",{"type":"boolean"}),"not a boolean")
    def test_nonfinite(self):
        self.assertEqual(validate_value("NaN",{"type":"number"}),"not a finite number")
    def test_allowed(self):
        self.assertFalse(check([{"id":"12","status":"unknown"}],self.contract)["valid"])
    def test_duplicate_field(self):
        with self.assertRaises(ValueError): validate_contract({"fields":[{"name":"x","type":"string"},{"name":"x","type":"integer"}]})
    def test_file_run(self):
        with tempfile.TemporaryDirectory() as directory:
            csvfile=Path(directory)/"data.csv"
            contractfile=Path(directory)/"contract.json"
            csvfile.write_text("id,status\n1,active\n",encoding="utf-8")
            contractfile.write_text('{"fields":[{"name":"id","type":"integer","required":true}]}',encoding="utf-8")
            self.assertTrue(run(str(csvfile),str(contractfile))["valid"])


if __name__=="__main__":
    unittest.main()
