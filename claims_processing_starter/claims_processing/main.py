import logging
import sys
from claims_processing.ndc.ndc_directory_manager import NdcDirectoryManager
from claims_processing.ndc.ndc_directory_downloader import main as download_ndc_directory
from claims_processing.ndc.ndc_directory_client import NdcDirectoryClient
from claims_processing.builders.result_builder import ResultBuilder
from claims_processing.services.quantity_rule_service import QuantityRuleService
from claims_processing.services.copay_rule_service import CopayRuleService
from claims_processing.config.logger_config import configure_logging
from claims_processing.data.batch_reader import BatchReader
from claims_processing.data.output_writer import OutputWriter
from claims_processing.data.input_parser import InputParser
from claims_processing.data.normalizer import Normalizer
from claims_processing.processor.claims_processor import ClaimsProcessor
from claims_processing.services.claim_validation_service import ClaimValidationService


logger = logging.getLogger(__name__)

def ensure_ndc_cache_ready() -> None:
    cache_manager = NdcDirectoryManager()

    if not cache_manager.is_cache_valid():
        logger.info("NDC cache missing or expired. Downloading new NDC directory...")
        download_ndc_directory()
    else:
        logger.info("NDC cache is fresh. Skipping NDC download.")

def main() -> int:

    configure_logging(logging.INFO)
    ensure_ndc_cache_ready()

    if len(sys.argv) != 3:
        logger.error("Usage: python -m claims_processing.processor.main <input_csv> <output_json>")
        return 1


    # to avoid position argument assign variable to function that match variable name from the constructor
    processor = ClaimsProcessor(
        reader=BatchReader(),
        parser=InputParser(),
        normalizer=Normalizer(),
        validator=ClaimValidationService(
            ndc_directory_client=NdcDirectoryClient("directory/ndc_cache.json")
        ),
        quantity_rule_service=QuantityRuleService(),
        copay_rule_service=CopayRuleService(),
        result_builder=ResultBuilder(),
        writer=OutputWriter(),
    )
    processor.process(sys.argv[1], sys.argv[2])


    return 0

if __name__ == "__main__":
    raise SystemExit(main())
