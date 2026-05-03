import logging
from claims_processing.model.claim import Claim

logger = logging.getLogger(__name__)

class CopayRuleService:
    def calculate(self, claim: Claim) -> float:
        logger.info("Calculating copay for claim_id = %s", claim.claim_id)
        if claim.plan_type == "commercial":
            copay = max(10.0, min(100.0, claim.drug_cost * 0.20))
        elif claim.plan_type == "medicare":
            copay = 15.0 if str(claim.ndc).startswith("0") else 5.0
        elif claim.plan_type == "medicaid":
            copay = 0.0
        else:
            raise ValueError(f"Unsupported plan_type: {claim.plan_type}")
        return round(copay, 2)
