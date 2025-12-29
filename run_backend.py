import uvicorn
import os
import sys

# Ensure modules are discoverable
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🚀 Starting PromptWise Backend...")
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
