"""Regression tests for registry cache behavior."""

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from hermes_link import registry


class FetchIndexTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.cache_file = Path(self.temporary_directory.name) / "index.json"
        self.cache_patch = patch.object(registry, "CACHE_FILE", self.cache_file)
        self.cache_directory_patch = patch.object(
            registry, "CACHE_DIR", self.cache_file.parent
        )
        self.cache_patch.start()
        self.cache_directory_patch.start()

    def tearDown(self) -> None:
        self.cache_directory_patch.stop()
        self.cache_patch.stop()
        self.temporary_directory.cleanup()

    def write_cache(self, skills: list[dict]) -> None:
        self.cache_file.write_text(json.dumps({"skills": skills}))

    def test_fresh_cache_avoids_network_request(self) -> None:
        skills = [{"name": "cached"}]
        self.write_cache(skills)

        with patch.object(registry, "_request") as request:
            result = registry.fetch_index()

        self.assertEqual(result, skills)
        request.assert_not_called()

    def test_stale_cache_is_used_when_refresh_fails(self) -> None:
        skills = [{"name": "offline"}]
        self.write_cache(skills)
        os.utime(self.cache_file, (0, 0))

        with (
            patch.object(registry.time, "time", return_value=10_000),
            patch.object(registry, "_request", return_value=None),
        ):
            result = registry.fetch_index()

        self.assertEqual(result, skills)

    def test_force_refresh_replaces_cache(self) -> None:
        self.write_cache([{"name": "old"}])
        fresh = {"skills": [{"name": "fresh"}]}

        with patch.object(registry, "_request", return_value=fresh):
            result = registry.fetch_index(force_refresh=True)

        self.assertEqual(result, fresh["skills"])
        self.assertEqual(json.loads(self.cache_file.read_text()), fresh)


if __name__ == "__main__":
    unittest.main()
