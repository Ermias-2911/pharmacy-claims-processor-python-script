import unittest
from unittest.mock import Mock

from claims_processing.processor.claims_processor import ClaimsProcessor


class TestClaimsProcessor(unittest.TestCase):

    def test_process_approved_claim(self):
        reader = Mock()
        parser = Mock()
        normalizer = Mock()
        validator = Mock()
        quantity_rule_service = Mock()
        copay_rule_service = Mock()
        result_builder = Mock()
        writer = Mock()

        row = {"claim_id": "CLM001"}
        parsed_claim = Mock()
        claim = Mock()
        result = Mock()

        reader.read.return_value = [row]
        parser.parse.return_value = parsed_claim
        normalizer.normalize.return_value = claim
        validator.validate.return_value = None
        quantity_rule_service.apply.return_value = None
        copay_rule_service.calculate.return_value = 20.0
        result_builder.build_approved.return_value = result

        processor = ClaimsProcessor(
            reader=reader,
            parser=parser,
            normalizer=normalizer,
            validator=validator,
            quantity_rule_service=quantity_rule_service,
            copay_rule_service=copay_rule_service,
            result_builder=result_builder,
            writer=writer,
        )

        results = processor.process("input.csv", "output.json")

        reader.read.assert_called_once_with("input.csv")
        parser.parse.assert_called_once_with(row)
        normalizer.normalize.assert_called_once_with(parsed_claim)

        validator.validate.assert_called_once()
        called_claim, called_context = validator.validate.call_args.args
        self.assertEqual(claim, called_claim)
        self.assertIsNotNone(called_context)

        quantity_rule_service.apply.assert_called_once_with(claim)
        copay_rule_service.calculate.assert_called_once_with(claim)
        result_builder.build_approved.assert_called_once_with(claim, 20.0)

        writer.write.assert_called_once_with([result], "output.json")
        self.assertEqual([result], results)


if __name__ == "__main__":
    unittest.main()