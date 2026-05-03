import unittest
from unittest.mock import Mock
from datetime import date, timedelta

from claims_processing.model.claim import Claim
from claims_processing.model.validation_context import ValidationContext
from claims_processing.services.claim_validation_service import ClaimValidationService


class TestClaimValidationService(unittest.TestCase):

    def setUp(self):
        self.ndc_client = Mock()
        self.ndc_client.exists.return_value = True
        self.service = ClaimValidationService(ndc_directory_client=self.ndc_client)
        self.context = ValidationContext()

    def valid_claim(self):
        return Claim(
            claim_id="CLM001",
            member_id="1234567890",
            ndc="12345-6789-01",
            date_of_service="2026-01-01",
            quantity="30",
            days_supply="30",
            drug_cost="100.00",
            plan_type="commercial",
        )

    def test_valid_claim_returns_none(self):
        claim = self.valid_claim()

        result = self.service.validate(claim, self.context)

        self.assertIsNone(result)

    def test_duplicate_claim_id_returns_error(self):
        claim1 = self.valid_claim()
        claim2 = self.valid_claim()

        self.service.validate(claim1, self.context)
        result = self.service.validate(claim2, self.context)

        self.assertEqual("DUPLICATE_CLAIM_ID", result.code)

    def test_invalid_member_id_returns_error(self):
        claim = self.valid_claim()
        claim.member_id = "123"

        result = self.service.validate(claim, self.context)

        self.assertEqual("INVALID_MEMBER_ID", result.code)

    def test_invalid_ndc_format_returns_error(self):
        claim = self.valid_claim()
        claim.ndc = "12345678901"

        result = self.service.validate(claim, self.context)

        self.assertEqual("INVALID_NDC", result.code)

    def test_ndc_not_found_returns_error(self):
        self.ndc_client.exists.return_value = False
        claim = self.valid_claim()

        result = self.service.validate(claim, self.context)

        self.assertEqual("INVALID_NDC", result.code)
        self.assertEqual("ndc not found in FDA NDC Directory", result.message)

    def test_invalid_date_format_returns_error(self):
        claim = self.valid_claim()
        claim.date_of_service = "01-01-2026"

        result = self.service.validate(claim, self.context)

        self.assertEqual("INVALID_DATE_OF_SERVICE", result.code)

    def test_future_date_returns_error(self):
        claim = self.valid_claim()
        claim.date_of_service = (date.today() + timedelta(days=1)).isoformat()

        result = self.service.validate(claim, self.context)

        self.assertEqual("FUTURE_DATE_OF_SERVICE", result.code)

    def test_invalid_quantity_returns_error(self):
        claim = self.valid_claim()
        claim.quantity = "abc"

        result = self.service.validate(claim, self.context)

        self.assertEqual("INVALID_QUANTITY", result.code)

    def test_invalid_days_supply_returns_error(self):
        claim = self.valid_claim()
        claim.days_supply = "91"

        result = self.service.validate(claim, self.context)

        self.assertEqual("INVALID_DAYS_SUPPLY", result.code)

    def test_invalid_drug_cost_returns_error(self):
        claim = self.valid_claim()
        claim.drug_cost = "0"

        result = self.service.validate(claim, self.context)

        self.assertEqual("INVALID_DRUG_COST", result.code)

    def test_invalid_plan_type_returns_error(self):
        claim = self.valid_claim()
        claim.plan_type = "gold"

        result = self.service.validate(claim, self.context)

        self.assertEqual("INVALID_PLAN_TYPE", result.code)


if __name__ == "__main__":
    unittest.main()