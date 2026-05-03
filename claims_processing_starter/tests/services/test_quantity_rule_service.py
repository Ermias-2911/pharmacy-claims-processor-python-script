import unittest
from unittest.mock import Mock

from claims_processing.services.copay_rule_service import CopayRuleService


class TestCopayRuleService(unittest.TestCase):

    def setUp(self):
        self.service = CopayRuleService()

    def test_commercial_min_copay(self):
        claim = Mock()
        claim.plan_type = "commercial"
        claim.drug_cost = 20.0  # 20% = 4 → should become 10 (min)

        result = self.service.calculate(claim)

        self.assertEqual(10.0, result)

    def test_commercial_max_copay(self):
        claim = Mock()
        claim.plan_type = "commercial"
        claim.drug_cost = 1000.0  # 20% = 200 → should cap at 100

        result = self.service.calculate(claim)

        self.assertEqual(100.0, result)

    def test_commercial_normal_range(self):
        claim = Mock()
        claim.plan_type = "commercial"
        claim.drug_cost = 100.0  # 20% = 20

        result = self.service.calculate(claim)

        self.assertEqual(20.0, result)

    def test_medicare_ndc_starts_with_zero(self):
        claim = Mock()
        claim.plan_type = "medicare"
        claim.ndc = "01234-5678-90"

        result = self.service.calculate(claim)

        self.assertEqual(15.0, result)

    def test_medicare_ndc_not_start_with_zero(self):
        claim = Mock()
        claim.plan_type = "medicare"
        claim.ndc = "12345-6789-01"

        result = self.service.calculate(claim)

        self.assertEqual(5.0, result)

    def test_medicaid(self):
        claim = Mock()
        claim.plan_type = "medicaid"

        result = self.service.calculate(claim)

        self.assertEqual(0.0, result)

    def test_invalid_plan_type(self):
        claim = Mock()
        claim.plan_type = "invalid"

        with self.assertRaises(ValueError):
            self.service.calculate(claim)


if __name__ == "__main__":
    unittest.main()