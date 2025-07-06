from modules.Chat_Session_Management.session_controller import start_session
from modules.Security_Access_Control.auth_manager import verify_access
from modules.Prompt_Engine.prompt_router import route_prompt
from modules.Export_Integration_System.exporter import export

# Step 1: Start a new session
user_id = "user123"
session = start_session(user_id)
print(f"Session started for {user_id}: {session['session_id']}")

# Step 2: Verify user's access to use Prompt Engine
access = verify_access(user_id, "Prompt_Engine")

if access["status"] == "granted":
    # Step 3: Prepare prompt input
    prompt_data = {
        "prompt_id": "p001",
        "content": "text: What is the theory of relativity?",
        "model": "text"
    }

    # Step 4: Route prompt
    result = route_prompt(prompt_data)
    print("Routing Result:", result)

    # Step 5: Export final output
    exported = export(result, format="json")
    print("Exported Output:\n", exported)

else:
    print("Access Denied:", access["reason"])
