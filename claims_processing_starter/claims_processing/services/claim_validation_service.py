import logging
from datetime import datetime, date
from claims_processing.model.claim import Claim
from claims_processing.model.processing_error import ProcessingError
from claims_processing.model.validation_context import ValidationContext

logger = logging.getLogger(__name__)

class ClaimValidationService:
    def __init__(self, ndc_directory_client=None):
        self.ndc_client = ndc_directory_client

    def validate(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        logger.info("Starting validation for claim_id = %s", claim.claim_id)
        validators = [
            self._validate_required_fields,
            self._validate_claim_id_uniqueness,
            self._validate_member_id,
            self._validate_ndc,
            self._validate_date_of_service,
            self._validate_quantity,
            self._validate_days_supply,
            self._validate_drug_cost,
            self._validate_plan_type,
        ]

        for validator in validators:
            error = validator(claim, context)
            if error is not None:
                logger.error(
                    "Validation failed for claim_id = %s error_code = %s error_message=%s",
                    claim.claim_id,
                    error.code,
                    error.message,
                )
                return error
        return None

    def _validate_required_fields(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        fields = {
            "claim_id": claim.claim_id, "member_id": claim.member_id, "ndc": claim.ndc,
            "date_of_service": claim.date_of_service, "quantity": claim.quantity,
            "days_supply": claim.days_supply, "drug_cost": claim.drug_cost, "plan_type": claim.plan_type,
        }
        for name, value in fields.items():
            if value is None or str(value).strip() == "":
                return ProcessingError("MISSING_REQUIRED_FIELD", f"{name} must be present and non-empty")
        return None

    def _validate_claim_id_uniqueness(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        if claim.claim_id in context.seen_claim_ids:
            return ProcessingError("DUPLICATE_CLAIM_ID", "claim id must be unique within the input file")
        context.seen_claim_ids.add(claim.claim_id)
        return None

    def _validate_member_id(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        if not str(claim.member_id).isdigit() or len(str(claim.member_id)) != 10:
            return ProcessingError("INVALID_MEMBER_ID", "member id must be exactly 10 digits")
        return None

    def _validate_ndc(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        original_ndc = str(claim.ndc).strip()

        parts = original_ndc.split("-")

        if len(parts) != 3:
            return ProcessingError("INVALID_NDC", "ndc must be in 5-4-2 format")

        if not (len(parts[0]) == 5 and len(parts[1]) == 4 and len(parts[2]) == 2):
            return ProcessingError("INVALID_NDC", "ndc must be in 5-4-2 format")

        normalized_ndc = "".join(parts)

        if not normalized_ndc.isdigit():
            return ProcessingError("INVALID_NDC", "ndc must contain digits only after normalization")

        if len(normalized_ndc) != 11:
            return ProcessingError("INVALID_NDC", "ndc must be exactly 11 digits after normalization")

        if self.ndc_client and not self.ndc_client.exists(original_ndc):
            return ProcessingError("INVALID_NDC", "ndc not found in FDA NDC Directory")
        return None

    def _validate_date_of_service(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        try:
            dos = datetime.strptime(claim.date_of_service, "%Y-%m-%d").date()
        except ValueError:
            return ProcessingError("INVALID_DATE_OF_SERVICE", "date of service must be a valid YYYY-MM-DD date")
        if dos > date.today():
            return ProcessingError("FUTURE_DATE_OF_SERVICE", "date of service must not be in the future")
        return None

    def _validate_quantity(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        try:
            claim.quantity = int(str(claim.quantity))
        except ValueError:
            return ProcessingError("INVALID_QUANTITY", "quantity must be a valid integer")
        if claim.quantity <= 0:
            return ProcessingError("INVALID_QUANTITY", "quantity must be greater than 0")
        return None

    def _validate_days_supply(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        try:
            claim.days_supply = int(str(claim.days_supply))
        except ValueError:
            return ProcessingError("INVALID_DAYS_SUPPLY", "days supply must be a valid integer")
        if claim.days_supply < 1 or claim.days_supply > 90:
            return ProcessingError("INVALID_DAYS_SUPPLY", "days supply must be between 1 and 90")
        return None

    def _validate_drug_cost(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        try:
            claim.drug_cost = float(str(claim.drug_cost))
        except ValueError:
            return ProcessingError("INVALID_DRUG_COST", "drug cost must be a valid positive number")
        if claim.drug_cost <= 0:
            return ProcessingError("INVALID_DRUG_COST", "drug cost must be greater than 0")
        return None

    def _validate_plan_type(self, claim: Claim, context: ValidationContext) -> ProcessingError | None:
        if claim.plan_type not in {"commercial", "medicare", "medicaid"}:
            return ProcessingError("INVALID_PLAN_TYPE", "plan type must be one of: commercial, medicare, medicaid")
        return None
