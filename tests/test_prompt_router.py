# tests/test_prompt_router.py

import unittest
from modules.Prompt_Engine import prompt_router


class TestPromptRouter(unittest.TestCase):

    def test_greeting(self):
        result = prompt_router.route_prompt("greeting")
        self.assertEqual(result, "Hello!")

    def test_farewell(self):
        result = prompt_router.route_prompt("farewell")
        self.assertEqual(result, "Goodbye!")

    def test_unknown(self):
        result = prompt_router.route_prompt("random")
        self.assertEqual(result, "Unknown prompt type")


if __name__ == "__main__":
    unittest.main()
