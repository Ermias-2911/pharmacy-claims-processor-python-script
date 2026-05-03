import tempfile
import unittest
from pathlib import Path

from claims_processing.data.batch_reader import BatchReader


class TestBatchReader(unittest.TestCase):

    def setUp(self):
        self.reader = BatchReader()

    def test_read_valid_csv(self):
        content = (
            "claim_id,member_id,ndc,date_of_service,quantity,days_supply,drug_cost,plan_type\n"
            "CLM001,1234567890,12345-6789-01,2026-01-01,30,30,100.00,commercial\n"
        )

        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "input.csv"
            file.write_text(content)

            rows = self.reader.read(str(file))

            self.assertEqual(1, len(rows))
            self.assertEqual("CLM001", rows[0]["claim_id"])

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError):
            self.reader.read("non_existing.csv")

    def test_missing_header_row(self):
        content = ""  # no header

        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "input.csv"
            file.write_text(content)

            with self.assertRaises(ValueError):
                self.reader.read(str(file))

    def test_missing_required_headers(self):
        content = (
            "claim_id,member_id\n"
            "CLM001,1234567890\n"
        )

        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "input.csv"
            file.write_text(content)

            with self.assertRaises(ValueError) as context:
                self.reader.read(str(file))

            self.assertIn("missing required headers", str(context.exception))


if __name__ == "__main__":
    unittest.main()