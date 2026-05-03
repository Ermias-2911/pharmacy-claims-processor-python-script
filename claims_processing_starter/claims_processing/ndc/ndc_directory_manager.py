import json
from datetime import datetime, timezone, timedelta
from pathlib import Path


class NdcDirectoryManager:

    def __init__(self, cache_file: str | Path = "directory/ndc_cache.json"):
        self.cache_file = Path(cache_file)

    def is_cache_valid(self) -> bool:
        if not self.cache_file.exists():
            return False

        try:
            with self.cache_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            created_at = data.get("created_at")
            if not created_at:
                return False

            created_time = datetime.fromisoformat(created_at)

            if created_time.tzinfo is None:
                created_time = created_time.replace(tzinfo=timezone.utc)

            now = datetime.now(timezone.utc)
            age = now - created_time

            return age < timedelta(hours=24)

        except Exception:
            return False