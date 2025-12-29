from Export_Integration_System.pdf_generator import markdown_to_pdf
from modules.Security_Access_Control.auth_manager import verify_access
from modules.Prompt_Engine.prompt_router import route_prompt
from modules.Export_Integration_System.exporter import export_data


def run_test():
    print("🧪 Starting test sequence...\n")

    user_id = "user123"
    session = start_session(user_id)
    print("[Session]", session)

    access = verify_access(user_id, "Prompt_Engine")
    print("[Access Check]", access)

    if access["status"] == "granted":
        prompt = {
            "prompt_id": "test_p001",
            "content": "text: Explain how a black hole works",
            "model": "text",
        }

        result = route_prompt(prompt)
        print("[Routing Result]", result)

        output = export(result, format="json")
        print("[Final Exported Output]\n", output)
    else:
        print("❌ Access Denied. Reason:", access.get("reason", "Unknown"))


if __name__ == "__main__":
    run_test()
