# Prompt Engine

Routes incoming prompt data to one of several LLM endpoints based on its model tag.

## Files
- `prompt_router.py`: Routing logic
- `engine_schema.json`: Prompt input validation

## Usage
Requires: `prompt_id`, `content`, `model`  
Returns: Endpoint name, timestamp, status
