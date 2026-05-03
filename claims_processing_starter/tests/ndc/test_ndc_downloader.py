import unittest
from claims_processing.ndc.ndc_directory_downloader import to_ndc_5_4_2


class TestNdcDownloader(unittest.TestCase):

    def test_convert_4_4_2(self):
        self.assertEqual("01234-5678-90", to_ndc_5_4_2("1234-5678-90"))

    def test_invalid_format(self):
        self.assertIsNone(to_ndc_5_4_2("12345678901"))