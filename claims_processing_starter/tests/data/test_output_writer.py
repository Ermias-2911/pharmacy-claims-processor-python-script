import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock

from claims_processing.data.output_writer import OutputWriter


class TestOutputWriter(unittest.TestCase):

    def setUp(self):
        self.writer = OutputWriter()

    def test_write_outputs_json(self):
        # mock result objects
        result1 = Mock()
        result1.to_dict.return_value = {"claimId": "CLM001", "status": "APPROVED"}

        result2 = Mock()
        result2.to_dict.return_value = {"claimId": "CLM002", "status": "REJECTED"}

        results = [result1, result2]

        with tempfile.TemporaryDirectory() as tmp:
            output_file = Path(tmp) / "output.json"

            self.writer.write(results, str(output_file))

            content = json.loads(output_file.read_text())

            self.assertEqual(2, len(content))
            self.assertEqual("CLM001", content[0]["claimId"])
            self.assertEqual("REJECTED", content[1]["status"])

    def test_write_empty_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            output_file = Path(tmp) / "output.json"

            self.writer.write([], str(output_file))

            content = json.loads(output_file.read_text())

            self.assertEqual([], content)


if __name__ == "__main__":
    unittest.main()