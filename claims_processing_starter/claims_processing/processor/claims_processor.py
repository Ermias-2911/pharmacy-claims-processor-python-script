import logging
from claims_processing.builders.result_builder import ResultBuilder
from claims_processing.services.quantity_rule_service import QuantityRuleService
from claims_processing.services.copay_rule_service import CopayRuleService
from claims_processing.data.batch_reader import BatchReader
from claims_processing.data.output_writer import OutputWriter
from claims_processing.model.claim_result import ClaimResult
from claims_processing.model.validation_context import ValidationContext
from claims_processing.data.input_parser import InputParser
from claims_processing.data.normalizer import Normalizer
from claims_processing.services.claim_validation_service import ClaimValidationService

logger = logging.getLogger(__name__)

class ClaimsProcessor:
    def __init__(self, reader: BatchReader, parser: InputParser, normalizer: Normalizer, validator: ClaimValidationService, quantity_rule_service: QuantityRuleService, copay_rule_service: CopayRuleService, result_builder: ResultBuilder, writer: OutputWriter) -> None:
        self.reader = reader
        self.parser = parser
        self.normalizer = normalizer
        self.validator = validator
        self.rule_service = quantity_rule_service
        self.copay_service = copay_rule_service
        self.result_builder = result_builder
        self.writer = writer

    def process(self, input_path: str, output_path: str) -> list[ClaimResult]:
        logger.info("Starting processing input = %s output = %s", input_path, output_path)
        context = ValidationContext()
        results: list[ClaimResult] = []
        approved_count = 0
        rejected_count = 0

        rows = self.reader.read(input_path)
        for row in rows:
            parsed_claim = self.parser.parse(row)
            claim = self.normalizer.normalize(parsed_claim)
            validation_error = self.validator.validate(claim, context)

            if validation_error is not None:
                results.append(self.result_builder.build_rejected(claim, validation_error))
                rejected_count += 1
                continue

            business_error = self.rule_service.apply(claim)
            if business_error is not None:
                results.append(self.result_builder.build_rejected(claim, business_error))
                rejected_count += 1
                continue

            results.append(self.result_builder.build_approved(claim, self.copay_service.calculate(claim)))
            approved_count += 1
        self.writer.write(results, output_path)

        logger.info(
            "Finished processing claims. total = %s approved = %s rejected = %s output_file = %s",
            len(results),
            approved_count,
            rejected_count,
            output_path,
        )
        return results