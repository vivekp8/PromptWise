import unittest


class TestExportIntegration(unittest.TestCase):
    def test_export(self):
        # Placeholder logic
        data = {"project": "PromptWise", "version": "1.0"}
        exported = str(data)
        self.assertIn("PromptWise", exported)
