import unittest
from unittest.mock import patch, mock_open
from Export_Integration_System.pdf_generator import markdown_to_pdf


class TestPDFGenerator(unittest.TestCase):
    def test_valid_markdown(self):
        result = markdown_to_pdf("# Hello", "output_test.pdf")
        self.assertTrue(result)

    def test_empty_markdown(self):
        result = markdown_to_pdf("", "output_empty.pdf")
        self.assertTrue(result)

    @patch("Export_Integration_System.pdf_generator.open", new_callable=mock_open)
    def test_file_write_failure(self, mock_file):
        mock_file.side_effect = IOError("Disk full")
        result = markdown_to_pdf("# Hello", "output_fail.pdf")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
