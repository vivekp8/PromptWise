# Export Logic Notes

## Rendering Rules

- Markdown in `.docx` = styled via Headings, Lists, and Tables
- Chat bubbles in `.pdf` = alternating color blocks, timestamps below

## Failure Conditions

- File server timeout → retry 2x, then notify user
- If export fails: fallback to `.json` download
- `.docx` → fallback to `.txt` if rendering library fails

## Suggestions

- Show "Preparing export…" animation if file > 1MB
- Add token badge to footer if "Include metadata" enabled
