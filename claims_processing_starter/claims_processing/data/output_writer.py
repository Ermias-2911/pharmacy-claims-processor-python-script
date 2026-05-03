import logging
import json
from pathlib import Path

logger = logging.getLogger(__name__)

class OutputWriter:
    def write(self, results: list, output_path: str) -> None:
        logger.info("Writing %s results to %s", len(results), output_path)

        data = []
        for row in results:
            data.append(row.to_dict())

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
