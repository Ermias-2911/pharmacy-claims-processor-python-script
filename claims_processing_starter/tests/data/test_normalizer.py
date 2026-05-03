import unittest

from claims_processing.data.normalizer import Normalizer
from claims_processing.model.claim import Claim


class TestNormalizer(unittest.TestCase):

    def setUp(self):
        self.normalizer = Normalizer()

    def test_normalize_trims_and_lowercases(self):
        claim = Claim(
            claim_id="CLM001",
            member_id=" 1234567890 ",
            ndc=" 12345-6789-01 ",
            date_of_service="2026-01-01",
            quantity="30",
            days_supply="30",
            drug_cost="100.00",
            plan_type=" COMMERCIAL ",
        )

        result = self.normalizer.normalize(claim)

        self.assertEqual("12345-6789-01", result.ndc)
        self.assertEqual("commercial", result.plan_type)
        self.assertEqual("1234567890", result.member_id)

    def test_normalize_converts_member_id_to_string(self):
        claim = Claim(
            claim_id="CLM002",
            member_id=1234567890,  # int input
            ndc="12345-6789-01",
            date_of_service="2026-01-01",
            quantity="30",
            days_supply="30",
            drug_cost="100.00",
            plan_type="medicaid",
        )

        result = self.normalizer.normalize(claim)

        self.assertIsInstance(result.member_id, str)
        self.assertEqual("1234567890", result.member_id)

    def test_normalize_returns_same_object(self):
        claim = Claim(
            claim_id="CLM003",
            member_id="1234567890",
            ndc="12345-6789-01",
            date_of_service="2026-01-01",
            quantity="30",
            days_supply="30",
            drug_cost="100.00",
            plan_type="commercial",
        )

        result = self.normalizer.normalize(claim)

        self.assertIs(claim, result)  # same object (mutation)


if __name__ == "__main__":
    unittest.main()