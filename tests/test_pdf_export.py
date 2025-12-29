from Export_Integration_System.pdf_generator import (
    markdown_to_pdf,
)  # 📝 Sample Markdown content (code block rewritten with indentation)

sample_markdown = """
# 📄 Hello from PromptWise

This is a *Markdown* to **PDF** test using a custom CSS theme.

## ✨ Features:
- Custom headers and font
- Styled code blocks and quotes
- Modular export system

Here’s some Python code:

    def modular_thinking():
        print("PromptWise makes it clean!")

    modular_thinking()

> PromptWise: Designed with scalability and style.
"""

# 📍 Output path for the generated PDF
output_path = r"D:\Projects\PromptWise\output_test.pdf"

# 🚀 Generate the PDF
markdown_to_pdf(sample_markdown, output_path)
