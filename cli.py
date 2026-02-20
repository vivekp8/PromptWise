import argparse
from modules.Chat_Session_Management import session_controller
from modules.Prompt_Engine import ml_classifier as prompt_router
from modules.Prompt_Engine import feedback_logger


def main():
    parser = argparse.ArgumentParser(description="PromptWise CLI")
    parser.add_argument("--create", help="User ID to create a session")
    parser.add_argument("--get", help="Session ID to retrieve")
    parser.add_argument("--end", help="Session ID to end")
    parser.add_argument("--prompt", help="Text prompt to classify and route")
    parser.add_argument("--feedback", help="Feedback on routed response (good/bad)")
    args = parser.parse_args()

    if args.create:
        session_id = session_controller.create_session(args.create)
        print(f"[OK] Session created: {session_id}")

    elif args.get:
        session = session_controller.get_session(args.get)
        print(f"[INFO] Session found: {session}" if session else "[ERROR] Session not found.")

    elif args.end:
        result = session_controller.end_session(args.end)
        print(
            f"[STOP] Session ended: {args.end}"
            if result
            else "[ERROR] Session not found or already ended."
        )

    elif args.prompt:
        response = prompt_router.route_prompt(args.prompt)
        print(f"[ROUTE] Routed response: {response}")

        if args.feedback:
            label = prompt_router.classify_prompt(args.prompt)
            feedback_logger.log_feedback(args.prompt, label, args.feedback)
            print(f"[LOG] Feedback logged: {args.feedback}")

    else:
        print("[WARN] No valid command provided. Use --create, --get, --end, or --prompt.")


if __name__ == "__main__":
    main()
