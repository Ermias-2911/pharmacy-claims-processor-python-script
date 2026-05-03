from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class ClaimResult:
    claim_id: str
    status: str
    copay_amount: Optional[float]
    rejection_reason: Optional[str]
    processed_at: str

    def to_dict(self) -> dict:
        return asdict(self)
