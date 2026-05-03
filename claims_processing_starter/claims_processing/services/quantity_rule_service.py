import logging
from claims_processing.model.claim import Claim
from claims_processing.model.processing_error import ProcessingError

logger = logging.getLogger(__name__)
class QuantityRuleService:
    def apply(self, claim: Claim) -> ProcessingError | None:
        logger.info("Applying services rules for claim_id = %s", claim.claim_id)

        if claim.days_supply == 0:
            return ProcessingError("INVALID_DAYS_SUPPLY", "days_supply cannot be zero")

        if (claim.quantity / claim.days_supply) > 3:
            return ProcessingError("TOO_MANY_PILLS_PER_DAY", "quantity / days_supply must be less than or equal to 3")
        return None
