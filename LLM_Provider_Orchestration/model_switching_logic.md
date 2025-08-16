# Routing Rules

- GPT-4 = default for high-accuracy
- Claude = fallback for summarization + FAQs
- If provider fails:
  → retry 1x
  → fallback provider if set
