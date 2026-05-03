from claims_processing.model.claim import Claim

class InputParser:
    def parse(self, row: dict) -> Claim:
        return Claim(
            claim_id=(row.get("claim_id") or "").strip(),
            member_id=(row.get("member_id") or "").strip(),
            ndc=(row.get("ndc") or "").strip(),
            date_of_service=(row.get("date_of_service") or "").strip(),
            quantity=(row.get("quantity") or "").strip(),
            days_supply=(row.get("days_supply") or "").strip(),
            drug_cost=(row.get("drug_cost") or "").strip(),
            plan_type=(row.get("plan_type") or "").strip(),
        )
