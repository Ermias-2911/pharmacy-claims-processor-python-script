import json
import tempfile
import unittest
from datetime import datetime, timezone, timedelta
from pathlib import Path

from claims_processing.ndc.ndc_directory_manager import NdcDirectoryManager


class TestNdcManager(unittest.TestCase):

    def test_cache_valid(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "ndc.json"
            file.write_text(json.dumps({
                "created_at": datetime.now(timezone.utc).isoformat(),
                "ndcs": []
            }))

            manager = NdcDirectoryManager(cache_file=file)
            self.assertTrue(manager.is_cache_valid())

    def test_cache_expired(self):
        with tempfile.TemporaryDirectory() as tmp:
            file = Path(tmp) / "ndc.json"

            old_time = datetime.now(timezone.utc) - timedelta(hours=25)

            file.write_text(json.dumps({
                "created_at": old_time.isoformat(),
                "ndcs": []
            }))

            manager = NdcDirectoryManager(cache_file=file)
            self.assertFalse(manager.is_cache_valid())