from modules.Prompt_Engine.prompt_router import route_prompt

def test_valid_prompt_routing():
    data = {
        "prompt_id": "p001",
        "content": "text: Hello",
        "model": "text"
    }
    response = route_prompt(data)
    assert response["status"] == "success"
    assert response["routed_to"] == "LLM_TextModel"

def test_missing_fields():
    data = { "content": "text: Hello" }  # Missing prompt_id
    response = route_prompt(data)
    assert response["status"] == "error"
