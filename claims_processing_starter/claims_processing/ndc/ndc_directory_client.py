import json
from pathlib import Path


class NdcDirectoryClient:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.ndcs = self._load_ndcs()

    def _load_ndcs(self) -> set[str]:
        if not self.file_path.exists():
            return set()

        with self.file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return set(data.get("ndcs", []))

        if isinstance(data, list):
            return set(data)

        return set()

    def exists(self, ndc: str) -> bool:
        normalized_input = ndc.replace("-", "")
        return any(cached_ndc.replace("-", "") == normalized_input for cached_ndc in self.ndcs)