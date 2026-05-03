from claims_processing.model.claim import Claim

class Normalizer:
    def normalize(self, claim: Claim) -> Claim:
        claim.ndc = claim.ndc.strip()
        claim.plan_type = claim.plan_type.strip().lower()
        claim.member_id = str(claim.member_id).strip()
        return claim
