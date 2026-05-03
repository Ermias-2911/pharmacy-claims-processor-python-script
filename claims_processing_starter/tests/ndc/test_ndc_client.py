import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from claims_processing.ndc.ndc_directory_client import NdcDirectoryClient


class TestNdcClient(unittest.TestCase):

    def test_exists_with_hyphen(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "ndc.json"
            file.write_text(json.dumps({
                "created_at": datetime.now(timezone.utc).isoformat(),
                "ndcs": ["12345-6789-01"]
            }))

            client = NdcDirectoryClient(str(file))
            self.assertTrue(client.exists("12345-6789-01"))

    def test_exists_without_hyphen(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "ndc.json"
            file.write_text(json.dumps({
                "created_at": datetime.now(timezone.utc).isoformat(),
                "ndcs": ["12345-6789-01"]
            }))

            client = NdcDirectoryClient(str(file))
            self.assertTrue(client.exists("12345678901"))