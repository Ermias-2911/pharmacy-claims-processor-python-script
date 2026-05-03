import unittest

from claims_processing.data.input_parser import InputParser


class TestInputParser(unittest.TestCase):

    def setUp(self):
        self.parser = InputParser()

    def test_parse_trims_all_fields(self):
        row = {
            "claim_id": " CLM001 ",
            "member_id": " 1234567890 ",
            "ndc": " 12345-6789-01 ",
            "date_of_service": " 2026-01-01 ",
            "quantity": " 30 ",
            "days_supply": " 30 ",
            "drug_cost": " 100.00 ",
            "plan_type": " commercial ",
        }

        claim = self.parser.parse(row)

        self.assertEqual("CLM001", claim.claim_id)
        self.assertEqual("1234567890", claim.member_id)
        self.assertEqual("12345-6789-01", claim.ndc)
        self.assertEqual("commercial", claim.plan_type)

    def test_parse_handles_missing_fields(self):
        row = {}  # empty input

        claim = self.parser.parse(row)

        self.assertEqual("", claim.claim_id)
        self.assertEqual("", claim.member_id)
        self.assertEqual("", claim.ndc)
        self.assertEqual("", claim.plan_type)

    def test_parse_handles_none_values(self):
        row = {
            "claim_id": None,
            "member_id": None,
            "ndc": None,
            "date_of_service": None,
            "quantity": None,
            "days_supply": None,
            "drug_cost": None,
            "plan_type": None,
        }

        claim = self.parser.parse(row)

        self.assertEqual("", claim.claim_id)
        self.assertEqual("", claim.member_id)
        self.assertEqual("", claim.ndc)
        self.assertEqual("", claim.plan_type)


if __name__ == "__main__":
    unittest.main()