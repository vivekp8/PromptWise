import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import unittest
from core import prompt_engine
from unittest.mock import patch


class TestPromptEngine(unittest.TestCase):
    def test_real_prompts(self):
        self.assertEqual(
            prompt_engine.generate_prompt("admin"),
            "Access granted. Full privileges enabled.",
        )
        self.assertEqual(prompt_engine.generate_prompt("viewer"), "Read-only access.")
        self.assertEqual(prompt_engine.generate_prompt("unknown"), "No access.")

    @patch("core.prompt_engine.generate_prompt")
    def test_mocked_prompt(self, mock_generate):
        mock_generate.return_value = "Mocked response"
        result = prompt_engine.generate_prompt("editor")
        self.assertEqual(result, "Mocked response")
