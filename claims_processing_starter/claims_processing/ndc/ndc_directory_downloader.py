import json
import logging
import urllib.request
import zipfile
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

logger = logging.getLogger(__name__)

DOWNLOAD_INDEX_URL = "https://api.fda.gov/download.json"
OUTPUT_FILE = "directory/ndc_cache.json"


def to_ndc_5_4_2(ndc: str) -> str | None:
    parts = ndc.strip().split("-")

    if len(parts) != 3:
        return None

    s1, s2, s3 = parts

    if not (s1.isdigit() and s2.isdigit() and s3.isdigit()):
        return None

    if len(s1) == 4 and len(s2) == 4 and len(s3) == 2:
        return f"0{s1}-{s2}-{s3}"

    if len(s1) == 5 and len(s2) == 3 and len(s3) == 2:
        return f"{s1}-0{s2}-{s3}"

    if len(s1) == 5 and len(s2) == 4 and len(s3) == 1:
        return f"{s1}-{s2}-0{s3}"

    if len(s1) == 5 and len(s2) == 4 and len(s3) == 2:
        return f"{s1}-{s2}-{s3}"

    return None


def extract_ndcs_from_json(data: dict) -> set[str]:
    ndcs = set()

    for record in data.get("results", []):
        for pkg in record.get("packaging", []):
            package_ndc = pkg.get("package_ndc")

            if package_ndc:
                formatted_ndc = to_ndc_5_4_2(package_ndc)

                if formatted_ndc:
                    ndcs.add(formatted_ndc)

    return ndcs


def download_json_zip(file_url: str) -> dict:
    logger.info("Downloading FDA NDC file: %s", file_url)

    with urllib.request.urlopen(file_url, timeout=120) as response:
        zip_bytes = response.read()

    with zipfile.ZipFile(BytesIO(zip_bytes)) as zip_file:
        json_filename = zip_file.namelist()[0]

        with zip_file.open(json_filename) as json_file:
            return json.loads(json_file.read().decode("utf-8"))


def main() -> None:
    logger.info("Fetching openFDA download index")

    with urllib.request.urlopen(DOWNLOAD_INDEX_URL, timeout=30) as response:
        index = json.loads(response.read().decode("utf-8"))

    partitions = index["results"]["drug"]["ndc"]["partitions"]

    all_ndcs = set()

    for partition in partitions:
        file_url = partition["file"]
        data = download_json_zip(file_url)
        all_ndcs.update(extract_ndcs_from_json(data))

    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cache_data = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "ndcs": sorted(all_ndcs)
    }

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(cache_data, f, indent=2)

    logger.info("Saved %s NDCs to %s", len(all_ndcs), OUTPUT_FILE)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()