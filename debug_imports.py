import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


def test_import(module_path, symbol=None):
    try:
        module = __import__(module_path, fromlist=[symbol] if symbol else [])
        print(f"✅ Import succeeded: {module_path}")
    except ImportError as e:
        print(f"❌ Import failed: {module_path}")
        print(f"   Error: {e}")


test_import("Chat_Session_Management.session_controller", "start_session")
test_import("Security_Access_Control.auth_manager", "verify_access")
test_import("Export_Integration_System.exporter", "export")
test_import("Prompt_Engine.prompt_router", "route_prompt")
