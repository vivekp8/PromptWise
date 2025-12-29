import re


def classify_prompt(text: str) -> str:
    text = text.lower()

    # Define keyword groups
    greeting_keywords = ["hello", "hi", "hey", "greetings", "morning", "good morning"]
    farewell_keywords = ["bye", "goodbye", "see you", "later", "farewell"]

    # Score matches
    greeting_score = sum(1 for kw in greeting_keywords if re.search(rf"\b{kw}\b", text))
    farewell_score = sum(1 for kw in farewell_keywords if re.search(rf"\b{kw}\b", text))

    if greeting_score > farewell_score and greeting_score > 0:
        return "greeting"
    elif farewell_score > greeting_score and farewell_score > 0:
        return "farewell"
    else:
        return "unknown"


def route_prompt(text: str) -> str:
    prompt_type = classify_prompt(text)
    if prompt_type == "greeting":
        return "Hello!"
    elif prompt_type == "farewell":
        return "Goodbye!"
    else:
        return "Unknown prompt type"
