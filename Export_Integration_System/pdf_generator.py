# Export_Integration_System/pdf_generator.py

import markdown
from fpdf import FPDF
import os


def markdown_to_pdf(markdown_text: str, output_path: str) -> bool:
    try:
        # Save markdown to a temporary file with UTF-8 encoding
        temp_md_path = output_path.replace(".pdf", ".md")
        with open(temp_md_path, "w", encoding="utf-8") as f:
            f.write(markdown_text)

        # Convert markdown to HTML
        html = markdown.markdown(markdown_text)

        # Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, html)

        # Save PDF
        pdf.output(output_path)

        # Clean up temp file
        os.remove(temp_md_path)
        return True

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False
