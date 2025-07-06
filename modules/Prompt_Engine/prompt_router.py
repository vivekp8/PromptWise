from datetime import datetime

def route_prompt(prompt_data: dict) -> dict:
    """
    Routes a prompt to the correct LLM endpoint based on the model tag.
    Requires prompt_id, content, and model.
    """
    if not all(k in prompt_data for k in ("prompt_id", "content", "model")):
        return {"status": "error", "message": "Missing required fields"}

    model_tag = prompt_data["model"].lower()
    routing = {
        "text": "LLM_TextModel",
        "data": "LLM_DataModel",
        "default": "LLM_DefaultModel"
    }

    return {
        "status": "success",
        "routed_to": routing.get(model_tag, "LLM_DefaultModel"),
        "timestamp": datetime.utcnow().isoformat()
    }
