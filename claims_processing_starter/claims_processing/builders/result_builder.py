import logging
from datetime import datetime, timezone
from claims_processing.model.claim import Claim
from claims_processing.model.claim_result import ClaimResult
from claims_processing.model.processing_error import ProcessingError


logger = logging.getLogger(__name__)
class ResultBuilder:
    def build_approved(self, claim: Claim, copay: float) -> ClaimResult:
        logger.info("Building APPROVED result for claim_id = %s", claim.claim_id)
        return ClaimResult(claim.claim_id, "APPROVED", round(copay, 2), None, self._timestamp())

    def build_rejected(self, claim: Claim, error: ProcessingError) -> ClaimResult:
        logger.info("Building REJECTED result for claim_id = %s", claim.claim_id)
        return ClaimResult(claim.claim_id, "REJECTED", None, error.message, self._timestamp())

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
