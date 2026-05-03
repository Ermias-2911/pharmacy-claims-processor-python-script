import unittest
from unittest.mock import Mock

from claims_processing.services.copay_rule_service import CopayRuleService


class TestCopayRuleService(unittest.TestCase):

    def setUp(self):
        self.service = CopayRuleService()

    def test_commercial_min_copay(self):
        claim = Mock()
        claim.claim_id = "CLM001"
        claim.plan_type = "commercial"
        claim.drug_cost = 20.0  # 20% = 4 → min = 10

        self.assertEqual(10.0, self.service.calculate(claim))

    def test_commercial_max_copay(self):
        claim = Mock()
        claim.claim_id = "CLM002"
        claim.plan_type = "commercial"
        claim.drug_cost = 1000.0  # 20% = 200 → max = 100

        self.assertEqual(100.0, self.service.calculate(claim))

    def test_commercial_normal(self):
        claim = Mock()
        claim.claim_id = "CLM003"
        claim.plan_type = "commercial"
        claim.drug_cost = 100.0  # 20% = 20

        self.assertEqual(20.0, self.service.calculate(claim))

    def test_medicare_ndc_starts_with_zero(self):
        claim = Mock()
        claim.claim_id = "CLM004"
        claim.plan_type = "medicare"
        claim.ndc = "01234-5678-90"

        self.assertEqual(15.0, self.service.calculate(claim))

    def test_medicare_ndc_not_start_with_zero(self):
        claim = Mock()
        claim.claim_id = "CLM005"
        claim.plan_type = "medicare"
        claim.ndc = "12345-6789-01"

        self.assertEqual(5.0, self.service.calculate(claim))

    def test_medicaid(self):
        claim = Mock()
        claim.claim_id = "CLM006"
        claim.plan_type = "medicaid"

        self.assertEqual(0.0, self.service.calculate(claim))

    def test_invalid_plan_type(self):
        claim = Mock()
        claim.claim_id = "CLM007"
        claim.plan_type = "unknown"

        with self.assertRaises(ValueError):
            self.service.calculate(claim)


if __name__ == "__main__":
    unittest.main()