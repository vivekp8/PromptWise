from weasyprint import HTML, CSS
import markdown2
import os

# ✅ Absolute path to your CSS file
CSS_PATH = r"D:\Projects\PromptWise\frontend\src\assets\pdf_theme.css"

def markdown_to_pdf(markdown_str: str, output_path: str):
    """
    Converts a Markdown string to a styled PDF using WeasyPrint and custom CSS.
    """
    try:
        # Convert Markdown to HTML
        html_str = markdown2.markdown(markdown_str)

        # Prepare WeasyPrint HTML object
        html = HTML(string=html_str)

        # Load custom CSS if available
        css = CSS(filename=CSS_PATH) if os.path.exists(CSS_PATH) else None

        # Generate PDF with or without CSS
        if css:
            html.write_pdf(output_path, stylesheets=[css])
        else:
            html.write_pdf(output_path)

        print(f"[✓] PDF successfully saved to {output_path}")
    except Exception as e:
        print(f"[✗] PDF generation failed: {e}")