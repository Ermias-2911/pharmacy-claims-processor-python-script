import csv
from pathlib import Path

class BatchReader:
    REQUIRED_HEADERS = {
        "claim_id","member_id","ndc","date_of_service",
        "quantity","days_supply","drug_cost","plan_type",
    }

    def read(self, file_path: str) -> list[dict]:
        path = Path(file_path)
        rows = []
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {file_path}")
        with open(file_path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("CSV file is missing header row")
            missing = self.REQUIRED_HEADERS - set(reader.fieldnames)
            if missing:
                raise ValueError(f"CSV file missing required headers: {sorted(missing)}")
            for row in reader:
                rows.append(row)
            return rows
